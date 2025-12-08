from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
import json
from datetime import datetime, timedelta
import hashlib
import time
import uuid

from appointment.models import Appointment
from .models import Conversation, Message, Prescription, TestReport, VideoCall, Notification
from .forms import MessageForm, PrescriptionForm, TestReportForm, VideoCallForm, MedicineForm


@login_required
def chat_home(request):
    """Home page for chats - shows all conversations"""
    if request.user.is_doctor():
        # Doctor sees conversations with all patients
        conversations = Conversation.objects.filter(
            doctor=request.user.doctor_profile,
            is_active=True
        ).select_related('patient', 'appointment')
    else:
        # Patient sees conversations with all doctors
        conversations = Conversation.objects.filter(
            patient=request.user,
            is_active=True
        ).select_related('doctor', 'doctor__user', 'appointment')
    
    context = {
        'conversations': conversations,
    }
    return render(request, 'communication/chat_home.html', context)


@login_required
def chat_detail(request, appointment_id):
    """Chat room for specific appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user is part of this appointment
    if request.user != appointment.patient and request.user != appointment.doctor.user:
        messages.error(request, 'You are not authorized to view this chat.')
        return redirect('communication:chat_home')
    
    # Get or create conversation
    conversation, created = Conversation.objects.get_or_create(
        appointment=appointment,
        defaults={
            'patient': appointment.patient,
            'doctor': appointment.doctor,
        }
    )
    
    # Get messages
    messages_list = Message.objects.filter(conversation=conversation).select_related('sender')
    
    # Mark unread messages as read
    if request.user != conversation.patient:
        unread_messages = messages_list.filter(sender=conversation.patient, is_read=False)
        unread_messages.update(is_read=True)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            
            # Determine message type
            if message.file:
                message.message_type = 'file'
            elif message.image:
                message.message_type = 'image'
            else:
                message.message_type = 'text'
            
            message.save()
            
            # Create notification for receiver
            receiver = conversation.patient if request.user != conversation.patient else conversation.doctor.user
            Notification.objects.create(
                user=receiver,
                notification_type='message',
                title='New Message',
                message=f'New message from {request.user.get_full_name()}',
                related_id=conversation.id
            )
            
            return redirect('communication:chat_detail', appointment_id=appointment_id)
    else:
        form = MessageForm()
    
    # Get prescriptions and test reports for this appointment
    prescriptions = Prescription.objects.filter(appointment=appointment).order_by('-created_at')
    test_reports = TestReport.objects.filter(appointment=appointment).order_by('-created_at')
    
    # Get active video calls (ongoing or scheduled within time window)
    now = timezone.now()
    active_calls = VideoCall.objects.filter(
        appointment=appointment,
        status__in=['scheduled', 'ongoing'],
        scheduled_time__gte=now - timedelta(hours=2),
        scheduled_time__lte=now + timedelta(hours=24)
    ).order_by('-scheduled_time')
    
    # Get all video calls for history
    video_calls = VideoCall.objects.filter(appointment=appointment).order_by('-scheduled_time')
    
    context = {
        'appointment': appointment,
        'conversation': conversation,
        'messages': messages_list,
        'form': form,
        'prescriptions': prescriptions,
        'test_reports': test_reports,
        'video_calls': video_calls,
        'active_calls': active_calls,
        'now': now,
    }
    return render(request, 'communication/chat_detail.html', context)


@login_required
def create_prescription(request, appointment_id):
    """Doctor creates prescription"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Only doctor can create prescription
    if not request.user.is_doctor() or request.user.doctor_profile != appointment.doctor:
        messages.error(request, 'Only the doctor can create prescriptions.')
        return redirect('communication:chat_detail', appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.doctor = appointment.doctor
            prescription.patient = appointment.patient
            prescription.save()
            
            # Create a message for the prescription
            Message.objects.create(
                conversation=appointment.conversation,
                sender=request.user,
                message_type='prescription',
                content=f'New prescription created by Dr. {request.user.get_full_name()}'
            )
            
            # Create notification
            Notification.objects.create(
                user=appointment.patient,
                notification_type='prescription',
                title='New Prescription',
                message=f'Dr. {request.user.get_full_name()} has sent you a new prescription',
                related_id=prescription.id
            )
            
            messages.success(request, 'Prescription created successfully.')
            return redirect('communication:chat_detail', appointment_id=appointment_id)
    else:
        form = PrescriptionForm()
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'communication/create_prescription.html', context)


