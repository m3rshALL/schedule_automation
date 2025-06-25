from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

from .models import Course, StudentGroup, Subject
from .serializers import (
    CourseSerializer,
    StudentGroupSerializer,
    SubjectSerializer,
)


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "code"]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "code"]
    permission_classes = [permissions.IsAdminUser]


class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "size"]
    search_fields = ["name"]
    ordering_fields = ["name", "size"]
    permission_classes = [permissions.IsAdminUser]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("subject", "student_group").all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        "subject",
        "student_group",
        "course_year",
        "lesson_type",
        "is_mook",
        "is_elective",
        "elective_group",
        "parent_course",
    ]
    search_fields = ["subject__name", "student_group__name"]
    ordering_fields = ["course_year", "lesson_type"]
    permission_classes = [permissions.IsAdminUser]
