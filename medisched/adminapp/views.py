from django.shortcuts import render, redirect, get_object_or_404
from .models import Division, District, Upazila, Department, Symptom
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

# Dashboard
def admin_dashboard(request):
    return render(request, 'adminapp/admin_dashboard.html')


# ---------- Division ----------
def division_list(request):
    divisions = Division.objects.all()
    return render(request, 'adminapp/division_list.html', {'divisions': divisions})

def add_division(request):
    if request.method == 'POST':
        name = request.POST['division_name']
        Division.objects.create(division_name=name)
        messages.success(request, 'Division added successfully!')
        return redirect('division_list')
    return redirect('division_list')

def delete_division(request, id):
    division = get_object_or_404(Division, id=id)
    division.delete()
    messages.success(request, 'Division deleted!')
    return redirect('division_list')

def edit_division(request, id):
    division = get_object_or_404(Division, id=id)
    if request.method == 'POST':
        division_name = request.POST['division_name']
        division.division_name = division_name
        division.save()
        messages.success(request, 'Division updated successfully!')
        return redirect('division_list')
    return render(request, 'adminapp/edit_division.html', {'division': division})



# ---------- District ----------
def district_list(request):
    districts = District.objects.select_related('division').all()
    divisions = Division.objects.all()
    return render(request, 'adminapp/district_list.html', {'districts': districts, 'divisions': divisions})

def add_district(request):
    if request.method == 'POST':
        district_name = request.POST['district_name']
        division_id = request.POST['division_id']
        District.objects.create(district_name=district_name, division_id=division_id)
        messages.success(request, 'District added!')
        return redirect('district_list')
    return redirect('district_list')

def delete_district(request, id):
    district = get_object_or_404(District, id=id)
    district.delete()
    messages.success(request, 'District deleted!')
    return redirect('district_list')

def edit_district(request, id):
    district = get_object_or_404(District, id=id)
    divisions = Division.objects.all()
    if request.method == 'POST':
        district_name = request.POST['district_name']
        division_id = request.POST['division_id']
        district.district_name = district_name
        district.division_id = division_id
        district.save()
        messages.success(request, 'District updated successfully!')
        return redirect('district_list')
    return render(request, 'adminapp/edit_district.html', {'district': district, 'divisions': divisions})


# ---------- Upazila ----------
def upazila_list(request):
    upazilas = Upazila.objects.select_related('district').all()
    districts = District.objects.all()
    return render(request, 'adminapp/upazila_list.html', {'upazilas': upazilas, 'districts': districts})

def add_upazila(request):
    if request.method == 'POST':
        upazila_name = request.POST['upazila_name']
        district_id = request.POST['district_id']
        Upazila.objects.create(upazila_name=upazila_name, district_id=district_id)
        messages.success(request, 'Upazila added!')
        return redirect('upazila_list')
    return redirect('upazila_list')
def edit_upazila(request, id):
    upazila = get_object_or_404(Upazila, id=id)
    districts = District.objects.select_related('division').all()
    if request.method == 'POST':
        upazila_name = request.POST['upazila_name']
        district_id = request.POST['district_id']
        upazila.upazila_name = upazila_name
        upazila.district_id = district_id
        upazila.save()
        messages.success(request, 'Upazila updated successfully!')
        return redirect('upazila_list')
    return render(request, 'adminapp/edit_upazila.html', {'upazila': upazila, 'districts': districts})


def delete_upazila(request, id):
    upazila = get_object_or_404(Upazila, id=id)
    upazila.delete()
    messages.success(request, 'Upazila deleted!')
    return redirect('upazila_list')


# ---------- Department ----------
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'adminapp/department_list.html', {'departments': departments})

def add_department(request):
    if request.method == 'POST':
        name = request.POST.get('department_name')
        image = request.FILES.get('department_image')  # get uploaded image
        Department.objects.create(department_name=name, department_image=image)
        messages.success(request, 'Department added!')
        return redirect('department_list')
    return redirect('department_list')