@login_required
def upload_test_report(request, appointment_id):
    """Patient uploads test report"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Only patient can upload test reports
    if request.user != appointment.patient:
        messages.error(request, 'Only the patient can upload test reports.')
        return redirect('communication:chat_detail', appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = TestReportForm(request.POST, request.FILES)
        if form.is_valid():
            test_report = form.save(commit=False)
            test_report.appointment = appointment
            test_report.patient = request.user
            test_report.status = 'submitted'
            test_report.save()
            
            # Create a message for the test report
            Message.objects.create(
                conversation=appointment.conversation,
                sender=request.user,
                message_type='test_report',
                content=f'New test report uploaded: {test_report.test_name}'
            )
            
            # Create notification for doctor
            Notification.objects.create(
                user=appointment.doctor.user,
                notification_type='test_report',
                title='Test Report Uploaded',
                message=f'{request.user.get_full_name()} has uploaded a test report',
                related_id=test_report.id
            )
            
            messages.success(request, 'Test report uploaded successfully.')
            return redirect('communication:chat_detail', appointment_id=appointment_id)
    else:
        form = TestReportForm()
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'communication/upload_test_report.html', context)


@login_required
def schedule_video_call(request, appointment_id):
    """Schedule video/audio call"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Both doctor and patient can schedule calls
    if request.user not in [appointment.patient, appointment.doctor.user]:
        messages.error(request, 'You are not authorized to schedule calls for this appointment.')
        return redirect('communication:chat_detail', appointment_id=appointment_id)
    
    if request.method == 'POST':
        form = VideoCallForm(request.POST)
        if form.is_valid():
            video_call = form.save(commit=False)
            video_call.appointment = appointment
            video_call.doctor = appointment.doctor
            video_call.patient = appointment.patient
            
            # Generate unique call ID
            video_call.call_id = str(uuid.uuid4())[:12]
            
            # Set status
            video_call.status = 'scheduled'
            
            video_call.save()
            
            # Create message
            Message.objects.create(
                conversation=appointment.conversation,
                sender=request.user,
                message_type='video_call',
                content=f'{video_call.call_type.title()} call scheduled for {video_call.scheduled_time.strftime("%Y-%m-%d %I:%M %p")}'
            )
            
            # Create notification for both parties
            receiver = appointment.patient if request.user != appointment.patient else appointment.doctor.user
            Notification.objects.create(
                user=receiver,
                notification_type='video_call',
                title=f'{video_call.call_type.title()} Call Scheduled',
                message=f'{request.user.get_full_name()} scheduled a {video_call.call_type} call for {video_call.scheduled_time.strftime("%I:%M %p, %b %d")}',
                related_id=video_call.id
            )
            
            messages.success(request, f'{video_call.call_type.title()} call scheduled successfully.')
            return redirect('communication:chat_detail', appointment_id=appointment_id)
    else:
        form = VideoCallForm(initial={
            'scheduled_time': timezone.now() + timedelta(minutes=30)
        })
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'communication/schedule_video_call.html', context)


