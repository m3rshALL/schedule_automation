from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import EquipmentViewSet, RoomViewSet, RoomExportView, EquipmentExportView, RoomAsyncExportView, RoomAsyncExportStatusView, EquipmentAsyncExportView, EquipmentAsyncExportStatusView

router = DefaultRouter()
router.register(r"equipment", EquipmentViewSet, basename="equipment")
router.register(r"rooms", RoomViewSet, basename="room")

urlpatterns = router.urls + [
    path('export/rooms/', RoomExportView.as_view(), name='export-rooms'),
    path('export/equipment/', EquipmentExportView.as_view(), name='export-equipment'),
    path('export/rooms/async/', RoomAsyncExportView.as_view(), name='export-rooms-async'),
    path('export/rooms/async/status/', RoomAsyncExportStatusView.as_view(), name='export-rooms-async-status'),
    path('export/equipment/async/', EquipmentAsyncExportView.as_view(), name='export-equipment-async'),
    path('export/equipment/async/status/', EquipmentAsyncExportStatusView.as_view(), name='export-equipment-async-status'),
] 