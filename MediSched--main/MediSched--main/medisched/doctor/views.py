from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse,HttpResponseForbidden
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control
from django.utils import timezone
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.paginator import Paginator
from django.conf import settings
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt 
from django.urls import reverse            


import json
from datetime import datetime, timedelta

from appointment.models import Appointment,PaymentTransaction,AppointmentNote
from communication.models import Conversation, Message, Prescription, TestReport, VideoCall, Notification
from doctor.models import Doctor
import uuid


from adminapp.models import Division, District, Upazila, Department, Symptom
from .models import (
    Doctor, 
    DoctorExperience, 
    DoctorAppointmentFee,
    DoctorSpecializationDepartment,
    DoctorSpecializationSymptom
)
from appointment.models import Appointment
from users.models import CustomUser


@login_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True, max_age=0)
def doctor_dashboard(request):
    """Doctor dashboard with proper data retrieval"""
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, "You don't have a doctor profile.")
        return redirect('/')
    
    doctor = request.user.doctor_profile
    now = timezone.now()
    today = now.date()
    
    # Get today's datetime range (start and end of day)
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    # 1. UPCOMING APPOINTMENTS (future appointments, not cancelled)
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=now,
        status__in=['pending', 'confirmed']
    ).select_related('patient').order_by('appointment_date')[:10]
    
    upcoming_appointments_count = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=now,
        status__in=['pending', 'confirmed']
    ).count()
    
    # 2. TODAY'S APPOINTMENTS COUNT (all status except cancelled)
    patients_today_count = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__range=[today_start, today_end],
    ).exclude(status='cancelled').count()
    
    # 3. TODAY'S EARNINGS (completed and paid appointments today)
    earnings_today = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__range=[today_start, today_end],
        status='completed',
        payment_status='paid'
    ).aggregate(
        total=Sum('consultation_fee')
    )['total'] or Decimal('0.00')
    
    # 4. DOCTOR RATING & REVIEWS (using default values if not set)
    avg_rating = doctor.rating if doctor.rating else Decimal('4.5')
    total_reviews = doctor.total_reviews if doctor.total_reviews else 0
    
    # 5. ADDITIONAL STATS (optional but useful)
    total_patients = Appointment.objects.filter(
        doctor=doctor
    ).values('patient').distinct().count()
    
    completed_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='completed'
    ).count()
    
    pending_appointments = Appointment.objects.filter(
        doctor=doctor,
        status='pending'
    ).count()
    
    # Debug prints (can be removed in production)
    print(f"\n{'='*60}")
    print(f"🩺 DOCTOR DASHBOARD - {doctor.user.username}")
    print(f"{'='*60}")
    print(f"📅 Today's Date: {today}")
    print(f"⏰ Current Time: {now}")
    print(f"📊 Upcoming Appointments: {upcoming_appointments_count}")
    print(f"👥 Patients Today: {patients_today_count}")
    print(f"💰 Earnings Today: ${earnings_today}")
    print(f"⭐ Rating: {avg_rating} ({total_reviews} reviews)")
    print(f"{'='*60}\n")
    
    context = {
        'doctor': doctor,
        'upcoming_appointments': upcoming_appointments,
        'upcoming_appointments_count': upcoming_appointments_count,
        'patients_today_count': patients_today_count,
        'earnings_today': earnings_today,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews,
        'total_patients': total_patients,
        'completed_appointments': completed_appointments,
        'pending_appointments': pending_appointments,
    }
    
    return render(request, 'doctor/dashboard.html', context)


@login_required
def doctor_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    context = {'doctor': doctor}
    return render(request, 'doctor/profile.html', context)


@login_required
def doctor_profile_edit(request):
    """Allow doctor to edit both User and Doctor profile info"""
    doctor, created = Doctor.objects.get_or_create(user=request.user)

    # Fetch dropdown options
    divisions = Division.objects.all()
    districts = District.objects.all()
    upazilas = Upazila.objects.all()
    departments = Department.objects.all()
    symptoms = Symptom.objects.all()

    if request.method == 'POST':
        # USER MODEL UPDATE
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.save()

        # DOCTOR MODEL UPDATE
        doctor.about = request.POST.get('about', doctor.about)
        doctor.qualification = request.POST.get('qualification', doctor.qualification)
        doctor.total_experience = request.POST.get('total_experience', doctor.total_experience)
        doctor.bmdc_number = request.POST.get('bmdc_number', doctor.bmdc_number)

        # Safe ForeignKey Assignment
        division_id = request.POST.get('division')
        district_id = request.POST.get('district')
        upazila_id = request.POST.get('upazila')

        doctor.division = Division.objects.filter(id=division_id).first() if division_id else None
        doctor.district = District.objects.filter(id=district_id).first() if district_id else None
        doctor.upazila = Upazila.objects.filter(id=upazila_id).first() if upazila_id else None

        # Profile Image
        if 'profile_image' in request.FILES:
            doctor.profile_image = request.FILES['profile_image']

        doctor.save()

        messages.success(request, "✅ Profile updated successfully!")
        return redirect('doctor:doctor_profile_edit')

    context = {
        'doctor': doctor,
        'divisions': divisions,
        'districts': districts,
        'upazilas': upazilas,
        'departments': departments,
        'symptoms': symptoms,
    }
    return render(request, 'doctor/profile_edit.html', context)


