from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import User, Payment


# Create your tests here.
class UserTestCase(APITestCase):
    """Тесты для пользователей."""

    def setUp(self):
        """Создаю пользователя и авторизую его."""
        self.user = User.objects.create(email='test_case@example.ru', password='12345', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тест на создание пользователя."""
        # Получаю урл для создания пользователя
        url = reverse('users:register')

        # Заполняю данные пользователя
        data = {'email': 'test_email@yandex.ru', 'password': '12345'}

        # Делаю запрос на полученный урл
        response = self.client.post(url, data)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        # Тест экземпляр модели успешно создался в БД
        self.assertEqual(
            User.objects.all().count(), 2
        )

    def test_user_retrieve(self):
        """Тест на детальный просмотр пользователя."""
        # Получаю урл для информации об отдельном пользователе
        url = reverse('users:user-retrieve', args=(self.user.pk,))

        # Делаю запрос на полученный урл
        response = self.client.get(url)

        # Преобразую ответ в JSON
        data = response.json()

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Тест создание названия курса
        self.assertEqual(
            data.get('email'), self.user.email
        )

    def test_user_update(self):
        """Тест на обновление пользователя."""
        # Получаю урл для просмотра пользователя
        url = reverse('users:user-update', args=(self.user.pk,))

        # Заполняю данные для обновления пользователя
        data = {'phone_number': '+79663210099'}

        # Делаю запрос на полученный урл
        response = self.client.patch(url, data)

        # Преобразую ответ в JSON
        data = response.json()

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Тест обновление пользователя
        self.assertEqual(
            data.get('phone_number'), '+79663210099'
        )

    def test_user_delete(self):
        """Тест на удаление пользователя."""
        # Получаю урл для удаления пользователя
        url = reverse('users:user-destroy', args=(self.user.pk,))

        # Делаю запрос на полученный урл
        response = self.client.delete(url)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        # Тест экземпляр модели успешно удалился из БД
        self.assertEqual(
            User.objects.all().count(), 0
        )

    def test_user_list(self):
        """Тест на просмотр списка пользователей."""
        # Получаю урл для информации о всех пользователях
        url = reverse('users:user-list')

        # Делаю запрос на полученный урл
        response = self.client.get(url)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Подготавливаем ожидаемый результат и сравниваем с получившимся
        result = [
            {
                "id": self.user.pk,
                "email": self.user.email,
                "phone_number": None,
                "city": None,
                "profile_picture": None,
                "payment_history": [],
                "password": self.user.password
            }
        ]
        data = response.json()
        self.assertEqual(
            data, result
        )


class PaymentTestCase(APITestCase):
    """Тесты для платежей."""

    def setUp(self):
        """Создаю пользователя, курс, платеж и авторизую пользователя."""
        self.user = User.objects.create(email='test_case@yandex.ru', password='12345', is_staff=True, is_superuser=True)
        self.course = Course.objects.create(title='test_case_title', description='test_case_description',
                                            creator=self.user)
        self.payment = Payment.objects.create(user=self.user, date_of_payment='2024-10-11', paid_course=self.course,
                                              payment_amount=15000, payment_method='cash',
                                              id_session='cs_test_a1dDPxHLFpMZlQpBKNNC8YnpB0InWUMPEB28ZS160iQ0Y5lIICQkacgdlH')
        self.client.force_authenticate(user=self.user)

    def test_payment_create(self):
        """Тест на создание платежа."""
        # Получаю урл для создания платежа
        url = reverse('users:payment-create')

        # Заполняю данные платежа
        data = {'date_of_payment': '2023-10-11', 'paid_course': self.course.pk,
                'payment_amount': 15000, 'payment_method': 'cash'}

        # Делаю запрос на полученный урл
        response = self.client.post(url, data)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        # Тест экземпляр модели успешно создался в БД
        self.assertEqual(
            Payment.objects.all().count(), 2
        )

    def test_payment_list(self):
        """Тест на просмотр списка платежей."""
        # Получаю урл для информации о всех платежах
        url = reverse('users:payment-list')

        # Делаю запрос на полученный урл
        response = self.client.get(url)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Подготавливаем ожидаемый результат и сравниваем с получившимся
        result = [
            {
                "id": self.payment.pk,
                "date_of_payment": self.payment.date_of_payment,
                "payment_amount": self.payment.payment_amount,
                "payment_method": self.payment.payment_method,
                "user": self.user.pk,
                "paid_course": self.course.pk,
                "paid_lesson": None,
                "id_session": self.payment.id_session,
                "payment_link": self.payment.payment_link,
                "payment_status": None
            }
        ]
        data = response.json()
        self.assertEqual(
            data, result
        )

    def test_payment_status(self):
        """Тест на просмотр статуса оплаты."""
        # Получаю урл для информации о статусе оплаты
        url = reverse('users:payment-status', args=(self.payment.pk,))

        # Делаю запрос на полученный урл
        response = self.client.get(url)

        # Преобразую ответ в JSON
        data = response.json()

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Тест создание названия курса
        self.assertEqual(
            data.get('id_session'), self.payment.id_session
        )



