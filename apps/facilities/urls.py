from rest_framework.routers import DefaultRouter

from .views import EquipmentViewSet, RoomViewSet

router = DefaultRouter()
router.register(r"equipment", EquipmentViewSet, basename="equipment")
router.register(r"rooms", RoomViewSet, basename="room")

urlpatterns = router.urls 