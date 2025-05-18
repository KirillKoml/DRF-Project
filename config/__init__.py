from .celery import app as celery_app

# Настройка для Celery
__all__ = ('celery_app',)