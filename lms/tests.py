from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


# Create your tests here.
class CourseTestCase(APITestCase):
    """Тесты для курсов."""

    def setUp(self):
        """Создаю пользователя, курс, урок и авторизую пользователя."""
        self.user = User.objects.create(email='test_case@yandex.ru', password='12345', is_staff=True, is_superuser=True)
        self.course = Course.objects.create(name='test_case_title', description='test_case_description',
                                            creator=self.user)
        self.lesson = Lesson.objects.create(name='test_case_title', description='test_case_description',
                                            course=self.course, creator=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тест на детальный просмотр курса."""
        # Получаю урл для информации об отдельном курсе
        url = reverse('lms:course-detail', args=(self.course.pk,))

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
            data.get('name'), self.course.name
        )

    def test_course_create(self):
        """Тест на создание курса."""
        # Получаю урл для информации о всех курсах
        url = reverse('lms:course-list')

        # Заполняю данные курса
        data = {'name': 'testov', 'description': 'testov', 'creator': self.user}

        # Делаю запрос на полученный урл
        response = self.client.post(url, data)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        # Тест экземпляр модели успешно создался в БД
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        """Тест на обновление курса."""
        # Получаю урл для просмотра курса
        url = reverse('lms:course-detail', args=(self.course.pk,))

        # Заполняю данные для обновления курса
        data = {'name': 'testov'}

        # Делаю запрос на полученный урл
        response = self.client.patch(url, data)

        # Преобразую ответ в JSON
        data = response.json()

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Тест обновление курса
        self.assertEqual(
            data.get('name'), 'testov'
        )

    def test_course_delete(self):
        """Тест на удаление курса."""
        # Получаю урл для просмотра курса
        url = reverse('lms:course-detail', args=(self.course.pk,))

        # Делаю запрос на полученный урл
        response = self.client.delete(url)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        # Тест экземпляр модели успешно удалился из БД
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        """Тест на просмотр списка курсов."""
        # Получаю урл для информации о всех курсах
        url = reverse('lms:course-list')

        # Делаю запрос на полученный урл
        response = self.client.get(url)
        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Подготавливаем ожидаемый результат и сравниваем с получившимся
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "preview": None,
                    "description": self.course.description,
                    "number_of_lessons": Lesson.objects.filter(course=self.course.pk).count(),
                    "creator": self.user.pk,
                    "subscription": "Подписка не активна"
                }
            ]
        }
        data = response.json()
        self.assertEqual(
            data, result
        )


class LessonTestCase(APITestCase):
    """Тесты для уроков."""

    def setUp(self):
        """Создаю пользователя, курс, урок и авторизую пользователя."""
        self.user = User.objects.create(email='test_case@yandex.ru', password='12345', is_staff=True, is_superuser=True)
        self.course = Course.objects.create(title='test_case_name', description='test_case_description',
                                            creator=self.user)
        self.lesson = Lesson.objects.create(title='test_case_name', description='test_case_description',
                                            course=self.course, creator=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест на детальный просмотр курса."""
        # Получаю урл для информации об отдельном уроке
        url = reverse('lms:lesson-retrieve', args=(self.lesson.pk,))

        # Делаю запрос на полученный урл
        response = self.client.get(url)

        # Преобразую ответ в JSON
        data = response.json()

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Тест создание названия урока
        self.assertEqual(
            data.get('name'), self.lesson.name
        )

    def test_lesson_create(self):
        """Тест на создание урока."""
        # Получаю урл для создания урока
        url = reverse('lms:lesson-create')

        # Заполняю данные урока
        data = {'name': 'testov', 'description': 'testov', 'course': self.course.pk, 'creator': self.user.pk,
                'link_to_video': 'https://www.youtube.com/'}

        # Делаю запрос на полученный урл
        response = self.client.post(url, data)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

        # Тест экземпляр модели успешно создался в БД
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """Тест на обновление урока."""
        # Получаю урл для просмотра урока
        url = reverse('lms:lesson-update', args=(self.lesson.pk,))

        # Заполняю данные для обновления урока
        data = {'name': 'testov'}

        # Делаю запрос на полученный урл
        response = self.client.patch(url, data)

        # Преобразую ответ в JSON
        data = response.json()

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Тест обновление урока
        self.assertEqual(
            data.get('name'), 'testov'
        )

    def test_lesson_delete(self):
        """Тест на удаление урока."""
        # Получаю урл для удаления урока
        url = reverse('lms:lesson-destroy', args=(self.lesson.pk,))

        # Делаю запрос на полученный урл
        response = self.client.delete(url)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

        # Тест экземпляр модели успешно удалился из БД
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        """Тест на просмотр списка уроков."""
        # Получаю урл для информации о всех уроках
        url = reverse('lms:lesson-list')

        # Делаю запрос на полученный урл
        response = self.client.get(url)

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Подготавливаем ожидаемый результат и сравниваем с получившимся
        result = {
            "count": Lesson.objects.all().count(),
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "link_to_video": None,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "creator": self.user.pk
                }
            ]
        }
        data = response.json()
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    """Тесты для подписок на курс."""

    def setUp(self):
        """Создаю пользователя, курс, подписку на курс и авторизую пользователя."""
        self.user = User.objects.create(email='test_case@yandex.ru', password='12345', is_staff=True, is_superuser=True)
        self.course = Course.objects.create(title='test_case_name', description='test_case_description',
                                            creator=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)

    def test_subscription_delete(self):
        """Тест на удаление подписки на курс."""
        # Получаю урл для удаления подписки на курс
        url = reverse('lms:subscription')

        # Создаю данные для запроса
        data = {"course": self.course.pk}

        # Делаю запрос на полученный урл
        response = self.client.post(url, data)

        # Преобразую ответ в JSON
        data = response.json()

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Тест экземпляр модели успешно удалился из БД
        self.assertEqual(
            Subscription.objects.all().count(), 0
        )

        # Тест вывод сообщения 'Подписка удалена'
        self.assertEqual(
            data.get('message'), 'Подписка удалена'
        )

    def test_subscription_create(self):
        """Тест на создание подписки на курс."""
        # Заранее удаляю подписку на курс созданную в setUp
        Subscription.objects.filter(pk=self.subscription.pk).delete()

        # Получаю урл для создания подписки на курс
        url = reverse('lms:subscription')

        # Создаю данные для запроса
        data = {"course": self.course.pk}

        # Делаю запрос на полученный урл
        response = self.client.post(url, data)

        # Преобразую ответ в JSON
        data = response.json()

        # Тест статус код
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        # Тест экземпляр модели успешно создался из БД
        self.assertEqual(
            Subscription.objects.all().count(), 1
        )

        # Тест вывод сообщения 'Подписка добавлена'
        self.assertEqual(
            data.get('message'), 'Подписка добавлена'
        )
