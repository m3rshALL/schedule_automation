from django.urls import path
from .views import (
    StudentGroupImportView,
    TeacherImportView,
    EquipmentImportView,
    RoomImportView,
    CourseImportView,
    ScheduleImportView,
)

urlpatterns = [
    path('groups/', StudentGroupImportView.as_view(), name='import-student-groups'),
    path('teachers/', TeacherImportView.as_view(), name='import-teachers'),
    path('equipment/', EquipmentImportView.as_view(), name='import-equipment'),
    path('rooms/', RoomImportView.as_view(), name='import-rooms'),
    path('courses/', CourseImportView.as_view(), name='import-courses'),
    path('schedule/', ScheduleImportView.as_view(), name='import-schedule'),
] 