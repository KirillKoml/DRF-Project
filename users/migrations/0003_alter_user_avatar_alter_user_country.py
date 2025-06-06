# Generated by Django 5.2 on 2025-05-14 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                help_text="Загрузите изображение",
                null=True,
                upload_to="users/avatars",
                verbose_name="Аватар пользователя",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="country",
            field=models.CharField(
                blank=True,
                help_text="Укажите страну",
                max_length=15,
                null=True,
                verbose_name="Страна",
            ),
        ),
    ]
