from django.urls import path
from .views import OptimizeScheduleView, OptimizeScheduleStatusView, ScheduleExportView

urlpatterns = [
    path('optimize/', OptimizeScheduleView.as_view(), name='optimize-schedule'),
    path('optimize/status/', OptimizeScheduleStatusView.as_view(), name='optimize-schedule-status'),
    path('export/', ScheduleExportView.as_view(), name='export-schedule'),
] 