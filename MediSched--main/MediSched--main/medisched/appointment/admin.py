from django.contrib import admin
from .models import Appointment, PaymentTransaction

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'consultation_type', 'status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'consultation_type', 'created_at']
    search_fields = ['patient__username', 'doctor__user__username', 'patient_phone', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'appointment', 'amount', 'method', 'status', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['transaction_id', 'appointment__id']
    readonly_fields = ['created_at']