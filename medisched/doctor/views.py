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
        today = timezone.now().date()
        appointments = appointments.filter(appointment_date__date=today)
    elif date_filter == 'upcoming':
        appointments = appointments.filter(appointment_date__gte=timezone.now())
    elif date_filter == 'past':
        appointments = appointments.filter(appointment_date__lt=timezone.now())
    
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
    
    # Statistics
    stats = {
        'total': appointments.count(),
        'pending': appointments.filter(status='pending').count(),
        'confirmed': appointments.filter(status='confirmed').count(),
        'completed': appointments.filter(status='completed').count(),
        'cancelled': appointments.filter(status='cancelled').count(),
        'today': Appointment.objects.filter(
            doctor=doctor,
            appointment_date__date=timezone.now().date()
        ).count(),
        'monthly_earnings': Appointment.objects.filter(
            doctor=doctor,
            appointment_date__month=timezone.now().month,
            appointment_date__year=timezone.now().year,
            status='completed',
            payment_status='paid'
        ).aggregate(total=Sum('consultation_fee'))['total'] or 0,
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
    }
    
    return render(request, 'doctor/appointments_list.html', context)


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
def update_appointment_status(request, appointment_id):
    """
    Update appointment status (AJAX endpoint)
    """
    if not hasattr(request.user, 'doctor_profile'):
        return JsonResponse({'success': False, 'error': 'Unauthorized'})
    
    if request.method == 'POST':
        doctor = request.user.doctor_profile
        
        try:
            appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Appointment not found'})
        
        new_status = request.POST.get('status')
        
        if new_status in dict(Appointment.APPOINTMENT_STATUS).keys():
            old_status = appointment.status
            appointment.status = new_status
            
            # Additional logic based on status change
            if new_status == 'completed' and old_status != 'completed':
                appointment.completed_at = timezone.now()
            elif new_status == 'cancelled' and old_status != 'cancelled':
                appointment.cancelled_at = timezone.now()
            
            appointment.save()
            
            # Create notification or log here if needed
            
            return JsonResponse({
                'success': True,
                'message': f'Appointment status updated to {new_status}',
                'status': new_status,
                'status_display': dict(Appointment.APPOINTMENT_STATUS)[new_status]
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


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
