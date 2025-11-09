from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('ajax/load-districts/', views.ajax_load_districts, name='ajax_load_districts'),
    path('ajax/load-upazilas/', views.ajax_load_upazilas, name='ajax_load_upazilas'), 


    # path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    # path('patients/', views.doctor_patients, name='doctor_patients'),
    # path('prescriptions/', views.doctor_prescriptions, name='doctor_prescriptions'),
    # path('payments/', views.doctor_payments, name='doctor_payments'),
    # path('reviews/', views.doctor_reviews, name='doctor_reviews'),
    path('profile/edit/', views.doctor_profile_edit, name='profile_edit'),
]

