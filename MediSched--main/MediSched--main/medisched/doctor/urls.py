# doctor/urls.py
from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    
    # Profile Management
    path('profile/', views.doctor_profile, name='profile'),
    path('profile/edit/', views.doctor_profile_edit, name='profile_edit'),
    path('expertise/edit/', views.doctor_expertise_edit, name='expertise_edit'),
    path('expertise/update/', views.update_doctor_expertise, name='update_expertise'),
    path('experience/manage/', views.doctor_experience_manage, name='experience_manage'),
    path('experience/manage/<int:exp_id>/', views.doctor_experience_manage, name='experience_manage_edit'),
    path('experience/delete/<int:exp_id>/', views.doctor_experience_delete, name='experience_delete'),
    
    # Appointments
    path('appointments/', views.doctor_appointments, name='appointments'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:appointment_id>/complete/', views.mark_appointment_complete, name='mark_appointment_complete'),
    path('appointments/<int:appointment_id>/status/', views.update_appointment_status, name='update_appointment_status'),
    path('appointments/analytics/', views.appointment_analytics, name='appointment_analytics'),
    path('appointments/export/', views.export_appointments, name='export_appointments'),
    
    # Fees Management
    path('fees/manage/', views.manage_appointment_fees, name='manage_appointment_fees'),
    
    # Communication
    path('chat/', views.doctor_chat_home, name='chat_home'),
    path('chat/<int:appointment_id>/', views.doctor_chat_detail, name='chat_detail'),
    path('chat/send/<int:appointment_id>/', views.send_message, name='send_message'),
    path('chat/messages/<int:appointment_id>/', views.get_messages, name='get_messages'),
    
    # Video Calls
    path('video-calls/', views.doctor_video_calls, name='video_calls'),
    path('video-call/schedule/<int:appointment_id>/', views.schedule_video_call_view, name='schedule_video_call'),
    path('video-call/room/<str:call_id>/', views.video_call_room_doctor, name='video_call_room'),
    path('video-call/start/<str:call_id>/', views.start_video_call, name='start_video_call'),
    path('video-call/end/<str:call_id>/', views.end_video_call_doctor, name='end_video_call'),
    path('video-call/cancel/<str:call_id>/', views.cancel_video_call, name='cancel_video_call'),
    
    # Prescriptions
    path('prescription/create/<int:appointment_id>/', views.create_prescription_view, name='create_prescription'),
    path('prescription/view/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
    
    # Test Reports
    path('test-report/review/<int:report_id>/', views.review_test_report, name='review_test_report'),
    
    # Notifications
    path('notifications/', views.get_doctor_notifications, name='notifications'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read_doctor, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # AJAX endpoints
    path('ajax/load-districts/', views.ajax_load_districts, name='ajax_load_districts'),
    path('ajax/load-upazilas/', views.ajax_load_upazilas, name='ajax_load_upazilas'),
    
    # Logout
    path('logout/', views.doctor_logout_view, name='logout'),
]