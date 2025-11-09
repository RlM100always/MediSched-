from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from adminapp.models import Division, District, Upazila, Department, Symptom
from .models import Doctor


@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor_profile'):
        return redirect('/')  # Unauthorized access

    context = {
        'doctor_user': request.user,
        'upcoming_appointments_count': 5,
        'patients_today_count': 8,
        'earnings_today': 120,
        'total_reviews': 15,
        'upcoming_appointments': [
            {
                'patient': {'first_name': 'John', 'last_name': 'Doe'},
                'appointment_date': '2025-11-08',
                'appointment_time': '10:00 AM',
                'status': {'status_name': 'Pending'}
            },
        ]
    }
    return render(request, 'doctor/dashboard.html', context)


@login_required
def doctor_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    context = {'doctor': doctor}
    return render(request, 'doctor/profile.html', context)


@login_required
def doctor_profile_edit(request):
    # Get or create doctor profile
    doctor, created = Doctor.objects.get_or_create(user=request.user)

    # Load selectable options
    divisions = Division.objects.all()
    districts = District.objects.all()
    upazilas = Upazila.objects.all()
    departments = Department.objects.all()
    symptoms = Symptom.objects.all()

    if request.method == 'POST':
        # --- Update User fields ---
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', getattr(user, 'phone', ''))
        user.save()

        # --- Update Doctor profile fields ---
        doctor.about = request.POST.get('about', doctor.about)
        doctor.qualification = request.POST.get('qualification', doctor.qualification)
        doctor.total_experience = request.POST.get('total_experience', doctor.total_experience)
        doctor.bmdc_number = request.POST.get('bmdc_number', doctor.bmdc_number)

        # --- Safe ForeignKey assignment ---
        division_id = request.POST.get('division')
        district_id = request.POST.get('district')
        upazila_id = request.POST.get('upazila')

        try:
            doctor.division = Division.objects.get(id=division_id) if division_id else None
        except Division.DoesNotExist:
            doctor.division = None

        try:
            doctor.district = District.objects.get(id=district_id) if district_id else None
        except District.DoesNotExist:
            doctor.district = None

        try:
            doctor.upazila = Upazila.objects.get(id=upazila_id) if upazila_id else None
        except Upazila.DoesNotExist:
            doctor.upazila = None

        doctor.save()  # Save before ManyToMany assignment

        # --- Safe ManyToMany assignment ---
        dept_ids = request.POST.getlist('departments')
        sym_ids = request.POST.getlist('symptoms')

        valid_depts = Department.objects.filter(id__in=dept_ids)
        valid_syms = Symptom.objects.filter(id__in=sym_ids)

        doctor.departments.set(valid_depts)
        doctor.symptoms.set(valid_syms)

        # --- Profile image upload ---
        if 'profile_image' in request.FILES:
            doctor.profile_image = request.FILES['profile_image']
            doctor.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('doctor:profile_edit')

    # --- Context for template ---
    context = {
        'doctor': doctor,
        'divisions': divisions,
        'districts': districts,
        'upazilas': upazilas,
        'departments': departments,
        'symptoms': symptoms,
    }
    return render(request, 'doctor/profile_edit.html', context)






# --- AJAX endpoints ---
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
