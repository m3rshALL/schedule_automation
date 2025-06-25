from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CourseViewSet, StudentGroupViewSet, SubjectViewSet, StudentGroupExportView, CourseExportView

router = DefaultRouter()
router.register(r"subjects", SubjectViewSet, basename="subject")
router.register(r"student-groups", StudentGroupViewSet, basename="student-group")
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = router.urls + [
    path('export/groups/', StudentGroupExportView.as_view(), name='export-groups'),
    path('export/courses/', CourseExportView.as_view(), name='export-courses'),
] 