from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    path('profile/edit/', views.doctor_profile_edit, name='profile_edit'),

    
]
