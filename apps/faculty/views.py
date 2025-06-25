from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

from .models import Teacher
from .serializers import TeacherSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.prefetch_related("qualifications").all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "qualifications"]
    search_fields = ["name", "qualifications__name"]
    ordering_fields = ["name"]
    permission_classes = [permissions.IsAdminUser]
