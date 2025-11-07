from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Gender, Division, District, Upazila, Department, Symptom
from .models import Doctor
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor():
        return redirect('/')  # Unauthorized access

    # Example data: Replace with actual queries
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
    doctor = get_object_or_404(Doctor, doctor_user=request.user)
    context = {
        'doctor': doctor
    }
    return render(request, 'doctor/profile.html', context)

@login_required
def doctor_profile_edit(request):
    # যদি Doctor record না থাকে, auto-create হবে
    doctor, created = Doctor.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.phone = request.POST.get('phone', getattr(request.user, 'phone', ''))
        request.user.save()

        doctor.about = request.POST.get('about', doctor.about)
        doctor.qualification = request.POST.get('qualification', doctor.qualification)
        doctor.total_experience = request.POST.get('total_experience', doctor.total_experience)
        doctor.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('doctor:profile_edit')

    context = {
        'doctor_user': request.user,
        'doctor_profile': doctor,
    }
    return render(request, 'doctor/profile_edit.html', context)
