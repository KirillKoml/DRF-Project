from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscription


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    number_of_lessons = SerializerMethodField()
    def get_number_of_lessons(self, course):
        return course.course.count()
    class Meta:
        model = Course
        fields = ("id", "name", "preview", "description", "creator", "number_of_lessons")


class CourseCreateSerializer(ModelSerializer):
    """Сериализатор для создания моделей курсов."""
    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description')


class SubscriptionSerializer(ModelSerializer):
    """Сериализатор для подписок на курс."""

    class Meta:
        model = Subscription
        fields = '__all__'

