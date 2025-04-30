from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    """Команда для создания 2 платежей(1 платеж за курс, 2 за урок)."""
    def handle(self, *args, **options):
        # создаю пользователя специально для команды
        user = User.objects.create(email='test_command@mail.ru')
        user.set_password('12345')
        user.save()

        # Создаю урок и курс специально для команды
        course = Course.objects.create(name='test_course', description='test_description')
        lesson = Lesson.objects.create(name='test_lesson', description='test_description', course=course)

        # Создаю платеж за курс
        payment_course = Payment.objects.create(user=user, date_of_payment='2024-09-21',
                                                paid_course=course, payment_amount=200000,
                                                payment_method='cash')
        payment_course.save()

        # Создаю платеж за урок
        payment_lesson = Payment.objects.create(user=user, date_of_payment='2024-09-21',
                                                paid_lesson=lesson, payment_amount=15000,
                                                payment_method='non-cash')
        payment_lesson.save()