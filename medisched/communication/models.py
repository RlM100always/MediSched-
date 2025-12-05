from django.db import models
from django.conf import settings
from appointment.models import Appointment
from doctor.models import Doctor
from decimal import Decimal

class Conversation(models.Model):
    """Doctor-Patient conversation thread"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='conversation')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_conversations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_conversations')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Conversation: Dr. {self.doctor.user.username} - {self.patient.username}"
    
    class Meta:
        ordering = ['-updated_at']


class Message(models.Model):
    """Individual messages in a conversation"""
    MESSAGE_TYPES = [
        ('text', 'Text Message'),
        ('image', 'Image'),
        ('file', 'File'),
        ('prescription', 'Prescription'),
        ('test_report', 'Test Report'),
        ('audio', 'Audio Message'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='communication/files/', blank=True, null=True)
    image = models.ImageField(upload_to='communication/images/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50] if self.content else self.message_type}"
    
    class Meta:
        ordering = ['created_at']


class Prescription(models.Model):
    """Doctor's prescription for patient"""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Prescription details
    diagnosis = models.TextField()
    advice = models.TextField(blank=True, null=True)
    follow_up_date = models.DateField(blank=True, null=True)
    
    # Prescribed medicines
    medicines = models.JSONField(default=list)  # Format: [{"name": "", "dosage": "", "duration": "", "instructions": ""}]
    
    # Suggested tests
    suggested_tests = models.JSONField(default=list)  # Format: [{"test_name": "", "instructions": ""}]
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Prescription #{self.id} - Dr. {self.doctor.user.username} for {self.patient.username}"


class TestReport(models.Model):
    """Patient's medical test reports"""
    REPORT_STATUS = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed by Doctor'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='test_reports')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Test details
    test_name = models.CharField(max_length=255)
    test_date = models.DateField()
    lab_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Report files
    report_file = models.FileField(upload_to='test_reports/')
    thumbnail = models.ImageField(upload_to='test_report_thumbnails/', blank=True, null=True)
    
    # Results
    findings = models.TextField(blank=True, null=True)
    doctor_notes = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Test Report: {self.test_name} - {self.patient.username}"


class VideoCall(models.Model):
    """Video/Audio call scheduling and recording"""
    CALL_TYPES = [
        ('video', 'Video Call'),
        ('audio', 'Audio Call'),
    ]
    
    CALL_STATUS = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('missed', 'Missed'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='video_calls')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Call details
    call_type = models.CharField(max_length=10, choices=CALL_TYPES, default='video')
    scheduled_time = models.DateTimeField()
    actual_start_time = models.DateTimeField(blank=True, null=True)
    actual_end_time = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(default=0)  # in minutes
    
    # Call metadata
    call_id = models.CharField(max_length=100, unique=True)  # For WebRTC or Zoom/Skype
    meeting_url = models.URLField(blank=True, null=True)
    meeting_password = models.CharField(max_length=100, blank=True, null=True)
    
    # Recording (if allowed)
    recording_url = models.URLField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=CALL_STATUS, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.call_type.title()} Call - Dr. {self.doctor.user.username} & {self.patient.username}"
    
    def save(self, *args, **kwargs):
        if not self.call_id:
            import uuid
            self.call_id = f"call_{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)


class Notification(models.Model):
    """Real-time notifications for users"""
    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('prescription', 'New Prescription'),
        ('test_report', 'Test Report Uploaded'),
        ('video_call', 'Video Call Scheduled'),
        ('appointment', 'Appointment Reminder'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_id = models.IntegerField(blank=True, null=True)  # ID of related object (appointment, message, etc.)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"
    
    class Meta:
        ordering = ['-created_at']