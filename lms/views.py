from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from lms.models import Course, Lesson, Subscription
from lms.paginators import CourseAndLessonPagination
from lms.serializers import CourseSerializer, LessonSerializer, CourseCreateSerializer, SubscriptionSerializer
from users.permissions import ModeratorPermission, CreatorPermission

from lms.tasks import sending_email_to_course_subscribers


# Декоратор для CourseViewSet
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Вывод списка курсов"
))
class CourseViewSet(ModelViewSet):
    """ViewSet для моделей курсов."""
    queryset = Course.objects.all()

    # Указываю пагинацию
    pagination_class = CourseAndLessonPagination

    def get_serializer_class(self):
        """Метод для выбора другого сериализатора при создании модели."""
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

    def perform_update(self, serializer):
        # Получаю название курса
        course_name = self.get_object()

        # Получаю queryset подписанных пользователей
        queryset_users_subscribed_to_course = Subscription.objects.filter(course=course_name)

        # Создаю список с пользователями которым надо отправить письмо об обновлении курса
        email_course_subscribers_list = []
        for email_users in queryset_users_subscribed_to_course:
            email_course_subscribers_list.append(email_users.user.email)

        # Добавляю отложенную задачу по отправке писем подписчикам курса
        sending_email_to_course_subscribers.delay(email_course_subscribers_list)
        serializer.save()


class LessonCreateAPIView(CreateAPIView):
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


class LessonListAPIView(ListAPIView):
    """Класс для вывода моделей уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Доступ имеют только модераторы
    permission_classes = (ModeratorPermission | IsAdminUser, IsAuthenticated)

    # Указываю пагинацию
    pagination_class = CourseAndLessonPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    """Класс для вывода отдельной модели урока."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Доступ имеют только модераторы или создатель урока
    permission_classes = (ModeratorPermission | CreatorPermission, IsAuthenticated)


class LessonUpdateAPIView(UpdateAPIView):
    """Класс для редактирования моделей уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Доступ имеют только модератор и создатель урока
    permission_classes = (ModeratorPermission | CreatorPermission, IsAuthenticated)


class LessonDestroyAPIView(DestroyAPIView):
    """Класс для удаления моделей уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Доступ имеет только создатель урока
    permission_classes = (~ModeratorPermission | CreatorPermission, IsAuthenticated)


class SubscriptionAPIView(APIView):
    """Класс для создания или удаления подписки на курс"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Класс для создания или удаления подписки на курс",
                         methods=['put', 'post'],
                         request_body=SubscriptionSerializer)
    @api_view(['GET', 'PUT', 'POST'])
    def post(self, request, *args, **kwargs):
        # Получаю пользователя, id курса и сам курс
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course)
        try:
            # Если программа смогла найти подписку, то я её удаляю
            subs_item.exist()
            subs_item.delete()
            message = 'Подписка удалена'
            sending_email_to_course_subscribers(course_id)
        except Subscription.DoesNotExist:
            # Если программа не смогла найти подписку, то я создаю эту подписку
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
            sending_email_to_course_subscribers(course_id)

        # Возвращаю сообщение о статусе подписки
        return Response({ message: 'message'})
