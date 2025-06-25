from rest_framework import serializers

from .models import Equipment, Room


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "capacity",
            "room_type",
            "equipment",
        ) 