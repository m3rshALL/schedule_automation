from django.contrib import admin
from .models import TimeSlot, Schedule, TaskHistory

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ("id", "day", "start_time", "end_time")
    list_filter = ("day",)
    search_fields = ("day",)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "teacher", "room", "timeslot", "created_at")
    list_filter = ("teacher", "room", "timeslot")
    search_fields = ("course__subject__name", "teacher__name", "room__name")

@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "task_id", "type", "status", "created_at", "result_url")
    list_filter = ("type", "status", "user")
    search_fields = ("task_id", "user__username")
    readonly_fields = ("created_at",)
