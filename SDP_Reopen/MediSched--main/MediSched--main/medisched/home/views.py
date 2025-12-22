# home/views.py
from django.views.decorators.csrf import csrf_protect
from adminapp.models import Department, Symptom
from doctor.models import Doctor  # Add this import
# home/views.py - Add these imports at the top
from django.shortcuts import render, get_object_or_404
from adminapp.models import Department, Symptom
from doctor.models import Doctor, DoctorSpecializationDepartment  # Add Doctor import here too
# Add at the end of the file, before any other code
from django.shortcuts import render, get_object_or_404
from adminapp.models import Department
from doctor.models import DoctorSpecializationDepartment
# home/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg, Count
from adminapp.models import Department, Symptom
from doctor.models import (
    Doctor,
    DoctorExperience,
    DoctorSpecializationDepartment,
    DoctorSpecializationSymptom,
    DoctorAppointmentFee
)

# ... rest of the code ...

@csrf_protect
def home(request):
    """Main home page view with departments and symptoms"""
    departments = Department.objects.all()[:10]  
    symptoms = Symptom.objects.all()[:5]
    
    # Get featured doctors - optimized query
    featured_doctors = Doctor.objects.exclude(profile_image__isnull=True)[:4]\
        .select_related('user')\
        .prefetch_related('specialized_departments__department')[:4]

    context = {
        'page_title': 'MediSched+ | Modern Telemedicine Platform',
        'is_authenticated': request.user.is_authenticated,
        'user': request.user if request.user.is_authenticated else None,
        'departments': departments,
        'symptoms': symptoms,
        'featured_doctors': featured_doctors,
    }
    return render(request, 'home/index.html', context)


def department_detail(request, dept_id):
    """Show all doctors in a specific department"""
    # Get the department
    department = get_object_or_404(Department, id=dept_id)
    
    # Get all doctors specialized in this department
    specializations = DoctorSpecializationDepartment.objects.filter(
        department=department
    ).select_related('doctor', 'doctor__user')
    
    doctors = [spec.doctor for spec in specializations]
    
    context = {
        'department': department,
        'doctors': doctors,
        'doctor_count': len(doctors),
    }
    return render(request, 'home/department_detail.html', context)

# home/views.py - Add this function after department_detail()




def symptom_detail(request, symptom_id):
    """Show all doctors related to a specific symptom"""

    # Get symptom
    symptom = get_object_or_404(Symptom, id=symptom_id)

    # Get doctors specialized for this symptom
    specializations = DoctorSpecializationSymptom.objects.filter(
        symptom=symptom
    ).select_related(
        'doctor',
        'doctor__user',
        'doctor__division',
        'doctor__district',
        'doctor__upazila'
    ).prefetch_related(
        'doctor__specialized_departments__department',
        'doctor__appointment_fees'
    )

    doctors = [spec.doctor for spec in specializations]

    context = {
        'symptom': symptom,
        'doctors': doctors,
        'doctor_count': len(doctors),
    }

    return render(request, 'home/symptom_detail.html', context)





@csrf_protect
def home(request):
    """Main home page view with departments and symptoms"""
    departments = Department.objects.all()[:10]
    symptoms = Symptom.objects.all()[:5]
    
    # Get featured doctors - optimized query
    featured_doctors = Doctor.objects.exclude(profile_image__isnull=True)\
        .select_related('user')\
        .prefetch_related('specialized_departments__department')[:4]
    
    context = {
        'page_title': 'MediSched+ | Modern Telemedicine Platform',
        'is_authenticated': request.user.is_authenticated,
        'user': request.user if request.user.is_authenticated else None,
        'departments': departments,
        'symptoms': symptoms,
        'featured_doctors': featured_doctors,
    }
    
    return render(request, 'home/index.html', context)





