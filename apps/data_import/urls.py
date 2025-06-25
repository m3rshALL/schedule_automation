from django.urls import path
from .views import StudentGroupImportView

urlpatterns = [
    path('groups/', StudentGroupImportView.as_view(), name='import-student-groups'),
] 