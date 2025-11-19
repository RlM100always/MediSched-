from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserSignupForm, CustomUserSigninForm


# -----------------------------
# SIMPLE SIGNUP (NO AJAX)
# -----------------------------
def signup_view(request):
    if request.method == "POST":
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account is ready!")

            # Redirect based on role
            if user.is_doctor():
                return redirect("users:doctor_dashboard")

            return redirect("users:patient_dashboard")

        messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserSignupForm()

    return render(request, "users/signup.html", {"form": form})


# -----------------------------
# SIMPLE SIGNIN (NO AJAX)
# -----------------------------
def signin_view(request):
    if request.method == "POST":
        form = CustomUserSigninForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back!")

            if user.is_doctor():
                return redirect("doctor:doctor_dashboard")

            return redirect("users:patient_dashboard")

        messages.error(request, "Incorrect username or password.")
    else:
        form = CustomUserSigninForm()

    return render(request, "users/signin.html", {"form": form})


# -----------------------------
# LOGOUT
# -----------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home:home")


# -----------------------------
# DASHBOARDS
# -----------------------------
@login_required
def patient_dashboard(request):
    if not request.user.is_patient():
        return redirect("home:home")
    return render(request, "users/patient_dashboard.html")


@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor():
        return redirect("home:home")
    return render(request, "doctor/doctor_dashboard.html")
