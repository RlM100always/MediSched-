from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    # Chat
    path('', views.chat_home, name='chat_home'),
    path('chat/<int:appointment_id>/', views.chat_detail, name='chat_detail'),
    path('api/messages/<int:appointment_id>/', views.get_messages, name='get_messages'),
    
    # Video Calls
    path('video-call/schedule/<int:appointment_id>/', views.schedule_video_call, name='schedule_video_call'),
    path('video-call/start/<int:appointment_id>/', views.start_or_join_video_call, name='start_video_call'),
    path('video-call/immediate/<int:appointment_id>/', views.start_immediate_video_call, name='immediate_video_call'),  # NEW
    path('video-call/<str:call_id>/', views.video_call_room, name='video_call_room'),
    path('video-call/<str:call_id>/end/', views.end_video_call, name='end_video_call'),
    path('api/check-call-status/<int:appointment_id>/', views.check_call_status, name='check_call_status'),
    
    # Prescriptions
    path('prescription/create/<int:appointment_id>/', views.create_prescription, name='create_prescription'),
    
    # Test Reports
    path('test-report/upload/<int:appointment_id>/', views.upload_test_report, name='upload_test_report'),
    
    # Notifications
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
]