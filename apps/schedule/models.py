from django.db import models
from django.utils.translation import gettext_lazy as _


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
