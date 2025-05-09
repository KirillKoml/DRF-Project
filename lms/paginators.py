from rest_framework.pagination import PageNumberPagination


class CourseAndLessonPagination(PageNumberPagination):
    page_size = 5