from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .forms import CustomUserSignupForm, CustomUserSigninForm
from django.views.decorators.cache import cache_control


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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def patient_dashboard(request):
    if not request.user.is_patient():
        return redirect("users:signin")
    return render(request, "users/patient_dashboard.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor():
        return redirect("users:signin")
    return render(request, "doctor/dashboard.html")