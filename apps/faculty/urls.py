from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import TeacherViewSet, TeacherExportView, TeacherAsyncExportView, TeacherAsyncExportStatusView

router = DefaultRouter()
router.register(r"teachers", TeacherViewSet, basename="teacher")

urlpatterns = router.urls + [
    path('export/teachers/', TeacherExportView.as_view(), name='export-teachers'),
    path('export/teachers/async/', TeacherAsyncExportView.as_view(), name='export-teachers-async'),
    path('export/teachers/async/status/', TeacherAsyncExportStatusView.as_view(), name='export-teachers-async-status'),
] 