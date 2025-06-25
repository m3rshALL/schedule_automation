from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity", "room_type", "block")
    list_filter = ("room_type", "block")
    search_fields = ("name",)
