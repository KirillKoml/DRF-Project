from rest_framework.viewsets import ModelViewSet

from lms.models import Course
from lms.serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    queryser = Course.objects.all()
    serializer_class = CourseSerializer