@login_required
def doctor_expertise_edit(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    departments = Department.objects.all()
    symptoms = Symptom.objects.all()

    # Doctor's selected departments
    selected_departments = DoctorSpecializationDepartment.objects.filter(
        doctor=doctor
    ).values_list('department_id', flat=True)

    # Doctor's selected symptoms
    selected_symptoms = DoctorSpecializationSymptom.objects.filter(
        doctor=doctor
    ).values_list('symptom_id', flat=True)

    context = {
        "doctor": doctor,
        "departments": departments,
        "symptoms": symptoms,
        "selected_departments": list(selected_departments),
        "selected_symptoms": list(selected_symptoms),
    }

    return render(request, "doctor/expertise_edit.html", context)


@login_required
def update_doctor_expertise(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    if request.method == "POST":
        dept_ids = request.POST.getlist("departments[]")
        sym_ids = request.POST.getlist("symptoms[]")

        # Clear old relations
        DoctorSpecializationDepartment.objects.filter(doctor=doctor).delete()
        DoctorSpecializationSymptom.objects.filter(doctor=doctor).delete()

        # Add departments
        for d_id in dept_ids:
            DoctorSpecializationDepartment.objects.create(
                doctor=doctor,
                department_id=d_id
            )

        # Add symptoms
        for s_id in sym_ids:
            DoctorSpecializationSymptom.objects.create(
                doctor=doctor,
                symptom_id=s_id
            )

        messages.success(request, "Your expertise has been updated successfully!")
        return redirect("doctor:expertise_edit")

    return redirect("doctor:expertise_edit")


@login_required
def ajax_load_districts(request):
    division_id = request.GET.get('division_id')
    districts = District.objects.filter(division_id=division_id).values('id', 'district_name')
    return JsonResponse(list(districts), safe=False)


@login_required
def ajax_load_upazilas(request):
    district_id = request.GET.get('district_id')
    upazilas = Upazila.objects.filter(district_id=district_id).values('id', 'upazila_name')
    return JsonResponse(list(upazilas), safe=False)


DAYS_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


@login_required
def doctor_experience_manage(request, exp_id=None):
    doctor = get_object_or_404(Doctor, user=request.user)
    experiences = doctor.experiences.all()
    working_hours = doctor.working_hours or {}

    # For editing specific experience
    experience = None
    if exp_id:
        experience = get_object_or_404(DoctorExperience, id=exp_id, doctor=doctor)

    # WORKING HOURS SAVE
    if request.method == "POST" and "working_hours_submit" in request.POST:
        updated_hours = {}
        for day in DAYS_OF_WEEK:
            time_value = request.POST.get(f"wh_{day}", "")
            updated_hours[day] = time_value

        doctor.working_hours = updated_hours
        doctor.save()
        messages.success(request, "Working hours updated successfully.")
        return redirect("doctor:experience_manage")

    # EXPERIENCE ADD/EDIT
    if request.method == "POST" and "experience_submit" in request.POST:
        hospital_name = request.POST.get("hospital_name")
        designation = request.POST.get("designation")
        department = request.POST.get("department")

        if not hospital_name or not designation:
            messages.error(request, "Hospital name and designation are required.")
            return redirect("doctor:experience_manage")

        if experience:
            # Update
            experience.hospital_name = hospital_name
            experience.designation = designation
            experience.department = department
            experience.save()
            messages.success(request, "Experience updated successfully.")
        else:
            # Add
            DoctorExperience.objects.create(
                doctor=doctor,
                hospital_name=hospital_name,
                designation=designation,
                department=department,
            )
            messages.success(request, "Experience added successfully.")

        return redirect("doctor:experience_manage")

    context = {
        "experiences": experiences,
        "experience": experience,
        "days": DAYS_OF_WEEK,
        "working_hours": working_hours,
    }

    return render(request, "doctor/experience_manage.html", context)


@login_required
def doctor_experience_delete(request, exp_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    experience = get_object_or_404(DoctorExperience, id=exp_id, doctor=doctor)
    experience.delete()
    messages.success(request, "Experience deleted successfully.")
    return redirect('doctor:experience_manage')


@login_required
def manage_appointment_fees(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    categories = DoctorAppointmentFee.APPOINTMENT_CATEGORIES

    # Build a list of fees for the template
    fees_list = []
    for key, label in categories:
        fee = doctor.appointment_fees.filter(category=key).first()
        fees_list.append({
            'key': key,
            'label': label,
            'fee': fee.price if fee else ''
        })

    if request.method == 'POST':
        for key, label in categories:
            price = request.POST.get(f'price_{key}')
            if price:
                DoctorAppointmentFee.objects.update_or_create(
                    doctor=doctor,
                    category=key,
                    defaults={'price': price}
                )
            else:
                DoctorAppointmentFee.objects.filter(doctor=doctor, category=key).delete()
        messages.success(request, "Appointment fees updated successfully!")
        return redirect('doctor:manage_appointment_fees')

    context = {
        'fees_list': fees_list
    }
    return render(request, 'doctor/manage_appointment_fees.html', context)


@login_required
@cache_control(no_cache=True, no_store=True, must_revalidate=True, max_age=0)
def doctor_logout_view(request):
    logout(request)
    return render(request, "users/logout_replace.html")















#appointment 
@login_required
def doctor_appointments(request):
    """
    View all appointments for the logged-in doctor
    """
    # Check if user is a doctor
    if not hasattr(request.user, 'doctor_profile'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    doctor = request.user.doctor_profile
    now = timezone.now()
    today = now.date()
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'all')
    search_query = request.GET.get('search', '')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    consultation_type_filter = request.GET.get('consultation_type', 'all')
    payment_status_filter = request.GET.get('payment_status', 'all')
    
    # Base queryset
    appointments = Appointment.objects.filter(doctor=doctor)
    
    # Apply status filter
    if status_filter != 'all':
        appointments = appointments.filter(status=status_filter)
    
    # Apply date filters
    if date_filter == 'today':
        appointments = appointments.filter(appointment_date__date=today)
    elif date_filter == 'upcoming':
        appointments = appointments.filter(appointment_date__gte=now)
    elif date_filter == 'past':
        appointments = appointments.filter(appointment_date__lt=now)
    elif date_filter == 'week':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        appointments = appointments.filter(
            appointment_date__date__gte=week_start,
            appointment_date__date__lte=week_end
        )
    elif date_filter == 'month':
        first_day_of_month = today.replace(day=1)
        appointments = appointments.filter(appointment_date__date__gte=first_day_of_month)
    
    # Apply custom date range from input fields
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            appointments = appointments.filter(appointment_date__date__gte=start_date)
        except ValueError:
            pass
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            appointments = appointments.filter(appointment_date__date__lte=end_date)
        except ValueError:
            pass
    
    # Apply consultation type filter
    if consultation_type_filter != 'all':
        appointments = appointments.filter(consultation_type=consultation_type_filter)
    
    # Apply payment status filter
    if payment_status_filter != 'all':
        appointments = appointments.filter(payment_status=payment_status_filter)
    
    # Apply search filter
    if search_query:
        appointments = appointments.filter(
            Q(patient__username__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient_name__icontains=search_query) |
            Q(patient_phone__icontains=search_query) |
            Q(symptoms__icontains=search_query)
        )
    
    # Order by appointment date (upcoming first)
    appointments = appointments.order_by('appointment_date')
    
    # Pagination
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # ====== CALCULATE STATISTICS ======
    
    # Get all appointments for this doctor
    all_appointments = Appointment.objects.filter(doctor=doctor)
    
    # Get today's datetime range
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    # Get today's appointments
    today_appointments = all_appointments.filter(appointment_date__range=[today_start, today_end])
    
    # Get unique patients
    total_patients = all_appointments.values('patient').distinct().count()
    today_patients = today_appointments.values('patient').distinct().count()
    
    # ====== EARNINGS CALCULATION FROM PaymentTransaction ======
    
    # Get paid payment transactions for this doctor
    paid_transactions = PaymentTransaction.objects.filter(
        appointment__doctor=doctor,
        status='paid'
    ).select_related('appointment')
    
    # Total earnings from all paid transactions
    total_earnings = paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Today's earnings (from appointments today with paid transactions)
    today_paid_transactions = paid_transactions.filter(
        created_at__range=[today_start, today_end]
    )
    earnings_today = today_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Monthly earnings (current month)
    month_start = today.replace(day=1)
    month_start_dt = timezone.make_aware(datetime.combine(month_start, datetime.min.time()))
    month_paid_transactions = paid_transactions.filter(
        created_at__gte=month_start_dt
    )
    monthly_earnings = month_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Weekly earnings (this week)
    week_start = today - timedelta(days=today.weekday())
    week_start_dt = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))
    week_paid_transactions = paid_transactions.filter(
        created_at__gte=week_start_dt
    )
    weekly_earnings = week_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Calculate averages
    avg_today = Decimal('0.00')
    if today_paid_transactions.count() > 0:
        avg_today = earnings_today / today_paid_transactions.count()
    
    # ====== APPOINTMENT STATISTICS ======
    
    stats = {
        'total': all_appointments.count(),
        'pending': all_appointments.filter(status='pending').count(),
        'confirmed': all_appointments.filter(status='confirmed').count(),
        'completed': all_appointments.filter(status='completed').count(),
        'cancelled': all_appointments.filter(status='cancelled').count(),
        
        'today': today_appointments.count(),
        'today_patients': today_patients,
        'pending_today': today_appointments.filter(status='pending').count(),
        'completed_today': today_appointments.filter(status='completed').count(),
        
        # Earnings statistics
        'earnings_today': earnings_today,
        'weekly_earnings': weekly_earnings,
        'monthly_earnings': monthly_earnings,
        'total_earnings': total_earnings,
        'avg_today': avg_today,
        
        'total_patients': total_patients,
    }
    
    # Prepare date range for display
    date_range = None
    if start_date_str and end_date_str:
        try:
            start_date_display = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date_display = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            date_range = {
                'start': start_date_display,
                'end': end_date_display,
            }
        except ValueError:
            pass
    
    context = {
        'doctor': doctor,
        'page_obj': page_obj,
        'appointments': page_obj.object_list,
        'stats': stats,
        
        # Filter values for template
        'status_filter': status_filter,
        'date_filter': date_filter,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'search_query': search_query,
        'consultation_type_filter': consultation_type_filter,
        'payment_status_filter': payment_status_filter,
        
        'status_choices': dict(Appointment.APPOINTMENT_STATUS),
        'today': today,
        'date_range': date_range,
    }
    
    return render(request, 'doctor/appointments_list.html', context)



# ============ DOCTOR APPOINTMENT VIEWS ============
@login_required
def doctor_appointments(request):
    """
    View all appointments for the logged-in doctor
    """
    # Check if user is a doctor
    if not hasattr(request.user, 'doctor_profile'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    doctor = request.user.doctor_profile
    now = timezone.now()
    today = now.date()
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'all')
    search_query = request.GET.get('search', '')
    
    # Base queryset
    appointments = Appointment.objects.filter(doctor=doctor)
    
    # Apply filters
    if status_filter != 'all':
        appointments = appointments.filter(status=status_filter)
    
    if date_filter == 'today':
        appointments = appointments.filter(appointment_date__date=today)
    elif date_filter == 'upcoming':
        appointments = appointments.filter(appointment_date__gte=now)
    elif date_filter == 'past':
        appointments = appointments.filter(appointment_date__lt=now)
    elif date_filter == 'week':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        appointments = appointments.filter(
            appointment_date__date__gte=week_start,
            appointment_date__date__lte=week_end
        )
    elif date_filter == 'month':
        first_day_of_month = today.replace(day=1)
        appointments = appointments.filter(appointment_date__date__gte=first_day_of_month)
    
    if search_query:
        appointments = appointments.filter(
            Q(patient__username__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient_name__icontains=search_query) |
            Q(patient_phone__icontains=search_query)
        )
    
    # Order by appointment date (upcoming first)
    appointments = appointments.order_by('appointment_date')
    
    # Pagination
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # ====== CALCULATE STATISTICS ======
    
    # Get all appointments for this doctor
    all_appointments = Appointment.objects.filter(doctor=doctor)
    
    # Get today's datetime range
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    # Get today's appointments
    today_appointments = all_appointments.filter(appointment_date__range=[today_start, today_end])
    
    # Get unique patients
    total_patients = all_appointments.values('patient').distinct().count()
    today_patients = today_appointments.values('patient').distinct().count()
    
    # ====== EARNINGS CALCULATION FROM PaymentTransaction ======
    
    # Get paid payment transactions for this doctor
    paid_transactions = PaymentTransaction.objects.filter(
        appointment__doctor=doctor,
        status='paid'
    ).select_related('appointment')
    
    # Total earnings from all paid transactions
    total_earnings = paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Today's earnings (from appointments today with paid transactions)
    today_paid_transactions = paid_transactions.filter(
        created_at__range=[today_start, today_end]
    )
    earnings_today = today_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Monthly earnings (current month)
    month_start = today.replace(day=1)
    month_start_dt = timezone.make_aware(datetime.combine(month_start, datetime.min.time()))
    month_paid_transactions = paid_transactions.filter(
        created_at__gte=month_start_dt
    )
    monthly_earnings = month_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Weekly earnings (this week)
    week_start = today - timedelta(days=today.weekday())
    week_start_dt = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))
    week_paid_transactions = paid_transactions.filter(
        created_at__gte=week_start_dt
    )
    weekly_earnings = week_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Calculate averages
    avg_today = Decimal('0.00')
    if today_paid_transactions.count() > 0:
        avg_today = earnings_today / today_paid_transactions.count()
    
    # ====== APPOINTMENT STATISTICS ======
    
    stats = {
        'total': all_appointments.count(),
        'pending': all_appointments.filter(status='pending').count(),
        'confirmed': all_appointments.filter(status='confirmed').count(),
        'completed': all_appointments.filter(status='completed').count(),
        'cancelled': all_appointments.filter(status='cancelled').count(),
        
        'today': today_appointments.count(),
        'today_patients': today_patients,
        'pending_today': today_appointments.filter(status='pending').count(),
        'completed_today': today_appointments.filter(status='completed').count(),
        
        # Earnings statistics
        'earnings_today': earnings_today,
        'weekly_earnings': weekly_earnings,
        'monthly_earnings': monthly_earnings,
        'total_earnings': total_earnings,
        'avg_today': avg_today,
        
        'total_patients': total_patients,
    }
    
    context = {
        'doctor': doctor,
        'page_obj': page_obj,
        'appointments': page_obj.object_list,
        'stats': stats,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'search_query': search_query,
        'status_choices': dict(Appointment.APPOINTMENT_STATUS),
        'today': today,
    }
    
    return render(request, 'doctor/appointments_list.html', context)


