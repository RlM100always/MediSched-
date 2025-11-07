# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('ajax/signup/', views.ajax_signup, name='signup_ajax'),
    path('ajax/signin/', views.ajax_signin, name='signin_ajax'),
    path('ajax/logout/', views.ajax_logout, name='logout_ajax'),

    # dashboards
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('admin/dashboard/', views.platform_admin_dashboard, name='platform_admin_dashboard'),
]
