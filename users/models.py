from django.contrib.auth.models import AbstractUser
from django.db import models
import lms.models


class User(AbstractUser):
    username = None

    email = models.CharField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар пользователя",
        null=True,
        blank=True,
    )

    country = models.CharField(
        max_length=15, verbose_name="Страна", null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user",
        null=True,
        blank=True,
    )
    date_of_payment = models.DateField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        lms.models.Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        related_name="paid_course",
        null=True,
        blank=True,
    )
    paid_lesson = models.ForeignKey(
        lms.models.Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        related_name="paid_lesson",
        null=True,
        blank=True,
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=37,
        choices=(
            ("cash", "Наличные"),
            ("non-cash", "Безнал"),
            ("cash and non-cash", "Частично наличные и частично безнал"),
        ),
        verbose_name="Способ оплаты(3 на выбор)",
    )
    id_session = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Id сессии"
    )
    payment_link = models.URLField(
        max_length=400,
        null=True,
        blank=True,
        verbose_name="Ссылка на оплату"
    )
    payment_status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Статус оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Пользователь - {self.user}, оплатил {self.payment_amount}"
