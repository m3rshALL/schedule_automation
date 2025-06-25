from django.contrib import admin
from .models import Room, Equipment

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity", "room_type", "block")
    list_filter = ("room_type", "block")
    search_fields = ("name",)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
