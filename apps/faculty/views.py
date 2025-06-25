from rest_framework import viewsets

# Create your views here.

from .models import Teacher
from .serializers import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.prefetch_related("qualifications").all()
    serializer_class = TeacherSerializer
