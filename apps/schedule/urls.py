from django.urls import path
from .views import OptimizeScheduleView, OptimizeScheduleStatusView, ScheduleExportView, ScheduleAsyncExportView, ScheduleAsyncExportStatusView

urlpatterns = [
    path('optimize/', OptimizeScheduleView.as_view(), name='optimize-schedule'),
    path('optimize/status/', OptimizeScheduleStatusView.as_view(), name='optimize-schedule-status'),
    path('export/', ScheduleExportView.as_view(), name='export-schedule'),
    path('export/async/', ScheduleAsyncExportView.as_view(), name='export-schedule-async'),
    path('export/async/status/', ScheduleAsyncExportStatusView.as_view(), name='export-schedule-async-status'),
] 