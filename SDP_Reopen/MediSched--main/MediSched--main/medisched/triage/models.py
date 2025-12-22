# triage/models.py - VERIFIED VERSION
from django.db import models
from django.conf import settings
from core.models import Symptom, Department
from doctor.models import Doctor

class PatientSymptomLog(models.Model):
    """Stores symptom check history for patients"""
    URGENCY_LEVELS = (
        ('emergency', 'Emergency - Need immediate care'),
        ('urgent', 'Urgent - See doctor within 24 hours'),
        ('routine', 'Routine - Schedule appointment soon'),
        ('self_care', 'Self-care - Monitor at home'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='symptom_logs')
    symptoms_input = models.TextField(help_text="Patient's description of symptoms")
    selected_symptoms = models.ManyToManyField(Symptom, blank=True)  # This exists
    
    # AI/Rule-based analysis results
    possible_conditions = models.JSONField(default=list, help_text="List of possible conditions")
    recommended_departments = models.ManyToManyField(Department, blank=True)  # This exists
    urgency_level = models.CharField(max_length=20, choices=URGENCY_LEVELS)
    advice = models.TextField(help_text="General advice for patient")
    
    # Doctor recommendation (if any)
    recommended_doctors = models.ManyToManyField(Doctor, blank=True)  # This exists
    confidence_score = models.FloatField(default=0.0, help_text="AI confidence score (0-1)")
    
    # For appointment pre-filling
    appointment_created = models.BooleanField(default=False)
    related_appointment = models.ForeignKey('appointment.Appointment', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Symptom check #{self.id} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']


class SymptomRule(models.Model):
    """Rule-based symptom mapping for triage system"""
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    related_departments = models.ManyToManyField(Department)  # This exists
    urgency_score = models.IntegerField(default=1, help_text="1-10, higher = more urgent")
    common_conditions = models.JSONField(default=list)
    red_flags = models.TextField(blank=True, help_text="Warning signs that need emergency care")
    self_care_tips = models.TextField(blank=True)
    
    def __str__(self):
        return f"Rule for {self.symptom.name}"
    
    class Meta:
        ordering = ['symptom__name']