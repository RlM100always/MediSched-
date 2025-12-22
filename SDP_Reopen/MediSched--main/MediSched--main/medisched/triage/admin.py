# triage/admin.py - FIXED VERSION
from django.contrib import admin
from .models import PatientSymptomLog, SymptomRule

@admin.register(PatientSymptomLog)
class PatientSymptomLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'urgency_level', 'confidence_score', 'appointment_created', 'created_at']
    list_filter = ['urgency_level', 'appointment_created', 'created_at']
    search_fields = ['user__username', 'user__email', 'symptoms_input']
    readonly_fields = ['created_at', 'updated_at']
    
    # FIX: Use correct field names from your models.py
    # Check what fields you have in PatientSymptomLog model
    filter_horizontal = ['selected_symptoms']  # Only include fields that exist
    
    # If you want to show departments and doctors in admin, use raw_id_fields instead
    raw_id_fields = ['recommended_doctors']  # Use this for ForeignKey/ManyToMany
    
    def get_queryset(self, request):
        """Optimize queries"""
        return super().get_queryset(request).select_related('user').prefetch_related('selected_symptoms')


@admin.register(SymptomRule)
class SymptomRuleAdmin(admin.ModelAdmin):
    list_display = ['symptom', 'urgency_score', 'get_related_departments']
    list_filter = ['urgency_score']
    search_fields = ['symptom__name', 'red_flags']
    
    # FIX: Use correct field name
    filter_horizontal = ['related_departments']  # This should exist in SymptomRule model
    
    def get_related_departments(self, obj):
        return ", ".join([dept.name for dept in obj.related_departments.all()[:3]])
    get_related_departments.short_description = 'Related Departments'