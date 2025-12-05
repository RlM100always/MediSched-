from django.db import models
from django.conf import settings
from doctor.models import Doctor, DoctorAppointmentFee
from decimal import Decimal
import uuid

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
    
    # Payment details
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2, default=29.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Payment info
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    
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
        # Calculate VAT (5%)
        if self.consultation_fee and not self.vat_amount:
            self.vat_amount = self.consultation_fee * Decimal('0.05')
        
        # Ensure all values are Decimal
        self.platform_fee = Decimal('29.00')
        
        # Calculate total amount - convert everything to Decimal
        self.total_amount = (
            Decimal(str(self.consultation_fee)) + 
            Decimal(str(self.vat_amount)) + 
            Decimal(str(self.platform_fee))
        )
        
        # Set patient name if not provided
        if not self.patient_name and self.patient:
            self.patient_name = self.patient.get_full_name() or self.patient.username
        
        # Generate transaction ID if not exists
        if not self.transaction_id:
            self.transaction_id = f"TXN{str(uuid.uuid4())[:8].upper()}"
        
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