def doctor_detail(request, doctor_id):
    """Show detailed information about a specific doctor"""
    # Get the doctor with all related data
    doctor = get_object_or_404(
        Doctor.objects.select_related('user', 'division', 'district', 'upazila')
        .prefetch_related('experiences', 'specialized_departments', 'specialized_symptoms', 'appointment_fees'),
        id=doctor_id
    )
    
    # Get related data
    experiences = DoctorExperience.objects.filter(doctor=doctor)
    specializations = DoctorSpecializationDepartment.objects.filter(doctor=doctor).select_related('department')
    symptoms = DoctorSpecializationSymptom.objects.filter(doctor=doctor).select_related('symptom')
    appointment_fees = DoctorAppointmentFee.objects.filter(doctor=doctor)
    
    context = {
        'doctor': doctor,
        'experiences': experiences,
        'specializations': specializations,
        'symptoms': symptoms,
        'appointment_fees': appointment_fees,
    }
    
    return render(request, 'home/doctor_detail.html', context)


def all_doctors(request):
    """Show all doctors with advanced filtering and search"""
    # Get all doctors with optimized queries
    doctors_list = Doctor.objects.select_related(
        'user', 'division', 'district', 'upazila'
    ).prefetch_related(
        'specialized_departments__department',
        'specialized_symptoms__symptom',
        'appointment_fees'
    ).order_by('-is_verified', 'user__first_name')  # FIXED: Removed '-rating'
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    location_filter = request.GET.get('location', '')
    experience_filter = request.GET.get('experience', '')
    sort_by = request.GET.get('sort', 'verified')  # CHANGED: default to 'verified' instead of 'rating'
    
    # Apply search filter
    if search_query:
        doctors_list = doctors_list.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(qualification__icontains=search_query) |
            Q(bmdc_number__icontains=search_query)
        )
    
    # Apply department filter
    if department_filter:
        doctors_list = doctors_list.filter(
            specialized_departments__department__id=department_filter
        )
    
    # Apply location filter
    if location_filter:
        doctors_list = doctors_list.filter(
            Q(division__id=location_filter) |
            Q(district__id=location_filter) |
            Q(upazila__id=location_filter)
        )
    
    # Apply experience filter
    if experience_filter:
        try:
            min_experience = int(experience_filter)
            doctors_list = doctors_list.filter(total_experience__gte=min_experience)
        except ValueError:
            pass
    
    # Apply sorting - FIXED: Updated sorting options
    if sort_by == 'verified':
        doctors_list = doctors_list.order_by('-is_verified', 'user__first_name')
    elif sort_by == 'experience':
        doctors_list = doctors_list.order_by('-total_experience', '-is_verified')
    elif sort_by == 'name':
        doctors_list = doctors_list.order_by('user__first_name', 'user__last_name')
    elif sort_by == 'fee_low':
        doctors_list = doctors_list.annotate(
            min_fee=Avg('appointment_fees__price')
        ).order_by('min_fee')
    elif sort_by == 'fee_high':
        doctors_list = doctors_list.annotate(
            max_fee=Avg('appointment_fees__price')
        ).order_by('-max_fee')
    
    # Get filter options for dropdowns
    departments = Department.objects.all().order_by('department_name')
    divisions = Doctor.objects.values_list('division__division_name', 'division__id').distinct()
    
    # Statistics
    total_doctors = doctors_list.count()
    verified_doctors = doctors_list.filter(is_verified=True).count()
    avg_experience = doctors_list.aggregate(avg_exp=Avg('total_experience'))['avg_exp'] or 0
    
    context = {
        'doctors': doctors_list,
        'departments': departments,
        'divisions': divisions,
        'search_query': search_query,
        'department_filter': department_filter,
        'location_filter': location_filter,
        'experience_filter': experience_filter,
        'sort_by': sort_by,
        'total_doctors': total_doctors,
        'verified_doctors': verified_doctors,
        'avg_experience': round(avg_experience, 1),
    }
    
    return render(request, 'home/all_doctors.html', context)