@login_required
def start_or_join_video_call(request, appointment_id):
    """Start or join existing video call"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check authorization
    if request.user not in [appointment.patient, appointment.doctor.user]:
        messages.error(request, 'You are not authorized to start/join video call.')
        return redirect('communication:chat_detail', appointment_id=appointment_id)
    
    # Check for existing ongoing or scheduled call
    now = timezone.now()
    
    # First, check for ongoing calls
    ongoing_call = VideoCall.objects.filter(
        appointment=appointment,
        status='ongoing'
    ).first()
    
    if ongoing_call:
        return redirect('communication:video_call_room', call_id=ongoing_call.call_id)
    
    # Check for scheduled calls that can be joined now
    scheduled_calls = VideoCall.objects.filter(
        appointment=appointment,
        status='scheduled'
    ).order_by('scheduled_time')
    
    for video_call in scheduled_calls:
        time_difference = (video_call.scheduled_time - now).total_seconds() / 60  # minutes
        
        # Check if user can join this call
        can_join_now = False
        
        if request.user == appointment.doctor.user:
            # Doctor can join 15 minutes before to 2 hours after scheduled time
            can_join_now = time_difference <= 120 and time_difference >= -15
        else:
            # Patient can join 5 minutes before to 2 hours after scheduled time
            can_join_now = time_difference <= 120 and time_difference >= -5
        
        if can_join_now:
            # Update call to ongoing
            video_call.status = 'ongoing'
            video_call.actual_start_time = now
            video_call.save()
            
            # Create notification
            receiver = appointment.patient if request.user != appointment.patient else appointment.doctor.user
            Notification.objects.create(
                user=receiver,
                notification_type='video_call',
                title='Video Call Started',
                message=f'{request.user.get_full_name()} has started the video call',
                related_id=video_call.id
            )
            
            return redirect('communication:video_call_room', call_id=video_call.call_id)
    
    # No active call that can be joined, redirect to schedule
    messages.info(request, 'No active video call found. Please schedule a new call.')
    return redirect('communication:schedule_video_call', appointment_id=appointment_id)

# communication/views.py - video_call_room function
@login_required
def video_call_room(request, call_id):
    """Video/audio call room"""
    try:
        video_call = VideoCall.objects.get(call_id=call_id)
    except VideoCall.DoesNotExist:
        messages.error(request, 'Video call not found.')
        return redirect('communication:chat_home')
    
    # Check authorization
    if request.user not in [video_call.patient, video_call.doctor.user]:
        messages.error(request, 'You are not authorized to join this call.')
        return redirect('communication:chat_home')
    
    # Check if call is still valid
    now = timezone.now()
    
    if video_call.status == 'completed':
        messages.warning(request, 'This video call has already ended.')
        return redirect('communication:chat_detail', appointment_id=video_call.appointment.id)
    
    if video_call.status == 'cancelled':
        messages.warning(request, 'This video call has been cancelled.')
        return redirect('communication:chat_detail', appointment_id=video_call.appointment.id)
    
    # If call is scheduled but time hasn't come yet
    if video_call.status == 'scheduled':
        time_difference = (video_call.scheduled_time - now).total_seconds() / 60
        
        # Doctor can start 15 minutes early, patient 5 minutes early
        if request.user == video_call.doctor.user:
            if time_difference > 15:  # More than 15 minutes before
                messages.warning(
                    request, 
                    f"Call is scheduled for {video_call.scheduled_time.strftime('%I:%M %p')}. "
                    f"You can start the call 15 minutes before the scheduled time."
                )
                return redirect('communication:chat_detail', appointment_id=video_call.appointment.id)
        else:
            if time_difference > 5:  # More than 5 minutes before
                messages.warning(
                    request, 
                    f"Call is scheduled for {video_call.scheduled_time.strftime('%I:%M %p')}. "
                    f"You can join the call 5 minutes before the scheduled time."
                )
                return redirect('communication:chat_detail', appointment_id=video_call.appointment.id)
        
        # Update status to ongoing if it's time
        video_call.status = 'ongoing'
        video_call.actual_start_time = now
        video_call.save()
    
    # Get Agora credentials
    AGORA_APP_ID = getattr(settings, 'AGORA_APP_ID', '')
    AGORA_APP_CERTIFICATE = getattr(settings, 'AGORA_APP_CERTIFICATE', '')
    
    # Check if Agora is configured
    if not AGORA_APP_ID or not AGORA_APP_CERTIFICATE:
        messages.error(request, 'Video call service is not configured. Please contact administrator.')
        return redirect('communication:chat_detail', appointment_id=video_call.appointment.id)
    
    # Generate channel name
    channel_name = f"medisched_{call_id}"
    
    # Generate user ID
    user_id = request.user.id
    
    # Generate tokens
    try:
        from .agora_utils import generate_rtc_token, generate_rtm_token
        
        rtc_token = generate_rtc_token(
            channel_name=channel_name,
            uid=user_id,
            expire_time=3600
        )
        
        rtm_token = generate_rtm_token(
            uid=user_id,
            expire_time=3600
        )
        
        # Check if tokens were generated
        if not rtc_token:
            messages.warning(request, 'Unable to generate video call token. Please try again.')
            rtc_token = None  # Set to None for testing mode
            
        if not rtm_token:
            rtm_token = None
            
    except ImportError as e:
        print(f"Error importing agora_utils: {e}")
        messages.error(request, 'Video call service configuration error.')
        return redirect('communication:chat_detail', appointment_id=video_call.appointment.id)
    
    except Exception as e:
        print(f"Error generating tokens: {e}")
        rtc_token = None
        rtm_token = None
    
    # Determine template based on user type
    is_doctor = False
    if hasattr(request.user, 'is_doctor'):
        is_doctor = request.user.is_doctor()
    elif hasattr(request.user, 'doctor_profile'):
        is_doctor = True
    
    if is_doctor:
        template_name = 'communication/doctor_video_call_room.html'
    else:
        template_name = 'communication/patient_video_call_room.html'
    
    context = {
        'video_call': video_call,
        'is_doctor': is_doctor,
        'agora_app_id': AGORA_APP_ID,
        'channel_name': channel_name,
        'user_id': user_id,
        'rtc_token': rtc_token,  # This should be None if generation failed
        'rtm_token': rtm_token,
        'now': now,
    }
    return render(request, template_name, context)


@login_required
def end_video_call(request, call_id):
    """End video call"""
    video_call = get_object_or_404(VideoCall, call_id=call_id)
    
    if request.user not in [video_call.patient, video_call.doctor.user]:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    video_call.status = 'completed'
    video_call.actual_end_time = timezone.now()
    
    # Calculate duration
    if video_call.actual_start_time:
        duration_seconds = (video_call.actual_end_time - video_call.actual_start_time).seconds
        video_call.duration = duration_seconds // 60  # Convert to minutes
    
    video_call.save()
    
    # Create notification
    receiver = video_call.patient if request.user != video_call.patient else video_call.doctor.user
    Notification.objects.create(
        user=receiver,
        notification_type='video_call',
        title='Video Call Ended',
        message=f'{request.user.get_full_name()} has ended the video call',
        related_id=video_call.id
    )
    
    # Create chat message
    Message.objects.create(
        conversation=video_call.appointment.conversation,
        sender=request.user,
        message_type='video_call',
        content=f'Video call ended. Duration: {video_call.duration} minutes.'
    )
    
    return JsonResponse({'success': True})


@login_required
def get_messages(request, appointment_id):
    """AJAX endpoint to get messages"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check authorization
    if request.user not in [appointment.patient, appointment.doctor.user]:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    conversation = get_object_or_404(Conversation, appointment=appointment)
    messages = Message.objects.filter(conversation=conversation).order_by('created_at')
    
    data = []
    for msg in messages:
        data.append({
            'id': msg.id,
            'sender': msg.sender.username,
            'sender_name': msg.sender.get_full_name() or msg.sender.username,
            'message_type': msg.message_type,
            'content': msg.content,
            'file_url': msg.file.url if msg.file else None,
            'image_url': msg.image.url if msg.image else None,
            'is_read': msg.is_read,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_own': msg.sender == request.user,
        })
    
    return JsonResponse({'messages': data})


