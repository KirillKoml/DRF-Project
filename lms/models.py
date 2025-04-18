from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    image = models.ImageField(
        upload_to="lms/image",
        verbose_name="Превью(Картинка)",
        help_text="Загрузите превью(Картинку)",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
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
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="lms/image",
        verbose_name="Превью(Картинка)",
        help_text="Загрузите превью(Картинку)",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
