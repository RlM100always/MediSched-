from django.db import models
from django.conf import settings
from doctor.models import Doctor, DoctorAppointmentFee
from decimal import Decimal
import uuid
from django.utils import timezone
from users.models import CustomUser as User



class Appointment(models.Model):
    APPOINTMENT_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_METHODS = (
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('card', 'Card'),
        ('mobile_banking', 'Mobile Banking'),
    )
    
    CONSULTATION_TYPES = (
        ('instant', 'Instant Video Consultation'),
        ('scheduled', 'Scheduled Appointment'),
    )
    
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    
    # Patient details
    patient_phone = models.CharField(max_length=15)
    patient_name = models.CharField(max_length=100, blank=True)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    patient_gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    
    # Appointment details
    appointment_type = models.CharField(max_length=20, choices=CONSULTATION_TYPES, default='scheduled')
    consultation_type = models.CharField(max_length=20, choices=[('general', 'General'), ('special', 'Special')])
    appointment_date = models.DateTimeField(null=True, blank=True)
    preferred_time = models.CharField(max_length=50, blank=True)
    
    # Completion tracking
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Marked as completed on')
    completed_by_doctor = models.BooleanField(default=False, verbose_name='Marked as completed by doctor')
    cancellation_reason = models.TextField(blank=True, verbose_name='Reason for cancellation')
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Duration tracking
    actual_start_time = models.DateTimeField(null=True, blank=True, verbose_name='Actual consultation start time')
    actual_end_time = models.DateTimeField(null=True, blank=True, verbose_name='Actual consultation end time')
    consultation_duration = models.PositiveIntegerField(default=0, verbose_name='Consultation duration (minutes)')
    
    # Doctor notes
    doctor_notes = models.TextField(blank=True, verbose_name='Doctor notes after consultation')
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True)
    
    # Payment details
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=29.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Payment info
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, unique=True)  # Make unique
    
    # Status
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='pending')
    
    # Additional info
    symptoms = models.TextField(blank=True)
    previous_prescriptions = models.FileField(upload_to='prescriptions/', blank=True, null=True)
    patient_test_reports = models.FileField(upload_to='test_reports/', blank=True, null=True, verbose_name='Test Reports')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Appointment #{self.id} - {self.patient.username}"
    
    def save(self, *args, **kwargs):
        # Generate transaction_id if not provided
        if not self.transaction_id and self.payment_status == 'paid':
            self.transaction_id = f"APPT-{uuid.uuid4().hex[:12].upper()}"
        
        # Calculate total amount if not set
        if not self.total_amount and self.consultation_fee:
            self.vat_amount = self.consultation_fee * Decimal('0.05')
            self.total_amount = self.consultation_fee + self.vat_amount + self.platform_fee
        
        super().save(*args, **kwargs)


class PaymentTransaction(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment_transaction')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    gateway_response = models.JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id}"
    
    def save(self, *args, **kwargs):
        # Generate transaction_id if not provided
        if not self.transaction_id:
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)




class AppointmentRescheduleHistory(models.Model):
    """
    Track appointment rescheduling history
    """
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reschedule_history')
    old_date = models.DateTimeField()
    new_date = models.DateTimeField()
    reason = models.TextField(blank=True)
    rescheduled_by = models.CharField(max_length=20, choices=[('doctor', 'Doctor'), ('patient', 'Patient'), ('system', 'System')])
    rescheduled_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reschedule #{self.id} - Appointment {self.appointment.id}"
    
    class Meta:
        verbose_name_plural = "Appointment reschedule history"
        ordering = ['-rescheduled_at']


class AppointmentNote(models.Model):
    """
    Additional notes for appointments
    """
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notes')
    note_type = models.CharField(max_length=20, choices=[
        ('doctor', 'Doctor Note'),
        ('patient', 'Patient Note'),
        ('system', 'System Note'),
        ('follow_up', 'Follow-up Note')
    ])
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Note #{self.id} for Appointment {self.appointment.id}"
    
    class Meta:
        ordering = ['-created_at']


    

class ExportHistory(models.Model):
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    record_count = models.IntegerField(default=0)
    filters = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.filename} - {self.user.username if self.user else 'Anonymous'}"
    
    class Meta:
        verbose_name_plural = "Export Histories"
        ordering = ['-created_at']
