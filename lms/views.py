from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer, CourseCreateSerializer
from users.permissions import ModeratorPermission, CreatorPermission


class CourseViewSet(ModelViewSet):
    """ViewSet для моделей курсов."""
    queryset = Course.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return CourseCreateSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        """Метод для автоматической привязки создающего пользователя к модели курс."""
        course = serializer.save()
        course.creator = self.request.user
        course.save()

    def get_permissions(self):
        """Метод для распределения прав доступа."""
        # Если действие на создание, то проверяем не является ли пользователь модератором
        if self.action == 'create':
            self.permission_classes = (~ModeratorPermission,)

        # Если действие на обновление или просмотр, то допускаем модератора или создателя курса
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (ModeratorPermission | CreatorPermission | IsAdminUser,)

        # Если действие на просмотр всех курсов, то допускаем только модератора или админа
        elif self.action == 'list':
            self.permission_classes = (ModeratorPermission | IsAdminUser,)

        # Если действие на удаление, то проверяем не является ли пользователь модератором и является ли он создателем
        # курса
        elif self.action == 'destroy':
            self.permission_classes = (~ModeratorPermission | CreatorPermission,)

        return super().get_permissions()

class LessonCreateApiView(CreateAPIView):
    """Класс для создания моделей уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Доступ имеют все авторизованные пользователи, кроме модераторов
    permission_classes = (~ModeratorPermission, IsAuthenticated)

    def perform_create(self, serializer):
        """Метод для автоматической привязки создающего пользователя к модели урок."""
        lesson = serializer.save()
        lesson.creator = self.request.user
        lesson.save()



class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (ModeratorPermission | IsAdminUser, IsAuthenticated)


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (ModeratorPermission | CreatorPermission, IsAuthenticated)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (ModeratorPermission | CreatorPermission, IsAuthenticated)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (ModeratorPermission | CreatorPermission, IsAuthenticated)
