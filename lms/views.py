from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView, get_object_or_404
)

from lms.models import Course, Lesson, Subscription
from lms.paginators import CourseAndLessonPagination
from lms.serializers import CourseSerializer, LessonSerializer, CourseCreateSerializer, SubscriptionSerializer
from users.permissions import ModeratorPermission, CreatorPermission


class CourseViewSet(ModelViewSet):
    """ViewSet для моделей курсов."""
    queryset = Course.objects.all()

    # Указываю пагинацию
    pagination_class = CourseAndLessonPagination

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

class SubscriptionApiView(APIView):
    """Класс для создания или удаления подписки на курс"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        # Получаю пользователя, id курса и сам курс
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)

        try:
            # Если программа смогла найти подписку, то я её удаляю
            subscription_find = Subscription.objects.get(user=user, course=course)
            subscription_find.delete()
            message = 'Подписка удалена'
        except Subscription.DoesNotExist:
            # Если программа не смогла найти подписку, то я создаю эту подписку
            subscription_create = Subscription.objects.create(user=user, course=course)
            subscription_create.save()
            message = 'Подписка добавлена'

        # Возвращаю сообщение о статусе подписки
        return Response({'message': message})