def edit_department(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == 'POST':
        name = request.POST.get('department_name')
        image = request.FILES.get('department_image')  # get uploaded image (optional)

        department.department_name = name
        if image:  # only update if a new image is uploaded
            department.department_image = image

        department.save()
        messages.success(request, 'Department updated!')
        return redirect('department_list')

    return render(request, 'adminapp/edit_department.html', {'department': department})

def delete_department(request, id):
    department = get_object_or_404(Department, id=id)
    # Optional: delete image file from storage when deleting record
    if department.department_image:
        department.department_image.delete(save=False)
    department.delete()
    messages.success(request, 'Department deleted!')
    return redirect('department_list')



# ---------- Symptom List ----------
def symptom_list(request):
    symptoms = Symptom.objects.all()
    return render(request, 'adminapp/symptom_list.html', {'symptoms': symptoms})


# ---------- Add Symptom ----------
def add_symptom(request):
    if request.method == 'POST':
        name = request.POST.get('symptom_name')
        image = request.FILES.get('symptom_image')  # handle file upload

        # Create the new symptom record
        Symptom.objects.create(symptom_name=name, symptom_image=image)

        messages.success(request, 'Symptom added successfully!')
        return redirect('symptom_list')

    return redirect('symptom_list')


# ---------- Edit Symptom ----------
def edit_symptom(request, id):
    symptom = get_object_or_404(Symptom, id=id)

    if request.method == 'POST':
        name = request.POST.get('symptom_name')
        image = request.FILES.get('symptom_image')

        symptom.symptom_name = name

        # If a new image is uploaded, replace the old one
        if image:
            symptom.symptom_image = image

        symptom.save()
        messages.success(request, 'Symptom updated successfully!')
        return redirect('symptom_list')

    return render(request, 'adminapp/edit_symptom.html', {'symptom': symptom})


# ---------- Delete Symptom ----------
def delete_symptom(request, id):
    symptom = get_object_or_404(Symptom, id=id)
    symptom.delete()
    messages.success(request, 'Symptom deleted successfully!')
    return redirect('symptom_list')



def appointment_list(request):
    # fetch appointments from database
    appointments = []  # replace with actual query
    return render(request, 'adminapp/appointment_list.html', {'appointments': appointments})


# Payments
def payment_list(request):
    # Fetch all payments (example)
    # from payments.models import Payment  # if you have payments app
    payments = []  # replace with real query
    return render(request, 'adminapp/payment_list.html', {'payments': payments})



def user_logout(request):
    logout(request)
    return redirect('login')  # Replace 'login' with your login page URL name



from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from users.models import CustomUser
from .models import Division, District, Upazila, Department, Symptom
from doctor.models import Doctor, DoctorExperience, DoctorSpecializationDepartment, DoctorSpecializationSymptom, DoctorAppointmentFee

# ========== DOCTOR MANAGEMENT ==========

def doctor_list(request):
    doctors = Doctor.objects.all().select_related('user', 'division', 'district', 'upazila')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
       # Build a Q object that performs an OR lookup across multiple fields
          query = Q(user__first_name__icontains=search_query) | \
            Q(user__last_name__icontains=search_query) | \
            Q(phone_number__icontains=search_query)
    
    # Filter by verification status
    verification_filter = request.GET.get('verification', '')
    if verification_filter == 'verified':
        doctors = doctors.filter(is_verified=True)
    elif verification_filter == 'not_verified':
        doctors = doctors.filter(is_verified=False)
    
    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        doctors = doctors.filter(departments__id=department_filter)
    
    context = {
        'doctors': doctors,
        'departments': Department.objects.all(),
        'search_query': search_query,
        'verification_filter': verification_filter,
        'department_filter': department_filter,
    }
    return render(request, 'adminapp/doctor/doctor_list.html', context)


# ========== DOCTOR MANAGEMENT ==========
def doctor_create(request):
    if request.method == 'POST':
        try:
            # Create User
            user = CustomUser.objects.create_user(
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                phone=request.POST.get('phone'),
                user_type='doctor'
            )
            
            # Create Doctor Profile
            doctor = Doctor.objects.create(
                user=user,
                about=request.POST.get('about', ''),
                bmdc_number=request.POST.get('bmdc_number', ''),
                qualification=request.POST.get('qualification', ''),
                total_experience=int(request.POST.get('total_experience', 0) or 0),
                is_verified=request.POST.get('is_verified') == 'on',
                rating=float(request.POST.get('rating', 0.0) or 0.0),
                division_id=request.POST.get('division') or None,
                district_id=request.POST.get('district') or None,
                upazila_id=request.POST.get('upazila') or None,
            )
            
            # Handle profile image
            if 'profile_image' in request.FILES:
                doctor.profile_image = request.FILES['profile_image']
                doctor.save()
            
            # Add Departments
            departments = request.POST.getlist('departments')
            for dept_id in departments:
                if dept_id:
                    department = Department.objects.get(id=dept_id)
                    DoctorSpecializationDepartment.objects.create(
                        doctor=doctor,
                        department=department
                    )
            
            # Add Symptoms
            symptoms = request.POST.getlist('symptoms')
            for symp_id in symptoms:
                if symp_id:
                    symptom = Symptom.objects.get(id=symp_id)
                    DoctorSpecializationSymptom.objects.create(
                        doctor=doctor,
                        symptom=symptom
                    )
            
            # Add Experiences
            hospital_names = request.POST.getlist('hospital_name')
            designations = request.POST.getlist('designation')
            dept_names = request.POST.getlist('experience_department')
            
            for i in range(len(hospital_names)):
                if hospital_names[i] and designations[i]:
                    DoctorExperience.objects.create(
                        doctor=doctor,
                        hospital_name=hospital_names[i],
                        designation=designations[i],
                        department=dept_names[i] if i < len(dept_names) and dept_names[i] else ''
                    )
            
            # Add Appointment Fees
            general_fee = request.POST.get('general_fee')
            special_fee = request.POST.get('special_fee')
            
            if general_fee:
                DoctorAppointmentFee.objects.create(
                    doctor=doctor,
                    category='General',
                    price=general_fee
                )
            
            if special_fee:
                DoctorAppointmentFee.objects.create(
                    doctor=doctor,
                    category='Special',
                    price=special_fee
                )
            
            messages.success(request, f'Doctor {user.first_name} {user.last_name} created successfully!')
            return redirect('doctor_list')
            
        except Exception as e:
            messages.error(request, f'Error creating doctor: {str(e)}')
            return redirect('doctor_create')
    
    context = {
        'divisions': Division.objects.all(),
        'districts': District.objects.all(),  # Load all districts initially
        'upazilas': Upazila.objects.all(),    # Load all upazilas initially
        'departments': Department.objects.all(),
        'symptoms': Symptom.objects.all(),
    }
    return render(request, 'adminapp/doctor/doctor_create.html', context)


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    # Get appointment fees
    general_fee = doctor.appointment_fees.filter(category='General').first()
    special_fee = doctor.appointment_fees.filter(category='Special').first()
    
    context = {
        'doctor': doctor,
        'general_fee': general_fee.price if general_fee else None,
        'special_fee': special_fee.price if special_fee else None,
    }
    return render(request, 'adminapp/doctor/doctor_detail.html', context)


def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        try:
            # Update User
            user = doctor.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            
            password = request.POST.get('password')
            if password:
                user.set_password(password)
            
            user.save()
            
            # Update Doctor
            doctor.about = request.POST.get('about', '')
            doctor.bmdc_number = request.POST.get('bmdc_number', '')
            doctor.qualification = request.POST.get('qualification', '')
            doctor.total_experience = int(request.POST.get('total_experience', 0) or 0)
            doctor.is_verified = request.POST.get('is_verified') == 'on'
            doctor.rating = float(request.POST.get('rating', 0.0) or 0.0)
            doctor.division_id = request.POST.get('division') or None
            doctor.district_id = request.POST.get('district') or None
            doctor.upazila_id = request.POST.get('upazila') or None
            
            if 'profile_image' in request.FILES:
                doctor.profile_image = request.FILES['profile_image']
            
            doctor.save()
            
            # Update Departments
            DoctorSpecializationDepartment.objects.filter(doctor=doctor).delete()
            departments = request.POST.getlist('departments')
            for dept_id in departments:
                if dept_id:
                    department = Department.objects.get(id=dept_id)
                    DoctorSpecializationDepartment.objects.create(
                        doctor=doctor,
                        department=department
                    )
            
            # Update Symptoms
            DoctorSpecializationSymptom.objects.filter(doctor=doctor).delete()
            symptoms = request.POST.getlist('symptoms')
            for symp_id in symptoms:
                if symp_id:
                    symptom = Symptom.objects.get(id=symp_id)
                    DoctorSpecializationSymptom.objects.create(
                        doctor=doctor,
                        symptom=symptom
                    )
            
            # Update Experiences
            DoctorExperience.objects.filter(doctor=doctor).delete()
            hospital_names = request.POST.getlist('hospital_name')
            designations = request.POST.getlist('designation')
            dept_names = request.POST.getlist('experience_department')
            
            for i in range(len(hospital_names)):
                if hospital_names[i] and designations[i]:
                    DoctorExperience.objects.create(
                        doctor=doctor,
                        hospital_name=hospital_names[i],
                        designation=designations[i],
                        department=dept_names[i] if i < len(dept_names) and dept_names[i] else ''
                    )
            
            # Update Appointment Fees
            DoctorAppointmentFee.objects.filter(doctor=doctor).delete()
            general_fee = request.POST.get('general_fee')
            special_fee = request.POST.get('special_fee')
            
            if general_fee:
                DoctorAppointmentFee.objects.create(
                    doctor=doctor,
                    category='General',
                    price=general_fee
                )
            
            if special_fee:
                DoctorAppointmentFee.objects.create(
                    doctor=doctor,
                    category='Special',
                    price=special_fee
                )
            
            messages.success(request, f'Doctor {user.first_name} {user.last_name} updated successfully!')
            return redirect('doctor_detail', pk=doctor.id)
            
        except Exception as e:
            messages.error(request, f'Error updating doctor: {str(e)}')
            return redirect('doctor_edit', pk=pk)
    
    # Get related data for dropdowns
    divisions = Division.objects.all()
    districts = District.objects.filter(division=doctor.division) if doctor.division else District.objects.none()
    upazilas = Upazila.objects.filter(district=doctor.district) if doctor.district else Upazila.objects.none()
    
    # Get appointment fees
    general_fee = doctor.appointment_fees.filter(category='General').first()
    special_fee = doctor.appointment_fees.filter(category='Special').first()
    
    context = {
        'doctor': doctor,
        'divisions': divisions,
        'districts': districts,
        'upazilas': upazilas,
        'departments': Department.objects.all(),
        'symptoms': Symptom.objects.all(),
        'selected_departments': [dept.id for dept in doctor.departments.all()],
        'selected_symptoms': [symp.id for symp in doctor.symptoms.all()],
        'experiences': doctor.experiences.all(),
        'general_fee': general_fee.price if general_fee else '',
        'special_fee': special_fee.price if special_fee else '',
    }
    return render(request, 'adminapp/doctor/doctor_edit.html', context)


def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        user_name = f"{doctor.user.first_name} {doctor.user.last_name}"
        doctor.user.delete()
        messages.success(request, f'Doctor {user_name} deleted successfully!')
        return redirect('doctor_list')
    
    return redirect('doctor_detail', pk=pk)


def doctor_verify(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.is_verified = True
    doctor.save()
    messages.success(request, f'Doctor {doctor.user.first_name} {doctor.user.last_name} verified successfully!')
    return redirect('doctor_list')


def doctor_unverify(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.is_verified = False
    doctor.save()
    messages.success(request, f'Doctor {doctor.user.first_name} {doctor.user.last_name} unverified!')
    return redirect('doctor_list')








# adminapp/views.py - Add these appointment views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
import json

from appointment.models import Appointment, AppointmentRescheduleHistory, AppointmentNote
from users.models import CustomUser
from doctor.models import Doctor

def is_admin(user):
    return user.is_staff

# Appointment List View
def appointment_list(request):
    # Get filter parameters
    status = request.GET.get('status', '')
    consultation_type = request.GET.get('consultation_type', '')
    payment_status = request.GET.get('payment_status', '')
    doctor_id = request.GET.get('doctor', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Start with all appointments
    appointments = Appointment.objects.all().select_related(
        'patient', 'doctor', 'doctor__user'
    ).order_by('-created_at')
    
    # Apply filters
    if status:
        appointments = appointments.filter(status=status)
    if consultation_type:
        appointments = appointments.filter(consultation_type=consultation_type)
    if payment_status:
        appointments = appointments.filter(payment_status=payment_status)
    if doctor_id:
        appointments = appointments.filter(doctor_id=doctor_id)
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            appointments = appointments.filter(appointment_date__gte=date_from_obj)
        except:
            pass
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
            appointments = appointments.filter(appointment_date__lte=date_to_obj)
        except:
            pass
    
    # Get all doctors for filter dropdown
    doctors = Doctor.objects.filter(is_verified=True)
    
    # Get statistics
    total_appointments = appointments.count()
    pending_appointments = appointments.filter(status='pending').count()
    confirmed_appointments = appointments.filter(status='confirmed').count()
    completed_appointments = appointments.filter(status='completed').count()
    cancelled_appointments = appointments.filter(status='cancelled').count()
    
    # Pagination
    paginator = Paginator(appointments, 20)  # 20 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'appointments': page_obj,
        'doctors': doctors,
        'status': status,
        'consultation_type': consultation_type,
        'payment_status': payment_status,
        'doctor_id': doctor_id,
        'date_from': date_from,
        'date_to': date_to,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments,
    }
    return render(request, 'adminapp/appointment/list.html', context)

# # Appointment Detail View
# @login_required
# @user_passes_test(is_admin)
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment.objects.select_related(
        'patient', 'doctor', 'doctor__user'
    ), id=appointment_id)
    
    # Get related data
    reschedule_history = AppointmentRescheduleHistory.objects.filter(
        appointment=appointment
    ).order_by('-rescheduled_at')
    
    notes = AppointmentNote.objects.filter(appointment=appointment).order_by('-created_at')
    
    context = {
        'appointment': appointment,
        'reschedule_history': reschedule_history,
        'notes': notes,
    }
    return render(request, 'adminapp/appointment/detail.html', context)


def appointment_update_status(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        new_status = request.POST.get('status')
        cancellation_reason = request.POST.get('cancellation_reason', '')
        
        if new_status in ['confirmed', 'completed', 'cancelled']:
            old_status = appointment.status
            appointment.status = new_status
            
            if new_status == 'cancelled':
                appointment.cancellation_reason = cancellation_reason
                appointment.cancelled_at = timezone.now()
                
                # If appointment is cancelled, optionally refund payment
                if appointment.payment_status == 'paid':
                    appointment.payment_status = 'refunded'
            elif new_status == 'completed':
                appointment.completed_at = timezone.now()
            
            appointment.save()
            
            # Add system note about status change
            AppointmentNote.objects.create(
                appointment=appointment,
                note_type='system',
                content=f'Status changed from {old_status} to {new_status} by admin.',
                created_by=request.user
            )
            
            messages.success(request, f'Appointment status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('appointment_detail', appointment_id=appointment_id)

# # Update Payment Status
# @login_required
# @user_passes_test(is_admin)
def appointment_update_payment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        new_payment_status = request.POST.get('payment_status')
        
        if new_payment_status in ['pending', 'paid', 'failed', 'refunded']:
            old_payment_status = appointment.payment_status
            appointment.payment_status = new_payment_status
            appointment.save()
            
            # Add system note about payment status change
            AppointmentNote.objects.create(
                appointment=appointment,
                note_type='system',
                content=f'Payment status changed from {old_payment_status} to {new_payment_status} by admin.',
                created_by=request.user
            )
            
            messages.success(request, f'Payment status updated to {new_payment_status}.')
        else:
            messages.error(request, 'Invalid payment status selected.')
    
    return redirect('appointment_detail', appointment_id=appointment_id)

# # Add Appointment Note
# @login_required
# @user_passes_test(is_admin)
def appointment_add_note(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        note_content = request.POST.get('note_content', '').strip()
        
        if note_content:
            AppointmentNote.objects.create(
                appointment=appointment,
                note_type='system',
                content=note_content,
                created_by=request.user
            )
            messages.success(request, 'Note added successfully.')
        else:
            messages.error(request, 'Note content cannot be empty.')
    
    return redirect('appointment_detail', appointment_id=appointment_id)

# # Delete Appointment Note
# @login_required
@user_passes_test(is_admin)
def appointment_delete_note(request, note_id):
    note = get_object_or_404(AppointmentNote, id=note_id)
    appointment_id = note.appointment.id
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully.')
    
    return redirect('appointment_detail', appointment_id=appointment_id)

# # Appointment Statistics/Dashboard
# @login_required
# @user_passes_test(is_admin)
def appointment_statistics(request):
    # Date range for statistics
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Overall statistics
    total_appointments = Appointment.objects.count()
    total_revenue = Appointment.objects.filter(payment_status='paid').aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    # Today's statistics
    today_appointments = Appointment.objects.filter(
        created_at__date=today
    ).count()
    today_revenue = Appointment.objects.filter(
        created_at__date=today,
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Weekly statistics
    weekly_appointments = Appointment.objects.filter(
        created_at__date__gte=week_ago
    ).count()
    weekly_revenue = Appointment.objects.filter(
        created_at__date__gte=week_ago,
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Monthly statistics
    monthly_appointments = Appointment.objects.filter(
        created_at__date__gte=month_ago
    ).count()
    monthly_revenue = Appointment.objects.filter(
        created_at__date__gte=month_ago,
        payment_status='paid'
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Status distribution
    status_counts = Appointment.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Payment status distribution
    payment_status_counts = Appointment.objects.values('payment_status').annotate(
        count=Count('id')
    ).order_by('payment_status')
    
    # Recent appointments
    recent_appointments = Appointment.objects.select_related(
        'patient', 'doctor'
    ).order_by('-created_at')[:10]
    
    # Top doctors by appointments
    top_doctors = Doctor.objects.annotate(
        appointment_count=Count('appointments'),
        total_revenue=Sum('appointments__total_amount',
                         filter=Q(appointments__payment_status='paid'))
    ).order_by('-appointment_count')[:10]
    
    context = {
        'today': today,
        'total_appointments': total_appointments,
        'total_revenue': total_revenue,
        'today_appointments': today_appointments,
        'today_revenue': today_revenue,
        'weekly_appointments': weekly_appointments,
        'weekly_revenue': weekly_revenue,
        'monthly_appointments': monthly_appointments,
        'monthly_revenue': monthly_revenue,
        'status_counts': status_counts,
        'payment_status_counts': payment_status_counts,
        'recent_appointments': recent_appointments,
        'top_doctors': top_doctors,
    }
    return render(request, 'adminapp/appointment/statistics.html', context)

# # Export Appointments
# @login_required
# @user_passes_test(is_admin)
def appointment_export(request):
    # For now, just show the export page
    # You can implement CSV/Excel export here
    return render(request, 'adminapp/appointment/export.html')
