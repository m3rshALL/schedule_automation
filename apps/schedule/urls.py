from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    OptimizeScheduleView, OptimizeScheduleStatusView, ScheduleExportView, ScheduleAsyncExportView, ScheduleAsyncExportStatusView,
    TimeSlotViewSet, ScheduleViewSet, ScheduleImportExportView, TaskHistoryStatusAPIView
)

router = DefaultRouter()
router.register(r'timeslots', TimeSlotViewSet, basename='timeslot')
router.register(r'schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', ScheduleImportExportView.as_view(), name='schedule-import-export'),
    path('tasks/status/', TaskHistoryStatusAPIView.as_view(), name='taskhistory-status'),
] + router.urls + [
    path('optimize/', OptimizeScheduleView.as_view(), name='optimize-schedule'),
    path('optimize/status/', OptimizeScheduleStatusView.as_view(), name='optimize-schedule-status'),
    path('export/', ScheduleExportView.as_view(), name='schedule-export'),
    path('export/async/', ScheduleAsyncExportView.as_view(), name='export-schedule-async'),
    path('export/async/status/', ScheduleAsyncExportStatusView.as_view(), name='export-schedule-async-status'),
] 