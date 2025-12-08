from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    # Dashboard and Profile
    path('dashboard/', views.doctor_dashboard, name='dashboard'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('profile/edit/', views.doctor_profile_edit, name='doctor_profile_edit'),
    path('profile/expertise/', views.doctor_expertise_edit, name='expertise_edit'),
    path('profile/expertise/update/', views.update_doctor_expertise, name='expertise_update'),
    path('doctor-logout/', views.doctor_logout_view, name='doctor-logout'),
    
    # Experience Management
    path('experience/', views.doctor_experience_manage, name='experience_manage'),
    path('experience/edit/<int:exp_id>/', views.doctor_experience_manage, name='experience_edit'),
    path('experience/delete/<int:exp_id>/', views.doctor_experience_delete, name='experience_delete'),
    
    # Fees Management
    path('manage-fees/', views.manage_appointment_fees, name='manage_appointment_fees'),
    
    # AJAX helpers
    path('ajax/load-districts/', views.ajax_load_districts, name='ajax_load_districts'),
    path('ajax/load-upazilas/', views.ajax_load_upazilas, name='ajax_load_upazilas'),
    
    # Appointments Management
    # Appointments Management
    path('appointments/', views.doctor_appointments, name='appointments'),
    path('appointment/<int:appointment_id>/mark-complete/', 
         views.mark_appointment_complete, 
         name='mark_appointment_complete'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),

    path('appointments/<int:appointment_id>/update-status/', views.update_appointment_status, name='update_appointment_status'),
   


    
    # Analytics
    path('appointments/analytics/', views.appointment_analytics, name='appointment_analytics'),
    path('appointments/export/', views.export_appointments, name='export_appointments'),
    
    # Communication (Chat, Prescription, Video Calls)
    path('chat/', views.doctor_chat_home, name='chat_home'),
    path('chat/<int:appointment_id>/', views.doctor_chat_detail, name='chat_detail'),
    path('chat/<int:appointment_id>/send/', views.send_message, name='send_message'),
    path('api/messages/<int:appointment_id>/', views.get_messages, name='get_messages'),
    
    # Prescriptions
    path('prescription/create/<int:appointment_id>/', views.create_prescription_view, name='create_prescription'),
    path('prescription/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
    
    # Test Reports
    path('test-report/<int:report_id>/review/', views.review_test_report, name='review_test_report'),
    
    # Video Calls
    path('video-calls/', views.doctor_video_calls, name='video_calls'),
    path('video-call/schedule/<int:appointment_id>/', views.schedule_video_call_view, name='schedule_video_call'),
    path('video-call/<str:call_id>/', views.video_call_room_doctor, name='video_call_room'),
    path('video-call/<str:call_id>/start/', views.start_video_call, name='start_video_call'),
    path('video-call/<str:call_id>/end/', views.end_video_call_doctor, name='end_video_call'),
    path('video-call/<str:call_id>/cancel/', views.cancel_video_call, name='cancel_video_call'),
    
    # Notifications
    path('api/notifications/', views.get_doctor_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read_doctor, name='mark_notification_read'),
    path('api/notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]