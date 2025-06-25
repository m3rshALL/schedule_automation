from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import EquipmentViewSet, RoomViewSet, RoomExportView, EquipmentExportView

router = DefaultRouter()
router.register(r"equipment", EquipmentViewSet, basename="equipment")
router.register(r"rooms", RoomViewSet, basename="room")

urlpatterns = router.urls + [
    path('export/rooms/', RoomExportView.as_view(), name='export-rooms'),
    path('export/equipment/', EquipmentExportView.as_view(), name='export-equipment'),
] 