@login_required
def get_notifications(request):
    """Get unread notifications"""
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:10]
    
    data = []
    for notif in notifications:
        data.append({
            'id': notif.id,
            'type': notif.notification_type,
            'title': notif.title,
            'message': notif.message,
            'created_at': notif.created_at.strftime('%H:%M'),
        })
    
    return JsonResponse({'notifications': data})


@login_required
def mark_notification_read(request, notification_id):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'success': True})


@login_required
def check_call_status(request, appointment_id):
    """Check if there's an active video call"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.user not in [appointment.patient, appointment.doctor.user]:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    now = timezone.now()
    
    # Check for ongoing call
    ongoing_call = VideoCall.objects.filter(
        appointment=appointment,
        status='ongoing'
    ).first()
    
    if ongoing_call:
        return JsonResponse({
            'has_active_call': True,
            'call_id': ongoing_call.call_id,
            'status': 'ongoing',
            'started_at': ongoing_call.actual_start_time.isoformat() if ongoing_call.actual_start_time else None,
        })
    
    # Check for scheduled call that can be joined
    scheduled_call = VideoCall.objects.filter(
        appointment=appointment,
        status='scheduled'
    ).order_by('scheduled_time').first()
    
    if scheduled_call:
        time_difference = (scheduled_call.scheduled_time - now).total_seconds() / 60
        
        can_join = False
        if request.user == appointment.doctor.user:
            can_join = time_difference <= 120 and time_difference >= -15
        else:
            can_join = time_difference <= 120 and time_difference >= -5
        
        return JsonResponse({
            'has_active_call': can_join,
            'call_id': scheduled_call.call_id if can_join else None,
            'status': 'scheduled',
            'scheduled_time': scheduled_call.scheduled_time.isoformat(),
            'time_until': time_difference,
            'can_join': can_join,
        })
    
    return JsonResponse({
        'has_active_call': False,
        'call_id': None,
        'status': 'none',
    })
    


@login_required
def start_immediate_video_call(request, appointment_id):
    """Start immediate video call without scheduling"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Both doctor and patient can start immediate calls
    if request.user not in [appointment.patient, appointment.doctor.user]:
        messages.error(request, 'You are not authorized to start video call.')
        return redirect('communication:chat_detail', appointment_id=appointment_id)
    
    # Create immediate video call
    video_call = VideoCall.objects.create(
        appointment=appointment,
        doctor=appointment.doctor,
        patient=appointment.patient,
        call_id=str(uuid.uuid4())[:12],
        call_type='video',
        status='ongoing',
        scheduled_time=timezone.now(),
        actual_start_time=timezone.now()
    )
    
    # Create notification
    receiver = appointment.patient if request.user != appointment.patient else appointment.doctor.user
    Notification.objects.create(
        user=receiver,
        notification_type='video_call',
        title='Video Call Request',
        message=f'{request.user.get_full_name()} wants to start a video call',
        related_id=video_call.id
    )
    
    # Create chat message
    Message.objects.create(
        conversation=appointment.conversation,
        sender=request.user,
        message_type='video_call',
        content=f'Started an immediate video call'
    )
    
    messages.success(request, 'Video call started! Waiting for other participant...')
    return redirect('communication:video_call_room', call_id=video_call.call_id)    