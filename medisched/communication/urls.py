from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    # Chat
    path('', views.chat_home, name='chat_home'),
    path('chat/<int:appointment_id>/', views.chat_detail, name='chat_detail'),
    path('api/messages/<int:appointment_id>/', views.get_messages, name='get_messages'),
    
    # Prescriptions
    path('prescription/create/<int:appointment_id>/', views.create_prescription, name='create_prescription'),
    
    # Test Reports
    path('test-report/upload/<int:appointment_id>/', views.upload_test_report, name='upload_test_report'),
    
    # Video Calls
    path('video-call/schedule/<int:appointment_id>/', views.schedule_video_call, name='schedule_video_call'),
    path('video-call/<str:call_id>/', views.video_call_room, name='video_call_room'),
    path('video-call/<str:call_id>/end/', views.end_video_call, name='end_video_call'),
    
    # Notifications
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
]