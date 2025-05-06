from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.permissions import UserHimself
from users.serializers import UserSerializer, PaymentSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserNonCreatorSerializer, PaymentStatusSerializer

from django_filters.rest_framework import DjangoFilterBackend


#from users.services import conversion_rub_into_usd, create_stripe_price, create_stripe_session, create_stripe_product, \
#    checking_status_payment


# Create your views here.
class UserCreateAPIView(CreateAPIView):
    """Класс для создания моделей пользователей."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Вмешиваюсь в логику контроллера для его правильной регистрации пользователей."""
        # Сохраняю пользователя и сразу делаю его активным
        user = serializer.save(is_active=True)

        # Хэширую пароль пользователя и сохраняю пользователя
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Класс для вывода всех моделей пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Класс для редактирования моделей пользователей."""
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (UserHimself, IsAuthenticated)


class UserRetrieveAPIView(RetrieveAPIView):
    """Класс для просмотра детальной информации об отдельном пользователе."""
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Метод для выбора сериализатора в зависимости от того является ли пользователь владельцем профиля или нет."""
        if self.request.user == self.get_object():
            return UserSerializer
        return UserNonCreatorSerializer


class UserDestroyAPIView(DestroyAPIView):
    """Класс для удаления пользователя."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentCreateAPIView(CreateAPIView):
    """Класс для создания платежей пользователей."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """Метод для автоматической привязки создающего пользователя к модели платеж, конвертации платежа в USD,
        создания цены Stripe, получения id сессии и ссылки на оплату."""
        payment = serializer.save()
        # Привязываем пользователя к модели платеж
        payment.user = self.request.user
        # Создаем продукт в Stripe из курса
        if payment.paid_course:
            stripe_product = create_stripe_product(payment.paid_course.title)
        else:
            stripe_product = create_stripe_product(payment.paid_lesson.title)
        # Конвертируем рубли в USD
        payment_amount_usd = conversion_rub_into_usd(payment.payment_amount)
        # Создаем цену в Stripe
        stripe_price = create_stripe_price(payment_amount_usd, stripe_product)
        # Получаем id сессии и ссылку на оплату
        session_id, session_url = create_stripe_session(stripe_price)
        # Записываем id сессии и ссылку на оплату в модель платежа
        payment.id_session = session_id
        payment.payment_link = session_url
        payment.save()


class PaymentListAPIView(ListAPIView):
    """Класс для вывода всех платежей."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Добавляю фильтрацию по способу оплаты, оплаченному уроку или курсу
    filterset_fields = ('payment_method', 'paid_course', 'paid_lesson')

    # Добавляю сортировку по дате оплаты курса или урока
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ('date_of_payment',)


class PaymentStatusRetrieveView(RetrieveAPIView):
    """Класс для просмотра статуса платежа по id сессии."""
    queryset = Payment.objects.all()
    serializer_class = PaymentStatusSerializer

    def get_object(self):
        """Метод для получения статуса оплаты"""
        # Получаю pk платежа и сам платеж
        payment_pk = self.kwargs['pk']
        payment = Payment.objects.get(pk=payment_pk)
        # Получаю статус платежа и сохраняю объект
        payment.payment_status = checking_status_payment(payment.id_session)
        payment.save()
        return Payment.objects.get(pk=payment_pk)