# ====== ADD THESE NEW VIEWS FOR MARK AS COMPLETE AND CANCEL ======
@login_required
def doctor_appointments(request):
    """
    View all appointments for the logged-in doctor
    """
    # Check if user is a doctor
    if not hasattr(request.user, 'doctor_profile'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    doctor = request.user.doctor_profile
    now = timezone.now()
    today = now.date()
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'all')
    search_query = request.GET.get('search', '')
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')
    consultation_type_filter = request.GET.get('consultation_type', 'all')
    payment_status_filter = request.GET.get('payment_status', 'all')
    
    # Base queryset
    appointments = Appointment.objects.filter(doctor=doctor)
    
    # Apply status filter
    if status_filter != 'all':
        appointments = appointments.filter(status=status_filter)
    
    # Apply date filters - FIXED
    if date_filter == 'today':
        appointments = appointments.filter(appointment_date__date=today)
    elif date_filter == 'upcoming':
        appointments = appointments.filter(appointment_date__gte=now)
    elif date_filter == 'past':
        appointments = appointments.filter(appointment_date__lt=now)
    elif date_filter == 'week':
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        appointments = appointments.filter(
            appointment_date__date__gte=week_start,
            appointment_date__date__lte=week_end
        )
    elif date_filter == 'month':
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=28) + timedelta(days=4)
        last_day_of_month = last_day_of_month - timedelta(days=last_day_of_month.day)
        appointments = appointments.filter(
            appointment_date__date__gte=first_day_of_month,
            appointment_date__date__lte=last_day_of_month
        )
    elif date_filter == 'custom':
        # Custom date range will be handled by start_date and end_date parameters
        pass
    
    # Apply custom date range from input fields
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            appointments = appointments.filter(appointment_date__date__gte=start_date)
        except ValueError:
            pass
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            appointments = appointments.filter(appointment_date__date__lte=end_date)
        except ValueError:
            pass
    
    # Apply consultation type filter
    if consultation_type_filter != 'all':
        appointments = appointments.filter(consultation_type=consultation_type_filter)
    
    # Apply payment status filter
    if payment_status_filter != 'all':
        appointments = appointments.filter(payment_status=payment_status_filter)
    
    # Apply search filter
    if search_query:
        appointments = appointments.filter(
            Q(patient__username__icontains=search_query) |
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient_name__icontains=search_query) |
            Q(patient_phone__icontains=search_query) |
            Q(symptoms__icontains=search_query)
        )
    
    # Order by appointment date (upcoming first)
    appointments = appointments.order_by('appointment_date')
    
    # Pagination
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # ====== CALCULATE STATISTICS ======
    
    # Get all appointments for this doctor
    all_appointments = Appointment.objects.filter(doctor=doctor)
    
    # Get today's datetime range
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    # Get today's appointments
    today_appointments = all_appointments.filter(appointment_date__range=[today_start, today_end])
    
    # Get unique patients
    total_patients = all_appointments.values('patient').distinct().count()
    today_patients = today_appointments.values('patient').distinct().count()
    
    # ====== EARNINGS CALCULATION FROM PaymentTransaction ======
    
    # Get paid payment transactions for this doctor
    paid_transactions = PaymentTransaction.objects.filter(
        appointment__doctor=doctor,
        status='paid'
    ).select_related('appointment')
    
    # Total earnings from all paid transactions
    total_earnings = paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Today's earnings (from appointments today with paid transactions)
    today_paid_transactions = paid_transactions.filter(
        created_at__range=[today_start, today_end]
    )
    earnings_today = today_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Monthly earnings (current month)
    month_start = today.replace(day=1)
    month_start_dt = timezone.make_aware(datetime.combine(month_start, datetime.min.time()))
    month_paid_transactions = paid_transactions.filter(
        created_at__gte=month_start_dt
    )
    monthly_earnings = month_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Weekly earnings (this week)
    week_start = today - timedelta(days=today.weekday())
    week_start_dt = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))
    week_paid_transactions = paid_transactions.filter(
        created_at__gte=week_start_dt
    )
    weekly_earnings = week_paid_transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    # Calculate averages
    avg_today = Decimal('0.00')
    if today_paid_transactions.count() > 0:
        avg_today = earnings_today / today_paid_transactions.count()
    
    # ====== APPOINTMENT STATISTICS ======
    
    stats = {
        'total': all_appointments.count(),
        'pending': all_appointments.filter(status='pending').count(),
        'confirmed': all_appointments.filter(status='confirmed').count(),
        'completed': all_appointments.filter(status='completed').count(),
        'cancelled': all_appointments.filter(status='cancelled').count(),
        
        'today': today_appointments.count(),
        'today_patients': today_patients,
        'pending_today': today_appointments.filter(status='pending').count(),
        'completed_today': today_appointments.filter(status='completed').count(),
        
        # Earnings statistics
        'earnings_today': earnings_today,
        'weekly_earnings': weekly_earnings,
        'monthly_earnings': monthly_earnings,
        'total_earnings': total_earnings,
        'avg_today': avg_today,
        
        'total_patients': total_patients,
    }
    
    # Prepare date range for display
    date_range = None
    if start_date_str and end_date_str:
        try:
            start_date_display = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date_display = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            date_range = {
                'start': start_date_display,
                'end': end_date_display,
            }
        except ValueError:
            pass
    
    context = {
        'doctor': doctor,
        'page_obj': page_obj,
        'appointments': page_obj.object_list,
        'stats': stats,
        
        # Filter values for template
        'status_filter': status_filter,
        'date_filter': date_filter,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'search_query': search_query,
        'consultation_type_filter': consultation_type_filter or 'all',
        'payment_status_filter': payment_status_filter or 'all',
        
        'status_choices': dict(Appointment.APPOINTMENT_STATUS),
        'today': today,
        'date_range': date_range,
    }
    
    return render(request, 'doctor/appointments_list.html', context)
