# triage/urls.py - FIXED VERSION
from django.urls import path
from . import views

app_name = 'triage'

urlpatterns = [
    # Main symptom checker
    path('check/', views.SymptomCheckerView.as_view(), name='symptom_check'),
    path('analyze/', views.AnalyzeSymptomsView.as_view(), name='analyze_symptoms'),
    
    # Appointment creation - use correct view name
    path('create-appointment/<int:log_id>/', views.CreateAppointmentFromTriageView.as_view(), name='create_appointment_from_triage'),
    path('history/', views.SymptomHistoryView.as_view(), name='symptom_history'),
    # API endpoints
    path('api/symptom-details/', views.GetSymptomDetailsAPI.as_view(), name='api_symptom_details'),
    path('api/quick-triage/', views.QuickTriageAPI.as_view(), name='api_quick_triage'),
]