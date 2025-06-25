from rest_framework import viewsets

# Create your views here.

from .models import Equipment, Room
from .serializers import EquipmentSerializer, RoomSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows equipment to be viewed or edited.
    """

    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """

    queryset = Room.objects.all().prefetch_related("equipment")
    serializer_class = RoomSerializer
