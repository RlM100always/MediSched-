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


]