@login_required
@require_POST
def mark_appointment_complete(request, appointment_id):
    """
    View to mark an appointment as complete
    """
    # Get the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user has permission (doctor of this appointment or admin)
    if not (request.user == appointment.doctor.user or request.user.is_staff):
        messages.error(request, "You don't have permission to mark this appointment as complete.")
        return redirect('doctor:appointment_detail', appointment_id=appointment.id)
    
    # Validate appointment can be marked as complete
    if appointment.status == 'completed':
        messages.warning(request, "This appointment is already marked as complete.")
        return redirect('doctor:appointment_detail', appointment_id=appointment.id)
    
    if appointment.status == 'cancelled':
        messages.error(request, "Cannot mark a cancelled appointment as complete.")
        return redirect('doctor:appointment_detail', appointment_id=appointment.id)
    
    # Check payment status
    if appointment.payment_status not in ['paid', 'refunded']:
        messages.error(request, "Cannot mark appointment as complete without successful payment.")
        return redirect('doctor:appointment_detail', appointment_id=appointment.id)
    
    # Update appointment status
    appointment.status = 'completed'
    appointment.completed_at = timezone.now()
    appointment.completed_by_doctor = True
    
    # If actual end time not set, set it
    if not appointment.actual_end_time:
        appointment.actual_end_time = timezone.now()
    
    # Calculate duration if start time exists
    if appointment.actual_start_time and not appointment.consultation_duration:
        duration = (appointment.actual_end_time - appointment.actual_start_time).seconds // 60
        appointment.consultation_duration = duration
    
    appointment.save()
    
    # Add a system note
    AppointmentNote.objects.create(
        appointment=appointment,
        note_type='system',
        content=f'Appointment marked as complete by {request.user.get_full_name() or request.user.username}',
        created_by=request.user
    )
    
    messages.success(request, "Appointment has been marked as complete successfully!")
    
    # Redirect back to appointment detail or list
    return redirect('doctor:appointment_detail', appointment_id=appointment.id)

