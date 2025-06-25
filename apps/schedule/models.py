from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class TimeSlot(models.Model):
    day = models.CharField(_("Day of the Week"), max_length=10)
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))

    class Meta:
        verbose_name = _("Time Slot")
        verbose_name_plural = _("Time Slots")
        unique_together = ("day", "start_time", "end_time")

    def __str__(self):
        return f"{self.day} {self.start_time:%H:%M} - {self.end_time:%H:%M}"


class Schedule(models.Model):
    course = models.ForeignKey(
        "academics.Course", on_delete=models.CASCADE, related_name="schedules"
    )
    teacher = models.ForeignKey(
        "faculty.Teacher", on_delete=models.CASCADE, related_name="schedules"
    )
    room = models.ForeignKey(
        "facilities.Room", on_delete=models.CASCADE, related_name="schedules"
    )
    timeslot = models.ForeignKey(
        "schedule.TimeSlot", on_delete=models.CASCADE, related_name="schedules"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")
        unique_together = (("teacher", "timeslot"), ("room", "timeslot"))

    def __str__(self):
        return f"{self.course} in {self.room} at {self.timeslot}"


class TaskHistory(models.Model):
    TASK_TYPE_CHOICES = [
        ("import", "Импорт"),
        ("export", "Экспорт"),
    ]
    STATUS_CHOICES = [
        ("PENDING", "В очереди"),
        ("STARTED", "Выполняется"),
        ("SUCCESS", "Завершено"),
        ("FAILURE", "Ошибка"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schedule_tasks")
    task_id = models.CharField(max_length=64, unique=True)
    type = models.CharField(max_length=16, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    result_url = models.CharField(max_length=255, blank=True, null=True)
    result_data = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Задача импорта/экспорта расписания"
        verbose_name_plural = "История задач импорта/экспорта"

    def __str__(self):
        return f"{self.get_type_display()} {self.task_id} ({self.status})"
