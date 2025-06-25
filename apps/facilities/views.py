from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

from .models import Equipment, Room
from .serializers import EquipmentSerializer, RoomSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows equipment to be viewed or edited.
    """

    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["name"]
    permission_classes = [permissions.IsAdminUser]


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """

    queryset = Room.objects.all().prefetch_related("equipment")
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "capacity", "room_type", "block", "equipment"]
    search_fields = ["name", "block"]
    ordering_fields = ["name", "capacity", "room_type", "block"]
    permission_classes = [permissions.IsAdminUser]
