# Generated by Django 5.2 on 2025-04-30 20:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0003_delete_subscription"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_of_payment", models.DateField(verbose_name="Дата оплаты")),
                (
                    "payment_amount",
                    models.PositiveIntegerField(verbose_name="Сумма оплаты"),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("cash", "Наличные"),
                            ("non-cash", "Безнал"),
                            (
                                "cash and non-cash",
                                "Частично наличные и частично безнал",
                            ),
                        ],
                        max_length=37,
                        verbose_name="Способ оплаты(3 на выбор)",
                    ),
                ),
                (
                    "id_session",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Id сессии"
                    ),
                ),
                (
                    "payment_link",
                    models.URLField(
                        blank=True,
                        max_length=400,
                        null=True,
                        verbose_name="Ссылка на оплату",
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Статус оплаты",
                    ),
                ),
                (
                    "paid_course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="paid_course",
                        to="lms.course",
                        verbose_name="Оплаченный курс",
                    ),
                ),
                (
                    "paid_lesson",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="paid_lesson",
                        to="lms.lesson",
                        verbose_name="Оплаченный урок",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
    ]
