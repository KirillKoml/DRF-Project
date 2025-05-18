from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonUpdateAPIView, \
    LessonRetrieveAPIView, LessonDestroyAPIView, SubscriptionAPIView

from lms.apps import LmsConfig

app_name = LmsConfig.name

# Создаем экземпляр класса SimpleRouter
router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    # Урлы для уроков
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/destroy/', LessonDestroyAPIView.as_view(), name='lesson-destroy'),

    # Урлы для подписок на курс
    path('subscription/', SubscriptionAPIView.as_view(), name='subscription'),
]

urlpatterns += router.urls
