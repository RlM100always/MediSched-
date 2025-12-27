from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .forms import CustomUserSignupForm, CustomUserSigninForm
from django.views.decorators.cache import cache_control
from appointment.models import Appointment
from django.utils import timezone
from appointment.models import Appointment
from datetime import timedelta
import json



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def edit_profile(request):
    if not request.user.is_patient():
        return redirect("users:signin")
    
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:patient_dashboard')
    else:
        form = CustomUserEditForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})


# -----------------------------
# SIGNUP VIEW
# -----------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup_view(request):
    if request.user.is_authenticated:
        # Already logged in user redirect
        return redirect("users:doctor_dashboard" if request.user.is_doctor() else "users:patient_dashboard")

    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account is ready!")
            return redirect("users:doctor_dashboard" if user.is_doctor() else "users:patient_dashboard")
        messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserSignupForm()

    return render(request, "users/signup.html", {"form": form})


# -----------------------------
# SIGNIN VIEW
# -----------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin_view(request):
    if request.user.is_authenticated:
        # Already logged in user redirect
        return redirect("users:doctor_dashboard" if request.user.is_doctor() else "users:patient_dashboard")

    if request.method == "POST":
        form = CustomUserSigninForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect("users:doctor_dashboard" if user.is_doctor() else "users:patient_dashboard")
        messages.error(request, "Incorrect username/email or password.")
    else:
        form = CustomUserSigninForm()

    return render(request, "users/signin.html", {"form": form})




# -----------------------------
# DASHBOARDS
# -----------------------------
# -----------------------------
# DASHBOARDS
# -----------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def patient_dashboard(request):
    if not request.user.is_patient():
        return redirect("users:signin")
    
    # Get all appointments for the patient
    appointments = Appointment.objects.filter(patient=request.user).select_related(
        'doctor', 'doctor__user'
    ).prefetch_related('doctor__departments').order_by('-appointment_date')
    
    # Get statistics
    total_appointments = appointments.count()
    completed_count = appointments.filter(status='completed').count()
    pending_count = appointments.filter(status__in=['pending', 'confirmed']).count()
    cancelled_count = appointments.filter(status='cancelled').count()
    
    # Get upcoming appointments (next 7 days)
    today = timezone.now()
    next_week = today + timedelta(days=7)
    upcoming_appointments = appointments.filter(
        appointment_date__gte=today,
        appointment_date__lte=next_week,
        status__in=['pending', 'confirmed']
    ).order_by('appointment_date')[:5]  # Limit to 5 upcoming appointments
    
    # Create recent activity
    recent_activity = []
    
    # Add recent appointments to activity
    recent_appointments = appointments[:3]
    for appointment in recent_appointments:
        recent_activity.append({
            'type': 'appointment',
            'title': f'Appointment with Dr. {appointment.doctor.user.get_full_name()}',
            'description': f'{appointment.get_status_display()} - {appointment.get_appointment_type_display()}',
            'date': appointment.created_at
        })
    
    # Add payment activities
    paid_appointments = appointments.filter(payment_status='paid')[:2]
    for appointment in paid_appointments:
        recent_activity.append({
            'type': 'payment',
            'title': 'Payment Completed',
            'description': f'৳{appointment.total_amount} for appointment #{appointment.id}',
            'date': appointment.updated_at
        })
    
    # Sort recent activity by date
    recent_activity.sort(key=lambda x: x['date'], reverse=True)
    
    context = {
        'total_appointments': total_appointments,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
        'upcoming_appointments': upcoming_appointments,
        'recent_activity': recent_activity[:5],  # Limit to 5 activities
        'current_date': timezone.now(),
    }
    
    return render(request, "users/patient_dashboard.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor():
        return redirect("users:signin")
    return render(request, "doctor/dashboard.html")


# -----------------------------
# LOGOUT VIEW
# -----------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("users:signin")

    # Prevent logout via GET
    return redirect("users:signin")
