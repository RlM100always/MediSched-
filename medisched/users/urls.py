# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),


    # dashboards
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    
    # profile editing
    path('patient/profile/edit/', views.edit_profile, name='edit_profile'),


]
