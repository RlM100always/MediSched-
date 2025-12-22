from django.urls import path
from . import views



urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),

    # Division CRUD
    path('divisions/', views.division_list, name='division_list'),
    path('divisions/add/', views.add_division, name='add_division'),
    path('divisions/delete/<int:id>/', views.delete_division, name='delete_division'),
    path('divisions/edit/<int:id>/', views.edit_division, name='edit_division'),  # ✅ Add this


    # District CRUD
    path('districts/', views.district_list, name='district_list'),
    path('districts/add/', views.add_district, name='add_district'),
    path('districts/delete/<int:id>/', views.delete_district, name='delete_district'),
    path('districts/edit/<int:id>/', views.edit_district, name='edit_district'),  # ✅ Add this


    # Upazila CRUD
    path('upazilas/', views.upazila_list, name='upazila_list'),
    path('upazilas/add/', views.add_upazila, name='add_upazila'),
    path('upazilas/delete/<int:id>/', views.delete_upazila, name='delete_upazila'),
    path('upazilas/edit/<int:id>/', views.edit_upazila, name='edit_upazila'),


    # Department CRUD
path('departments/', views.department_list, name='department_list'),
path('departments/add/', views.add_department, name='add_department'),
path('departments/edit/<int:id>/', views.edit_department, name='edit_department'),  # <-- Edit
path('departments/delete/<int:id>/', views.delete_department, name='delete_department'),

# Symptom CRUD
path('symptoms/', views.symptom_list, name='symptom_list'),
path('symptoms/add/', views.add_symptom, name='add_symptom'),
path('symptoms/edit/<int:id>/', views.edit_symptom, name='edit_symptom'),  # <-- Edit
path('symptoms/delete/<int:id>/', views.delete_symptom, name='delete_symptom'),

    
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('payments/', views.payment_list, name='payment_list'),
    path('logout/', views.user_logout, name='logout'),



    # Doctor URLs
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/create/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:pk>/edit/', views.doctor_edit, name='doctor_edit'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    path('doctors/verify/<int:pk>/', views.doctor_verify, name='doctor_verify'),
    path('doctors/unverify/<int:pk>/', views.doctor_unverify, name='doctor_unverify'),
    
    
    # Appointment URLs
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:appointment_id>/update-status/', views.appointment_update_status, name='appointment_update_status'),
    path('appointments/<int:appointment_id>/update-payment/', views.appointment_update_payment, name='appointment_update_payment'),
    path('appointments/<int:appointment_id>/add-note/', views.appointment_add_note, name='appointment_add_note'),
    path('appointments/note/<int:note_id>/delete/', views.appointment_delete_note, name='appointment_delete_note'),
    path('appointments/statistics/', views.appointment_statistics, name='appointment_statistics'),
    path('appointments/export/', views.appointment_export, name='appointment_export'),


]



