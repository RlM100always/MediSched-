from django.contrib import admin
from .models import Conversation, Message, Prescription, TestReport, VideoCall, Notification

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['patient__username', 'doctor__user__username']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'message_type', 'is_read', 'created_at']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['content', 'sender__username']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'created_at']
    list_filter = ['created_at']
    search_fields = ['patient__username', 'doctor__user__username', 'diagnosis']

@admin.register(TestReport)
class TestReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'test_name', 'test_date', 'status', 'created_at']
    list_filter = ['status', 'test_date', 'created_at']
    search_fields = ['patient__username', 'test_name', 'lab_name']

@admin.register(VideoCall)
class VideoCallAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'call_type', 'scheduled_time', 'status']
    list_filter = ['call_type', 'status', 'scheduled_time']
    search_fields = ['patient__username', 'doctor__user__username', 'call_id']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']