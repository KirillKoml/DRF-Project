from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from users.models import User


@shared_task
def sending_email_to_course_subscribers(email_course_subscribers):
    """Отложенная задача по отправке письма подписчикам курса, если курс обновился."""
    # Функция по отправке письма
    send_mail('Привет!', 'Курс на который ты подписан обновился', EMAIL_HOST_USER,
              email_course_subscribers)


@shared_task
def blocking_user():
    """Периодическая задача которая блокирует пользователей если они были последний раз в сети более 30 дней."""
    # Получаю сегодняшнюю дату
    today = timezone.now()

    # Отсекаю пользователей у которых нет даты последнего входа
    users = User.objects.filter(last_login__isnull=False)

    # Начинаю сравнивать у каждого пользователя дату последнего входа и текущую дату и если разница более 30 дней, то
    # удаляю пользователя
    for user in users:
        if today - user.last_login > timedelta(days=30/31):
            user.is_active = False
            user.save()