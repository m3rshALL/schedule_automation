from rest_framework import viewsets

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


class StudentGroupViewSet(viewsets.ModelViewSet):
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("subject", "student_group").all()
    serializer_class = CourseSerializer