@login_required
def appointment_detail(request, appointment_id):
    """
    View detailed information about a specific appointment
    """
    if not hasattr(request.user, 'doctor_profile'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    doctor = request.user.doctor_profile
    
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
        return redirect('doctor:appointments')
    
    # Get payment transaction if exists
    payment_transaction = None
    if hasattr(appointment, 'payment_transaction'):
        payment_transaction = appointment.payment_transaction
    
    context = {
        'doctor': doctor,
        'appointment': appointment,
        'payment_transaction': payment_transaction,
    }
    
    return render(request, 'doctor/appointment_detail.html', context)

@login_required
@require_POST
def update_appointment_status(request, appointment_id):
    """
    Update appointment status (AJAX endpoint)
    """
    if not hasattr(request.user, 'doctor_profile'):
        return JsonResponse({'success': False, 'error': 'Unauthorized'})
    
    doctor = request.user.doctor_profile
    
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
    except Appointment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Appointment not found'})
    
    new_status = request.POST.get('status')
    
    # Valid status check
    valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
    if new_status not in valid_statuses:
        return JsonResponse({'success': False, 'error': 'Invalid status'})
    
    # Store old status
    old_status = appointment.status
    
    # Update appointment
    appointment.status = new_status
    
    # Additional logic based on status change
    if new_status == 'completed' and old_status != 'completed':
        appointment.completed_at = timezone.now()
    elif new_status == 'cancelled' and old_status != 'cancelled':
        appointment.cancelled_at = timezone.now()
    
    appointment.save()
    
    # Create notification for patient
    if new_status in ['completed', 'cancelled']:
        Notification.objects.create(
            user=appointment.patient,
            notification_type='appointment',
            title=f'Appointment {new_status.title()}',
            message=f'Dr. {doctor.user.get_full_name()} has marked your appointment as {new_status}',
            related_id=appointment.id,
            is_read=False
        )
    
    return JsonResponse({
        'success': True,
        'message': f'Appointment status updated to {new_status}',
        'status': new_status,
        'status_display': dict(Appointment.APPOINTMENT_STATUS).get(new_status, new_status),
        'appointment_id': appointment.id
    })



@login_required
def appointment_analytics(request):
    """
    Appointment analytics dashboard
    """
    if not hasattr(request.user, 'doctor_profile'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    doctor = request.user.doctor_profile
    
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Get appointments
    all_appointments = Appointment.objects.filter(doctor=doctor)
    
    # Basic stats
    total_appointments = all_appointments.count()
    completed_appointments = all_appointments.filter(status='completed').count()
    pending_appointments = all_appointments.filter(status='pending').count()
    
    # Earnings stats
    total_earnings = all_appointments.filter(
        status='completed', 
        payment_status='paid'
    ).aggregate(total=Sum('consultation_fee'))['total'] or 0
    
    monthly_earnings = all_appointments.filter(
        appointment_date__date__gte=month_ago,
        status='completed',
        payment_status='paid'
    ).aggregate(total=Sum('consultation_fee'))['total'] or 0
    
    # Daily appointments for the last 7 days
    daily_stats = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        daily_count = all_appointments.filter(
            appointment_date__date=date
        ).count()
        daily_stats.append({
            'date': date.strftime('%b %d'),
            'count': daily_count
        })
    
    # Status distribution
    status_distribution = []
    for status_code, status_name in Appointment.APPOINTMENT_STATUS:
        count = all_appointments.filter(status=status_code).count()
        percentage = (count / total_appointments * 100) if total_appointments > 0 else 0
        status_distribution.append({
            'status': status_name,
            'count': count,
            'percentage': round(percentage, 1)
        })
    
    context = {
        'doctor': doctor,
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'pending_appointments': pending_appointments,
        'total_earnings': total_earnings,
        'monthly_earnings': monthly_earnings,
        'daily_stats': daily_stats,
        'status_distribution': status_distribution,
    }
    
    return render(request, 'doctor/appointment_analytics.html', context)


@login_required
def create_prescription(request, appointment_id):
    """
    Create prescription for an appointment
    """
    if not hasattr(request.user, 'doctor_profile'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    doctor = request.user.doctor_profile
    
    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
        return redirect('doctor:appointments')
    
    if request.method == 'POST':
        # Get form data
        diagnosis = request.POST.get('diagnosis', '')
        advice = request.POST.get('advose', '')
        follow_up_date = request.POST.get('follow_up_date', '')
        
        # Parse medicines from form
        medicines = []
        medicine_names = request.POST.getlist('medicine_name[]')
        medicine_dosages = request.POST.getlist('medicine_dosage[]')
        medicine_durations = request.POST.getlist('medicine_duration[]')
        medicine_instructions = request.POST.getlist('medicine_instructions[]')
        
        for i in range(len(medicine_names)):
            if medicine_names[i].strip():  # Only add if name is not empty
                medicines.append({
                    'name': medicine_names[i],
                    'dosage': medicine_dosages[i] if i < len(medicine_dosages) else '',
                    'duration': medicine_durations[i] if i < len(medicine_durations) else '',
                    'instructions': medicine_instructions[i] if i < len(medicine_instructions) else ''
                })
        
        # Parse test suggestions
        suggested_tests = []
        test_names = request.POST.getlist('test_name[]')
        test_instructions = request.POST.getlist('test_instructions[]')
        
        for i in range(len(test_names)):
            if test_names[i].strip():  # Only add if name is not empty
                suggested_tests.append({
                    'test_name': test_names[i],
                    'instructions': test_instructions[i] if i < len(test_instructions) else ''
                })
        
        # Create prescription (you need to create a Prescription model)
        try:
            from appointment.models import Prescription
            prescription = Prescription.objects.create(
                appointment=appointment,
                doctor=doctor,
                patient=appointment.patient,
                diagnosis=diagnosis,
                advice=advice,
                follow_up_date=follow_up_date if follow_up_date else None,
                medicines=medicines,
                suggested_tests=suggested_tests
            )
            
            # Update appointment status to completed
            appointment.status = 'completed'
            appointment.save()
            
            messages.success(request, "Prescription created successfully!")
            return redirect('doctor:appointment_detail', appointment_id=appointment.id)
            
        except ImportError:
            messages.warning(request, "Prescription model not available. Data saved in session.")
            # Store in session for now
            request.session['prescription_data'] = {
                'diagnosis': diagnosis,
                'advice': advice,
                'medicines': medicines,
                'suggested_tests': suggested_tests
            }
            return redirect('doctor:appointment_detail', appointment_id=appointment.id)
    
    context = {
        'doctor': doctor,
        'appointment': appointment,
    }
    
    return render(request, 'doctor/create_prescription.html', context)


@login_required
def export_appointments(request):
    """
    Export appointments to CSV or PDF
    """
    if not hasattr(request.user, 'doctor_profile'):
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    doctor = request.user.doctor_profile
    
    # Get filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status', 'all')
    
    appointments = Appointment.objects.filter(doctor=doctor)
    
    if start_date:
        appointments = appointments.filter(appointment_date__date__gte=start_date)
    if end_date:
        appointments = appointments.filter(appointment_date__date__lte=end_date)
    if status != 'all':
        appointments = appointments.filter(status=status)
    
    appointments = appointments.order_by('appointment_date')
    
    context = {
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
        'appointments': appointments,
        'status_choices': dict(Appointment.APPOINTMENT_STATUS),
        'export_formats': [
            {'value': 'csv', 'name': 'CSV', 'description': 'Comma separated values'},
            {'value': 'pdf', 'name': 'PDF', 'description': 'Portable document format'},
            {'value': 'excel', 'name': 'Excel', 'description': 'Microsoft Excel format'},
        ],
        'export_fields': [
            {'value': 'id', 'name': 'Appointment ID'},
            {'value': 'patient', 'name': 'Patient Name'},
            {'value': 'date', 'name': 'Date & Time'},
            {'value': 'status', 'name': 'Status'},
            {'value': 'fee', 'name': 'Consultation Fee'},
            {'value': 'payment', 'name': 'Payment Status'},
            {'value': 'type', 'name': 'Consultation Type'},
            {'value': 'phone', 'name': 'Patient Phone'},
            {'value': 'symptoms', 'name': 'Symptoms'},
        ],
        'file_size_estimate': f'{appointments.count() * 2} KB',
        'last_export': 'Never',
        'export_history': [],
    }
    
    # You can implement CSV/PDF generation here
    # For now, just return JSON
    if request.GET.get('format') == 'json':
        data = list(appointments.values(
            'id', 'patient__username', 'patient_name', 'appointment_date',
            'status', 'consultation_fee', 'payment_status'
        ))
        return JsonResponse({'appointments': data})
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,
    }
    
    return render(request, 'doctor/export_appointments.html', context)












# Chat & Messaging Views
# Chat & Messaging Views

@login_required
def doctor_chat_home(request):
    """
    Display chat home for doctor with all patient conversations
    """
    try:
        doctor = request.user.doctor_profile
    except:
        return redirect('doctor:dashboard')
    
    # Get all conversations for this doctor
    # Use 'messages' instead of 'message_set' (correct related_name from model)
    conversations_queryset = Conversation.objects.filter(
        doctor=doctor
    ).select_related(
        'appointment__patient',
        'appointment'
    ).prefetch_related(
        'messages'  # ✅ CORRECT: Use 'messages' not 'message_set'
    ).order_by('-updated_at')
    
    # Build conversations with metadata
    conversations = []
    total_unread = 0
    
    for conv in conversations_queryset:
        appointment = conv.appointment
        
        # Count unread messages from patient
        unread_count = conv.messages.filter(
            is_read=False,
            sender=appointment.patient
        ).count()
        
        # Get last message
        last_message = conv.messages.order_by('-created_at').first()
        
        conversations.append({
            'appointment': appointment,
            'patient': appointment.patient,
            'conversation': conv,
            'unread_count': unread_count,
            'last_message': last_message,
        })
        
        total_unread += unread_count
    
    # Get current appointment from query parameter
    appointment_id = request.GET.get('appointment')
    current_appointment = None
    messages = []
    
    if appointment_id:
        try:
            current_appointment = Appointment.objects.get(
                id=appointment_id,
                doctor=doctor
            )
            
            # Get or create conversation
            conversation, created = Conversation.objects.get_or_create(
                appointment=current_appointment,
                defaults={
                    'doctor': doctor,
                    'patient': current_appointment.patient,
                    'is_active': True
                }
            )
            
            # Get all messages
            messages = conversation.messages.select_related(
                'sender'
            ).order_by('created_at')
            
            # Mark patient messages as read
            conversation.messages.filter(
                is_read=False,
                sender=current_appointment.patient
            ).update(is_read=True)
            
        except Appointment.DoesNotExist:
            pass
    
    # Calculate stats
    today = timezone.now().date()
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    today_appointments_count = Appointment.objects.filter(
        doctor=doctor,
        appointment_date__gte=today_start,
        appointment_date__lte=today_end
    ).exclude(status='cancelled').count()
    
    context = {
        'conversations': conversations,
        'current_appointment': current_appointment,
        'messages': messages,
        'total_unread': total_unread,
        'today_calls': today_appointments_count,
        'today_appointments': today_appointments_count,
    }
    
    return render(request, 'doctor/communication/chat_home.html', context)


@login_required
def send_message(request, appointment_id):
    """
    Send a message in a conversation
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})
    
    try:
        doctor = request.user.doctor_profile
        appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
    except (Appointment.DoesNotExist, AttributeError):
        return JsonResponse({'success': False, 'error': 'Appointment not found'})
    
    # Get or create conversation
    conversation, created = Conversation.objects.get_or_create(
        appointment=appointment,
        defaults={
            'doctor': doctor,
            'patient': appointment.patient,
            'is_active': True
        }
    )
    
    content = request.POST.get('content', '').strip()
    message_type = request.POST.get('message_type', 'text')
    
    try:
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
            message_type=message_type
        )
        
        # Handle file uploads
        if message_type == 'image' and 'image' in request.FILES:
            message.image = request.FILES['image']
            message.save()
        
        elif message_type == 'file' and 'file' in request.FILES:
            message.file = request.FILES['file']
            message.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Message sent successfully',
            'message_id': message.id
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def get_messages(request, appointment_id):
    """
    Get all messages for an appointment (API endpoint)
    """
    try:
        doctor = request.user.doctor_profile
        appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
    except (Appointment.DoesNotExist, AttributeError):
        return JsonResponse({'success': False, 'error': 'Appointment not found'})
    
    try:
        conversation = Conversation.objects.get(appointment=appointment)
    except Conversation.DoesNotExist:
        return JsonResponse({'success': True, 'messages': []})
    
    # Use 'messages' instead of 'message_set'
    messages_qs = conversation.messages.select_related('sender').order_by('created_at')
    
    messages_data = []
    for msg in messages_qs:
        messages_data.append({
            'id': msg.id,
            'sender_name': msg.sender.get_full_name() or msg.sender.username,
            'sender_type': 'doctor' if msg.sender == request.user else 'patient',
            'content': msg.content,
            'message_type': msg.message_type,
            'time': msg.created_at.strftime('%I:%M %p'),
            'is_read': msg.is_read,
            'image_url': msg.image.url if msg.image else None,
            'file_url': msg.file.url if msg.file else None,
        })
    
    return JsonResponse({
        'success': True,
        'messages': messages_data
    })


@login_required
def doctor_chat_detail(request, appointment_id):
    """Doctor's chat interface for a specific appointment"""
    try:
        doctor = request.user.doctor_profile
    except:
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    # Get or create conversation
    conversation, created = Conversation.objects.get_or_create(
        appointment=appointment,
        defaults={
            'doctor': doctor,
            'patient': appointment.patient,
            'is_active': True
        }
    )
    
    # Mark all messages as read
    conversation.messages.filter(
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    # Get all messages - use 'messages' not 'message_set'
    messages_list = conversation.messages.select_related('sender').order_by('created_at')
    
    # Get related data
    prescriptions = Prescription.objects.filter(
        appointment=appointment
    ).order_by('-created_at')
    
    test_reports = TestReport.objects.filter(
        appointment=appointment
    ).order_by('-created_at')
    
    video_calls = VideoCall.objects.filter(
        appointment=appointment
    ).order_by('-scheduled_time')
    
    context = {
        'appointment': appointment,
        'conversation': conversation,
        'messages': messages_list,
        'prescriptions': prescriptions,
        'test_reports': test_reports,
        'video_calls': video_calls,
        'patient': appointment.patient,
        'doctor': doctor,
        'active_tab': 'chat'
    }
    return render(request, 'doctor/communication/chat_detail.html', context)





# Prescription Management
@login_required
def create_prescription_view(request, appointment_id):
    """Create prescription for an appointment"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        try:
            # Parse medicines from form
            medicine_names = request.POST.getlist('medicine_name[]')
            medicine_dosages = request.POST.getlist('medicine_dosage[]')
            medicine_durations = request.POST.getlist('medicine_duration[]')
            medicine_instructions = request.POST.getlist('medicine_instructions[]')
            
            medicines = []
            for i in range(len(medicine_names)):
                if medicine_names[i].strip():
                    medicines.append({
                        'name': medicine_names[i],
                        'dosage': medicine_dosages[i] if i < len(medicine_dosages) else '',
                        'duration': medicine_durations[i] if i < len(medicine_durations) else '',
                        'instructions': medicine_instructions[i] if i < len(medicine_instructions) else ''
                    })
            
            # Parse suggested tests
            test_names = request.POST.getlist('test_name[]')
            test_instructions = request.POST.getlist('test_instructions[]')
            
            suggested_tests = []
            for i in range(len(test_names)):
                if test_names[i].strip():
                    suggested_tests.append({
                        'test_name': test_names[i],
                        'instructions': test_instructions[i] if i < len(test_instructions) else ''
                    })
            
            # Create prescription
            prescription = Prescription.objects.create(
                appointment=appointment,
                doctor=doctor,
                patient=appointment.patient,
                diagnosis=request.POST.get('diagnosis', ''),
                advice=request.POST.get('advice', ''),
                follow_up_date=request.POST.get('follow_up_date') or None,
                medicines=medicines,
                suggested_tests=suggested_tests
            )
            
            # Add prescription as message in conversation
            try:
                conversation = Conversation.objects.get(appointment=appointment)
                Message.objects.create(
                    conversation=conversation,
                    sender=request.user,
                    message_type='prescription',
                    content=f'New prescription created for {appointment.patient.get_full_name()}',
                    is_read=False
                )
            except Conversation.DoesNotExist:
                pass
            
            # Create notification for patient
            Notification.objects.create(
                user=appointment.patient,
                notification_type='prescription',
                title=f'New Prescription from Dr. {doctor.user.get_full_name()}',
                message=f'Doctor has prescribed medicines for your appointment',
                related_id=appointment.id,
                is_read=False
            )
            
            return JsonResponse({'success': True, 'prescription_id': prescription.id})
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    context = {
        'appointment': appointment,
        'active_tab': 'appointments'
    }
    return render(request, 'doctor/communication/create_prescription.html', context)

@login_required
def view_prescription(request, prescription_id):
    """View prescription details"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect('home')
    
    prescription = get_object_or_404(Prescription, id=prescription_id, doctor=doctor)
    
    context = {
        'prescription': prescription,
        'appointment': prescription.appointment
    }
    return render(request, 'doctor/communication/view_prescription.html', context)

# Test Report Management
@login_required
def review_test_report(request, report_id):
    """Doctor reviews a test report"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect('home')
    
    test_report = get_object_or_404(TestReport, id=report_id, appointment__doctor=doctor)
    
    if request.method == 'POST':
        test_report.doctor_notes = request.POST.get('doctor_notes', '')
        test_report.status = 'reviewed'
        test_report.save()
        
        # Create notification for patient
        Notification.objects.create(
            user=test_report.patient,
            notification_type='test_report',
            title='Test Report Reviewed',
            message=f'Dr. {doctor.user.get_full_name()} has reviewed your test report',
            related_id=test_report.appointment.id,
            is_read=False
        )
        
        return JsonResponse({'success': True})
    
    context = {
        'test_report': test_report,
        'appointment': test_report.appointment
    }
    return render(request, 'doctor/communication/review_test_report.html', context)





# Video Call Management
@login_required
def doctor_video_calls(request):
    """Doctor's video calls dashboard"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect('home')
    
    # Get upcoming calls
    upcoming_calls = VideoCall.objects.filter(
        doctor=doctor,
        status__in=['scheduled'],
        scheduled_time__gte=timezone.now()
    ).select_related('appointment', 'patient').order_by('scheduled_time')
    
    # Get past calls
    past_calls = VideoCall.objects.filter(
        doctor=doctor,
        status__in=['completed', 'cancelled', 'missed']
    ).select_related('appointment', 'patient').order_by('-scheduled_time')[:50]
    
    # Get ongoing call if any
    ongoing_call = VideoCall.objects.filter(
        doctor=doctor,
        status='ongoing'
    ).first()
    
    context = {
        'upcoming_calls': upcoming_calls,
        'past_calls': past_calls,
        'ongoing_call': ongoing_call,
        'active_tab': 'video_calls'
    }
    return render(request, 'doctor/communication/video_calls.html', context)

@login_required
def schedule_video_call_view(request, appointment_id):
    """Schedule a video call with patient"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        try:
            scheduled_time_str = request.POST.get('scheduled_time')
            call_type = request.POST.get('call_type', 'video')
            notes = request.POST.get('notes', '')
            
            scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')
            
            # Generate unique call ID
            call_id = f"call_{str(uuid.uuid4())[:8]}"
            
            # Create video call
            video_call = VideoCall.objects.create(
                appointment=appointment,
                doctor=doctor,
                patient=appointment.patient,
                call_type=call_type,
                scheduled_time=scheduled_time,
                call_id=call_id,
                notes=notes,
                status='scheduled'
            )
            
            # Create notification for patient
            Notification.objects.create(
                user=appointment.patient,
                notification_type='video_call',
                title=f'{call_type.title()} Call Scheduled with Dr. {doctor.user.get_full_name()}',
                message=f'Your {call_type} call is scheduled for {scheduled_time.strftime("%B %d, %Y at %I:%M %p")}',
                related_id=appointment.id,
                is_read=False
            )
            
            return JsonResponse({
                'success': True,
                'call_id': call_id,
                'scheduled_time': scheduled_time.strftime('%B %d, %Y at %I:%M %p')
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    context = {
        'appointment': appointment,
        'min_date': timezone.now().strftime('%Y-%m-%d'),
        'default_time': (timezone.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
    }
    return render(request, 'doctor/communication/schedule_video_call.html', context)

@login_required
def video_call_room_doctor(request, call_id):
    """Doctor joins video call room"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return redirect('home')
    
    video_call = get_object_or_404(VideoCall, call_id=call_id, doctor=doctor)
    
    # Update call status if starting
    if request.GET.get('join') == 'true' and video_call.status == 'scheduled':
        video_call.status = 'ongoing'
        video_call.actual_start_time = timezone.now()
        video_call.save()
    
    context = {
        'video_call': video_call,
        'appointment': video_call.appointment,
        'user_type': 'doctor',
        'user_name': doctor.user.get_full_name(),
        'user_id': request.user.id,
        'peer_id': f"doctor_{request.user.id}",
        'patient_name': video_call.patient.get_full_name(),
        'patient_peer_id': f"patient_{video_call.patient.id}",
        'agora_app_id': settings.AGORA_APP_ID if hasattr(settings, 'AGORA_APP_ID') else None
    }
    return render(request, 'doctor/communication/video_call_room.html', context)

@login_required
@require_POST
def start_video_call(request, call_id):
    """Doctor starts a video call"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Doctor not found'})
    
    video_call = get_object_or_404(VideoCall, call_id=call_id, doctor=doctor)
    
    if video_call.status == 'scheduled':
        video_call.status = 'ongoing'
        video_call.actual_start_time = timezone.now()
        video_call.save()
        
        # Create notification for patient
        Notification.objects.create(
            user=video_call.patient,
            notification_type='video_call',
            title='Video Call Started',
            message=f'Dr. {doctor.user.get_full_name()} has started the video call',
            related_id=video_call.appointment.id,
            is_read=False
        )
        
        return JsonResponse({'success': True, 'status': 'ongoing'})
    
    return JsonResponse({'success': False, 'error': 'Cannot start call'})

@login_required
@require_POST
def end_video_call_doctor(request, call_id):
    """Doctor ends a video call"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Doctor not found'})
    
    video_call = get_object_or_404(VideoCall, call_id=call_id, doctor=doctor)
    
    if video_call.status == 'ongoing':
        video_call.status = 'completed'
        video_call.actual_end_time = timezone.now()
        
        # Calculate duration in minutes
        if video_call.actual_start_time:
            duration = (video_call.actual_end_time - video_call.actual_start_time).seconds // 60
            video_call.duration = duration
        
        video_call.save()
        
        return JsonResponse({'success': True, 'duration': video_call.duration})
    
    return JsonResponse({'success': False, 'error': 'Call not in progress'})

@login_required
@require_POST
def cancel_video_call(request, call_id):
    """Doctor cancels a scheduled video call"""
    try:
        # Changed from doctor to doctor_profile
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Doctor not found'})
    
    video_call = get_object_or_404(VideoCall, call_id=call_id, doctor=doctor)
    
    if video_call.status == 'scheduled':
        video_call.status = 'cancelled'
        video_call.save()
        
        # Create notification for patient
        Notification.objects.create(
            user=video_call.patient,
            notification_type='video_call',
            title='Video Call Cancelled',
            message=f'Dr. {doctor.user.get_full_name()} has cancelled the scheduled video call',
            related_id=video_call.appointment.id,
            is_read=False
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Cannot cancel call'})

# Notifications
@login_required
@require_GET
def get_doctor_notifications(request):
    """Get doctor's notifications (AJAX)"""
    try:
        # Changed from doctor to doctor_profile (optional, as we're using request.user)
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        # User might not be a doctor, but still allow getting notifications
        pass
    
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:20]
    
    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()
    
    notifications_data = []
    for notif in notifications:
        notifications_data.append({
            'id': notif.id,
            'type': notif.notification_type,
            'title': notif.title,
            'message': notif.message,
            'is_read': notif.is_read,
            'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'time_ago': timesince(notif.created_at)
        })
    
    return JsonResponse({
        'success': True,
        'notifications': notifications_data,
        'unread_count': unread_count
    })

@login_required
@require_POST
def mark_notification_read_doctor(request, notification_id):
    """Mark notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'})

@login_required
@require_POST
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})

# Utility function for time since
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    now = timezone.now()
    diff = now - dt
    
    periods = (
        (diff.days // 365, "year", "years"),
        (diff.days // 30, "month", "months"),
        (diff.days // 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds // 3600, "hour", "hours"),
        (diff.seconds // 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    
    for period, singular, plural in periods:
        if period:
            return f"{period} {singular if period == 1 else plural} ago"
    
    return default







# Utility function for time since
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    now = timezone.now()
    diff = now - dt
    
    periods = (
        (diff.days // 365, "year", "years"),
        (diff.days // 30, "month", "months"),
        (diff.days // 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds // 3600, "hour", "hours"),
        (diff.seconds // 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    
    for period, singular, plural in periods:
        if period:
            return f"{period} {singular if period == 1 else plural} ago"
    
    return default