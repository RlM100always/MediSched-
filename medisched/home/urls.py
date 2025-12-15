# home/urls.py
from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='index'),  # Homepage
    path('department/<int:dept_id>/', views.department_detail, name='department_detail'),
    path("symptom/<int:symptom_id>/", views.symptom_detail, name="symptom_detail"),
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),  # Add this
    path('doctors/', views.all_doctors, name='all_doctors'),   # <-- NEW



    
]