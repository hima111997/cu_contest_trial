from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='registration_index'),
    path('success/', views.registration_success, name='registration_success'),
    path('validate-email/', views.validate_email, name='validate_email'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]