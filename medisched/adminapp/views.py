from django.shortcuts import render, redirect, get_object_or_404
from .models import Division, District, Upazila, Department, Symptom
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

def admin_dashboard(request):
    try:
        # Get current date
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year
        
        # Get first day of current and previous month
        first_day_current = datetime(current_year, current_month, 1).date()
        if current_month == 1:
            first_day_previous = datetime(current_year-1, 12, 1).date()
        else:
            first_day_previous = datetime(current_year, current_month-1, 1).date()
        
        # Basic counts with safe defaults
        total_doctors = Doctor.objects.count()
        total_patients = CustomUser.objects.filter(role='patient').count()
        total_appointments = Appointment.objects.count()
        
        # Get total revenue from paid appointments
        try:
            total_revenue_result = Appointment.objects.filter(payment_status='paid').aggregate(
                total=Sum('total_amount')
            )
            total_revenue = total_revenue_result['total'] or 0
        except:
            total_revenue = 0
        
        # Today's counts
        today_pending_appointments = Appointment.objects.filter(
            appointment_date__date=today,
            status='pending'
        ).count()
        
        today_completed_appointments = Appointment.objects.filter(
            appointment_date__date=today,
            status='completed'
        ).count()
        
        today_cancelled_appointments = Appointment.objects.filter(
            appointment_date__date=today,
            status='cancelled'
        ).count()
        
        today_new_registrations = CustomUser.objects.filter(
            date_joined__date=today
        ).count()
        
        # Location counts
        total_divisions = Division.objects.count()
        total_districts = District.objects.count()
        total_upazilas = Upazila.objects.count()
        
        # Department and symptom counts
        total_departments = Department.objects.count()
        total_symptoms = Symptom.objects.count()
        
        # Pending appointments count
        pending_appointments = Appointment.objects.filter(status='pending').count()
        
        # Monthly statistics for appointments
        monthly_appointments = Appointment.objects.filter(
            created_at__month=current_month,
            created_at__year=current_year
        ).count()
        
        previous_month_appointments = Appointment.objects.filter(
            created_at__date__gte=first_day_previous,
            created_at__date__lt=first_day_current
        ).count()
        
        try:
            monthly_revenue_result = Appointment.objects.filter(
                created_at__month=current_month,
                created_at__year=current_year,
                payment_status='paid'
            ).aggregate(total=Sum('total_amount'))
            monthly_revenue = monthly_revenue_result['total'] or 0
        except:
            monthly_revenue = 0
        
        try:
            previous_month_revenue_result = Appointment.objects.filter(
                created_at__date__gte=first_day_previous,
                created_at__date__lt=first_day_current,
                payment_status='paid'
            ).aggregate(total=Sum('total_amount'))
            previous_month_revenue = previous_month_revenue_result['total'] or 0
        except:
            previous_month_revenue = 0
        
        # New doctors this month (using user's date_joined)
        monthly_new_doctors = Doctor.objects.filter(
            user__date_joined__month=current_month,
            user__date_joined__year=current_year
        ).count()
        
        previous_month_doctors = Doctor.objects.filter(
            user__date_joined__date__gte=first_day_previous,
            user__date_joined__date__lt=first_day_current
        ).count()
        
        # Calculate percentage changes with safe defaults
        def calculate_percent_change(current, previous):
            if previous == 0:
                return 100 if current > 0 else 0
            try:
                return round(((current - previous) / previous) * 100, 1)
            except:
                return 0
        
        monthly_appointments_percent_change = calculate_percent_change(
            monthly_appointments, previous_month_appointments
        )
        
        monthly_revenue_percent_change = calculate_percent_change(
            monthly_revenue, previous_month_revenue
        )
        
        monthly_doctors_percent_change = calculate_percent_change(
            monthly_new_doctors, previous_month_doctors
        )
        
        # Calculate growth percentages (week over week) with safe defaults
        week_ago = today - timedelta(days=7)
        
        # Weekly statistics with safe handling
        doctor_this_week = Doctor.objects.filter(
            user__date_joined__date__gte=week_ago
        ).count()
        
        doctor_previous_week = Doctor.objects.filter(
            user__date_joined__date__gte=week_ago - timedelta(days=7),
            user__date_joined__date__lt=week_ago
        ).count()
        
        patient_this_week = CustomUser.objects.filter(
            date_joined__date__gte=week_ago,
            role='patient'
        ).count()
        
        patient_previous_week = CustomUser.objects.filter(
            date_joined__date__gte=week_ago - timedelta(days=7),
            date_joined__date__lt=week_ago,
            role='patient'
        ).count()
        
        appointment_this_week = Appointment.objects.filter(
            created_at__date__gte=week_ago
        ).count()
        
        appointment_previous_week = Appointment.objects.filter(
            created_at__date__gte=week_ago - timedelta(days=7),
            created_at__date__lt=week_ago
        ).count()
        
        try:
            revenue_this_week_result = Appointment.objects.filter(
                created_at__date__gte=week_ago,
                payment_status='paid'
            ).aggregate(total=Sum('total_amount'))
            revenue_this_week = revenue_this_week_result['total'] or 0
        except:
            revenue_this_week = 0
        
        try:
            revenue_previous_week_result = Appointment.objects.filter(
                created_at__date__gte=week_ago - timedelta(days=7),
                created_at__date__lt=week_ago,
                payment_status='paid'
            ).aggregate(total=Sum('total_amount'))
            revenue_previous_week = revenue_previous_week_result['total'] or 0
        except:
            revenue_previous_week = 0
        
        # Calculate growth percentages
        doctor_growth = calculate_percent_change(doctor_this_week, doctor_previous_week)
        patient_growth = calculate_percent_change(patient_this_week, patient_previous_week)
        appointment_growth = calculate_percent_change(appointment_this_week, appointment_previous_week)
        revenue_growth = calculate_percent_change(revenue_this_week, revenue_previous_week)
        
        # Get top doctors by appointment count
        try:
            top_doctors = Doctor.objects.annotate(
                appointment_count=Count('appointments')
            ).order_by('-appointment_count')[:5]
        except:
            top_doctors = Doctor.objects.all()[:5]
        
        # Get recent activities
        recent_activities = []
        
        # Add recent appointments
        try:
            recent_appointments = Appointment.objects.select_related(
                'patient', 'doctor', 'doctor__user'
            ).order_by('-created_at')[:5]
            
            for appointment in recent_appointments:
                # Get patient name safely
                if appointment.patient:
                    patient_name = appointment.patient.get_full_name() or appointment.patient.username
                else:
                    patient_name = appointment.patient_name or "Unknown Patient"
                
                # Get doctor name safely
                if appointment.doctor and appointment.doctor.user:
                    doctor_name = appointment.doctor.user.get_full_name() or appointment.doctor.user.username
                else:
                    doctor_name = "Unknown Doctor"
                
                recent_activities.append({
                    'title': f'Appointment - {appointment.get_status_display()}',
                    'description': f'{patient_name} with Dr. {doctor_name}',
                    'time': appointment.created_at,
                    'icon': 'fas fa-calendar-check',
                    'color': '#10b981' if appointment.status == 'completed' else 
                            '#f59e0b' if appointment.status == 'pending' else
                            '#ef4444' if appointment.status == 'cancelled' else '#3b82f6'
                })
        except Exception as e:
            print(f"Error getting recent appointments: {e}")
        
        # Add recent doctor registrations
        try:
            recent_doctors = Doctor.objects.select_related('user').order_by('-user__date_joined')[:3]
            for doctor in recent_doctors:
                # Get department name safely
                department_name = "General"
                if doctor.departments.exists():
                    first_department = doctor.departments.all().first()
                    if first_department:
                        department_name = first_department.department_name
                
                recent_activities.append({
                    'title': 'New Doctor Registered',
                    'description': f'Dr. {doctor.user.get_full_name() or doctor.user.username} - {department_name}',
                    'time': doctor.user.date_joined,
                    'icon': 'fas fa-user-md',
                    'color': '#8b5cf6'
                })
        except Exception as e:
            print(f"Error getting recent doctors: {e}")
        
        # Add recent patient registrations
        try:
            recent_patients = CustomUser.objects.filter(
                role='patient'
            ).order_by('-date_joined')[:3]
            
            for patient in recent_patients:
                recent_activities.append({
                    'title': 'New Patient Registered',
                    'description': f'{patient.get_full_name() or patient.username} - {patient.email}',
                    'time': patient.date_joined,
                    'icon': 'fas fa-user-plus',
                    'color': '#3b82f6'
                })
        except Exception as e:
            print(f"Error getting recent patients: {e}")
        
        # Add recent payments
        try:
            recent_payments = Appointment.objects.filter(
                payment_status='paid'
            ).order_by('-created_at')[:3]
            
            for payment in recent_payments:
                patient_name = payment.patient_name
                if not patient_name and payment.patient:
                    patient_name = payment.patient.get_full_name() or payment.patient.username
                
                recent_activities.append({
                    'title': 'Payment Received',
                    'description': f'৳{payment.total_amount} - {patient_name or "Unknown"}',
                    'time': payment.created_at,
                    'icon': 'fas fa-dollar-sign',
                    'color': '#10b981'
                })
        except Exception as e:
            print(f"Error getting recent payments: {e}")
        
        # Sort activities by time (most recent first)
        recent_activities.sort(key=lambda x: x['time'], reverse=True)
        recent_activities = recent_activities[:10]
        
        # Get current month name
        current_month_name = timezone.now().strftime('%B')
        
        context = {
            'today_date': today,
            'total_doctors': total_doctors,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'total_revenue': total_revenue,
            'today_pending_appointments': today_pending_appointments,
            'today_completed_appointments': today_completed_appointments,
            'today_cancelled_appointments': today_cancelled_appointments,
            'today_new_registrations': today_new_registrations,
            'total_divisions': total_divisions,
            'total_districts': total_districts,
            'total_upazilas': total_upazilas,
            'total_departments': total_departments,
            'total_symptoms': total_symptoms,
            'pending_appointments': pending_appointments,
            'doctor_growth': doctor_growth,
            'patient_growth': patient_growth,
            'appointment_growth': appointment_growth,
            'revenue_growth': revenue_growth,
            'top_doctors': top_doctors,
            'recent_activities': recent_activities,
            'monthly_appointments': monthly_appointments,
            'monthly_revenue': monthly_revenue,
            'monthly_new_doctors': monthly_new_doctors,
            'monthly_appointments_percent_change': monthly_appointments_percent_change,
            'monthly_revenue_percent_change': monthly_revenue_percent_change,
            'monthly_doctors_percent_change': monthly_doctors_percent_change,
            'current_month_name': current_month_name,
        }
        
        return render(request, 'adminapp/admin_dashboard.html', context)
        
    except Exception as e:
        # If there's any error, return a minimal working context
        print(f"Dashboard error: {e}")
        import traceback
        traceback.print_exc()
        
        # Minimal context to at least show something
        context = {
            'today_date': timezone.now().date(),
            'total_doctors': Doctor.objects.count(),
            'total_patients': CustomUser.objects.filter(role='patient').count(),
            'total_appointments': Appointment.objects.count(),
            'total_revenue': 0,
            'today_pending_appointments': 0,
            'today_completed_appointments': 0,
            'today_cancelled_appointments': 0,
            'today_new_registrations': 0,
            'total_divisions': Division.objects.count(),
            'total_districts': District.objects.count(),
            'total_upazilas': Upazila.objects.count(),
            'total_departments': Department.objects.count(),
            'total_symptoms': Symptom.objects.count(),
            'pending_appointments': Appointment.objects.filter(status='pending').count(),
            'doctor_growth': 0,
            'patient_growth': 0,
            'appointment_growth': 0,
            'revenue_growth': 0,
            'top_doctors': Doctor.objects.all()[:5],
            'recent_activities': [],
            'monthly_appointments': 0,
            'monthly_revenue': 0,
            'monthly_new_doctors': 0,
            'monthly_appointments_percent_change': 0,
            'monthly_revenue_percent_change': 0,
            'monthly_doctors_percent_change': 0,
            'current_month_name': timezone.now().strftime('%B'),
        }
        
        return render(request, 'adminapp/admin_dashboard.html', context)
    
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
        
        # Debug print to console
        print(f"DEBUG: POST request received for department {id}")
        print(f"DEBUG: Name: {name}")
        print(f"DEBUG: Has image: {'Yes' if image else 'No'}")
        
        if not name:
            messages.error(request, 'Department name is required!')
            return render(request, 'adminapp/edit_department.html', {'department': department})
        
        try:
            department.department_name = name
            if image:  # only update if a new image is uploaded
                # Delete old image if exists
                if department.department_image:
                    department.department_image.delete(save=False)
                department.department_image = image
            
            department.save()
            print(f"DEBUG: Department saved successfully")
            messages.success(request, f'Department "{name}" updated successfully!')
            return redirect('department_list')
            
        except Exception as e:
            print(f"DEBUG: Error saving department: {str(e)}")
            messages.error(request, f'Error updating department: {str(e)}')
            return render(request, 'adminapp/edit_department.html', {'department': department})
    
    # For GET request, render the form
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
# ========== DOCTOR MANAGEMENT ==========
def doctor_create(request):
    if request.method == 'POST':
        try:
            # Generate username from email (or use form field if you add it)
            email = request.POST.get('email')
            
            # Option 1: Generate username from email
            username = email.split('@')[0]  # Use part before @ as username
            
            # Ensure username is unique
            original_username = username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Option 2: If you prefer to use a username from form, add this field to template
            # username = request.POST.get('username')  # Uncomment if you add username field to form
            
            # Create User with proper field names
            user = CustomUser.objects.create_user(
                username=username,  # REQUIRED: Django's AbstractUser requires username
                email=email,
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                phone=request.POST.get('phone', ''),  # Provide default empty string
                role='doctor'  # CORRECT: Use 'role' not 'user_type'
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
                    try:
                        department = Department.objects.get(id=dept_id)
                        DoctorSpecializationDepartment.objects.create(
                            doctor=doctor,
                            department=department
                        )
                    except Department.DoesNotExist:
                        continue  # Skip if department doesn't exist
            
            # Add Symptoms
            symptoms = request.POST.getlist('symptoms')
            for symp_id in symptoms:
                if symp_id:
                    try:
                        symptom = Symptom.objects.get(id=symp_id)
                        DoctorSpecializationSymptom.objects.create(
                            doctor=doctor,
                            symptom=symptom
                        )
                    except Symptom.DoesNotExist:
                        continue  # Skip if symptom doesn't exist
            
            # Add Experiences
            hospital_names = request.POST.getlist('hospital_name')
            designations = request.POST.getlist('designation')
            dept_names = request.POST.getlist('experience_department')
            
            # Only create if we have at least one experience with hospital name
            if hospital_names and hospital_names[0]:  # Check first experience entry
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
            # For debugging
            import traceback
            print(f"Error details: {str(e)}")
            traceback.print_exc()
            
            # Re-render the form with existing data
            context = {
                'divisions': Division.objects.all(),
                'districts': District.objects.all(),
                'upazilas': Upazila.objects.all(),
                'departments': Department.objects.all(),
                'symptoms': Symptom.objects.all(),
            }
            return render(request, 'adminapp/doctor/doctor_create.html', context)
    
    context = {
        'divisions': Division.objects.all(),
        'districts': District.objects.all(),
        'upazilas': Upazila.objects.all(),
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
    
    # Get ALL districts and upazilas for JavaScript filtering
    all_districts = District.objects.all()
    all_upazilas = Upazila.objects.all()
    
    # Convert to JSON for JavaScript
    all_districts_json = json.dumps([
        {
            'id': str(district.id),
            'district_name': district.district_name,
            'division_id': str(district.division.id)
        }
        for district in all_districts
    ])
    
    all_upazilas_json = json.dumps([
        {
            'id': str(upazila.id),
            'upazila_name': upazila.upazila_name,
            'district_id': str(upazila.district.id)
        }
        for upazila in all_upazilas
    ])
    
    # Get appointment fees
    general_fee = doctor.appointment_fees.filter(category='General').first()
    special_fee = doctor.appointment_fees.filter(category='Special').first()
    
    context = {
        'doctor': doctor,
        'divisions': divisions,
        'districts': districts,
        'upazilas': upazilas,
        'all_districts_json': all_districts_json,
        'all_upazilas_json': all_upazilas_json,
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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
import json
import csv
import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from appointment.models import Appointment, ExportHistory

def appointment_export(request):
    # For GET requests, show the export form
    if request.method == 'GET':
        try:
            # Get recent exports for the logged-in user
            recent_exports = ExportHistory.objects.filter(user=request.user).order_by('-created_at')[:5]
        except Exception as e:
            recent_exports = []
            print(f"Error fetching recent exports: {e}")
        
        # Use the nested template path
        return render(request, 'adminapp/appointment/export.html', {
            'recent_exports': recent_exports
        })

    
    # For POST requests, handle the export
    elif request.method == 'POST':
        try:
            # Get filter parameters
            format_type = request.POST.get('format', 'csv')
            date_range = request.POST.get('date_range', 'all')
            status_filter = request.POST.get('status_filter', 'all')
            payment_filter = request.POST.get('payment_filter', 'all')
            columns = request.POST.getlist('columns', [])
            
            # If no columns selected, default to all basic columns
            if not columns:
                columns = ['id', 'patient', 'doctor', 'date', 'status', 'payment', 'amount']
            
            # Start with all appointments
            appointments = Appointment.objects.all()
            
            # Apply filters
            if date_range == 'custom':
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                if start_date and end_date:
                    appointments = appointments.filter(
                        appointment_date__range=[start_date, end_date]
                    )
            
            if status_filter != 'all':
                appointments = appointments.filter(status=status_filter)
            
            if payment_filter != 'all':
                appointments = appointments.filter(payment_status=payment_filter)
            
            # Prepare data for export
            data = []
            headers = []
            
            # Define column mapping
            column_mapping = {
                'id': 'Appointment ID',
                'patient': 'Patient Information',
                'doctor': 'Doctor Information',
                'date': 'Date & Time',
                'status': 'Status',
                'payment': 'Payment Information',
                'amount': 'Amount',
                'notes': 'Notes',
                'symptoms': 'Symptoms'
            }
            
            # Add headers based on selected columns
            for col in columns:
                if col in column_mapping:
                    headers.append(column_mapping[col])
            
            # Add data rows
            for appointment in appointments:
                row = []
                
                for col in columns:
                    if col == 'id':
                        row.append(str(appointment.id))
                    elif col == 'patient':
                        patient_name = appointment.patient_name or (appointment.patient.username if appointment.patient else 'N/A')
                        patient_phone = appointment.patient_phone or 'N/A'
                        patient_info = f"{patient_name}\n{patient_phone}"
                        row.append(patient_info)
                    elif col == 'doctor':
                        doctor_name = appointment.doctor.user.get_full_name() if appointment.doctor and appointment.doctor.user else 'N/A'
                        doctor_specialization = appointment.doctor.specialization if appointment.doctor else 'N/A'
                        doctor_info = f"{doctor_name}\n{doctor_specialization}"
                        row.append(doctor_info)
                    elif col == 'date':
                        if appointment.appointment_date:
                            date_str = appointment.appointment_date.strftime("%Y-%m-%d %H:%M")
                        else:
                            date_str = "Not scheduled"
                        row.append(date_str)
                    elif col == 'status':
                        row.append(appointment.get_status_display())
                    elif col == 'payment':
                        payment_status = appointment.get_payment_status_display()
                        payment_method = appointment.payment_method or "N/A"
                        payment_info = f"{payment_status}\n{payment_method}"
                        row.append(payment_info)
                    elif col == 'amount':
                        row.append(f"৳{appointment.total_amount if appointment.total_amount else '0'}")
                    elif col == 'notes':
                        row.append(appointment.notes or "")
                    elif col == 'symptoms':
                        row.append(appointment.symptoms or "")
                
                data.append(row)
            
            # Create response based on format
            current_date = timezone.now().date()
            
            if format_type == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="appointments_{current_date}.csv"'
                
                writer = csv.writer(response)
                writer.writerow(headers)
                writer.writerows(data)
                
                # Save export history
                try:
                    ExportHistory.objects.create(
                        user=request.user,
                        filename=f"appointments_{current_date}.csv",
                        format='csv',
                        record_count=appointments.count(),
                        filters=json.dumps({
                            'date_range': date_range,
                            'status_filter': status_filter,
                            'payment_filter': payment_filter,
                            'columns': columns
                        }, default=str)  # Use default=str to handle any non-serializable objects
                    )
                except Exception as e:
                    print(f"Error saving export history: {e}")
                    # Continue with export even if history fails
                
                return response
            
            elif format_type == 'excel':
                # Create DataFrame
                df = pd.DataFrame(data, columns=headers)
                
                # Create response
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="appointments_{current_date}.xlsx"'
                
                # Write to Excel
                output = BytesIO()
                try:
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, index=False, sheet_name='Appointments')
                    output.seek(0)
                    response.write(output.getvalue())
                except Exception as e:
                    print(f"Excel export error: {e}")
                    messages.error(request, "Error creating Excel file. Please try CSV format.")
                    return redirect('appointment_export')
                
                # Save export history
                try:
                    ExportHistory.objects.create(
                        user=request.user,
                        filename=f"appointments_{current_date}.xlsx",
                        format='excel',
                        record_count=appointments.count(),
                        filters=json.dumps({
                            'date_range': date_range,
                            'status_filter': status_filter,
                            'payment_filter': payment_filter,
                            'columns': columns
                        }, default=str)
                    )
                except Exception as e:
                    print(f"Error saving export history: {e}")
                
                return response
            
            elif format_type == 'pdf':
                try:
                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="appointments_{current_date}.pdf"'
                    
                    # Create PDF document
                    buffer = BytesIO()
                    doc = SimpleDocTemplate(buffer, pagesize=letter)
                    elements = []
                    
                    # Add title
                    styles = getSampleStyleSheet()
                    title = Paragraph(f"Appointments Report - {current_date}", styles['Title'])
                    elements.append(title)
                    
                    # Add filter info
                    filter_text = f"Total Records: {appointments.count()}"
                    if status_filter != 'all':
                        filter_text += f" | Status: {status_filter}"
                    if payment_filter != 'all':
                        filter_text += f" | Payment: {payment_filter}"
                    elements.append(Paragraph(filter_text, styles['Normal']))
                    elements.append(Paragraph("<br/>", styles['Normal']))
                    
                    # Create table (limit rows for PDF performance)
                    max_pdf_rows = 100
                    table_data = [headers] + data[:max_pdf_rows]
                    
                    if len(data) > max_pdf_rows:
                        warning = Paragraph(f"Note: Showing first {max_pdf_rows} of {len(data)} records", styles['Italic'])
                        elements.append(warning)
                        elements.append(Paragraph("<br/>", styles['Normal']))
                    
                    table = Table(table_data)
                    
                    # Add style
                    style = TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('FONTSIZE', (0, 1), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # Enable word wrap
                    ])
                    table.setStyle(style)
                    elements.append(table)
                    
                    # Build PDF
                    doc.build(elements)
                    pdf = buffer.getvalue()
                    buffer.close()
                    response.write(pdf)
                    
                    # Save export history
                    try:
                        ExportHistory.objects.create(
                            user=request.user,
                            filename=f"appointments_{current_date}.pdf",
                            format='pdf',
                            record_count=min(appointments.count(), max_pdf_rows),
                            filters=json.dumps({
                                'date_range': date_range,
                                'status_filter': status_filter,
                                'payment_filter': payment_filter,
                                'columns': columns
                            }, default=str)
                        )
                    except Exception as e:
                        print(f"Error saving export history: {e}")
                    
                    return response
                    
                except Exception as e:
                    print(f"PDF export error: {e}")
                    messages.error(request, f"Error creating PDF file: {str(e)}. Please try CSV or Excel format.")
                    return redirect('appointment_export')
        
        except Exception as e:
            print(f"Export error: {e}")
            messages.error(request, f"Error exporting data: {str(e)}")
            return redirect('appointment_export')

def download_export(request, export_id):
    try:
        export = ExportHistory.objects.get(id=export_id, user=request.user)
        
        # Create a simple response with the export info
        # In a real implementation, you would generate the file again or serve from storage
        content = f"Export Details:\n"
        content += f"Filename: {export.filename}\n"
        content += f"Format: {export.format}\n"
        content += f"Record Count: {export.record_count}\n"
        content += f"Created: {export.created_at}\n"
        content += f"Filters: {export.filters}\n\n"
        content += "Note: In a production environment, this would download the actual exported file."
        
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{export.filename}"'
        return response
        
    except ExportHistory.DoesNotExist:
        messages.error(request, "Export not found or you don't have permission to access it.")
        return redirect('appointment_export')
    except Exception as e:
        print(f"Download error: {e}")
        messages.error(request, "Error downloading export.")
        return redirect('appointment_export')
