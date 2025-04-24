from django.db import models

from config.settings import AUTH_USER_MODEL


# Create your models here.
class Course(models.Model):
    """Модель курса."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        verbose_name="Превью(изображение)",
        null=True,
        blank=True,
        upload_to="materials/course",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Создатель",
        related_name="user_course",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.title}"


class Lesson(models.Model):
    """Модель урока."""

    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )
    preview = models.ImageField(
        verbose_name="Превью(изображение)",
        null=True,
        blank=True,
        upload_to="materials/lesson",
    )
    link_to_video = models.TextField(
        verbose_name="Ссылка на видео", null=True, blank=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        related_name="course",
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель",
        related_name="user_lesson",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["pk"]

    def __str__(self):
        return f"{self.title}"


class Subscription(models.Model):
    """Модель подписки на курс."""

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь который подписался на курс",
        related_name="user_subscription",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс на который подписался пользователь",
        related_name="course_subscription",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user}"
