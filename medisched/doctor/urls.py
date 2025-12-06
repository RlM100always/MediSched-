from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('ajax/load-districts/', views.ajax_load_districts, name='ajax_load_districts'),
    path('ajax/load-upazilas/', views.ajax_load_upazilas, name='ajax_load_upazilas'), 
    path('doctor-logout/', views.doctor_logout_view, name='doctor-logout'),
    
    # Profile Management
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('profile/edit/', views.doctor_profile_edit, name='doctor_profile_edit'),
    path('profile/expertise/', views.doctor_expertise_edit, name='expertise_edit'),
    path('profile/expertise/update/', views.update_doctor_expertise, name='expertise_update'),
    
    # Experience
    path('experience/', views.doctor_experience_manage, name='experience_manage'),
    path('experience/edit/<int:exp_id>/', views.doctor_experience_manage, name='experience_edit'),
    path('experience/delete/<int:exp_id>/', views.doctor_experience_delete, name='experience_delete'),
    
    # Appointment Fees
    path('manage-fees/', views.manage_appointment_fees, name='manage_appointment_fees'),
    
    # Add these new URLs for dashboard sidebar
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('patients/', views.doctor_patients, name='doctor_patients'),
    path('reviews/', views.doctor_reviews, name='doctor_reviews'),
    path('analytics/', views.doctor_analytics, name='doctor_analytics'),
]