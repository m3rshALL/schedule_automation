from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, StudentGroupViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r"subjects", SubjectViewSet, basename="subject")
router.register(r"student-groups", StudentGroupViewSet, basename="student-group")
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = router.urls 