from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
import json
from datetime import datetime

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
    video_calls = VideoCall.objects.filter(appointment=appointment).order_by('-scheduled_time')
    
    context = {
        'appointment': appointment,
        'conversation': conversation,
        'messages': messages_list,
        'form': form,
        'prescriptions': prescriptions,
        'test_reports': test_reports,
        'video_calls': video_calls,
        'now': timezone.now(),
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
            
            # Generate meeting URL (simplified - in real app, integrate with Zoom/Google Meet)
            import uuid
            meeting_id = str(uuid.uuid4())[:8]
            video_call.meeting_url = f"/communication/video-call/{meeting_id}/"
            video_call.meeting_password = str(uuid.uuid4())[:6]
            
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
                message=f'{request.user.get_full_name()} scheduled a {video_call.call_type} call',
                related_id=video_call.id
            )
            
            messages.success(request, f'{video_call.call_type.title()} call scheduled successfully.')
            return redirect('communication:chat_detail', appointment_id=appointment_id)
    else:
        form = VideoCallForm()
    
    context = {
        'appointment': appointment,
        'form': form,
    }
    return render(request, 'communication/schedule_video_call.html', context)


@login_required
def video_call_room(request, call_id):
    """Video/audio call room"""
    video_call = get_object_or_404(VideoCall, call_id=call_id)
    
    # Check authorization
    if request.user not in [video_call.patient, video_call.doctor.user]:
        messages.error(request, 'You are not authorized to join this call.')
        return redirect('communication:chat_home')
    
    # Update call status if starting
    if request.GET.get('action') == 'start' and video_call.status == 'scheduled':
        video_call.status = 'ongoing'
        video_call.actual_start_time = timezone.now()
        video_call.save()
    
    context = {
        'video_call': video_call,
        'is_doctor': request.user == video_call.doctor.user,
    }
    return render(request, 'communication/video_call_room.html', context)


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
        duration = (video_call.actual_end_time - video_call.actual_start_time).seconds // 60
        video_call.duration = duration
    
    video_call.save()
    
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