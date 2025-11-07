# users/views.py
import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import CustomUser

@require_POST
def ajax_signup(request):
    """
    Expect JSON body:
    { "username": "...", "email":"...", "password":"...", "user_type":"patient" }
    Returns JSON: { success: bool, message: str, redirect: url }
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)

    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    user_type = data.get('user_type', CustomUser.ROLE_PATIENT)

    # Basic validation
    if not username or not email or not password:
        return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({'success': False, 'message': 'Username already taken.'}, status=400)

    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': 'Email already registered.'}, status=400)

    # Create user
    user = CustomUser.objects.create_user(username=username, email=email, password=password, role=user_type)
    user.save()

    # Auto login
    login(request, user)

    # Decide redirect based on role
    if user.is_doctor():
        redirect_url = 'users/doctor/dashboard/'
    elif user.is_platform_admin():
        redirect_url = 'users/admin/dashboard/'
    else:
        redirect_url = 'users/patient/dashboard/'

    return JsonResponse({'success': True, 'message': 'Account created successfully.', 'redirect': redirect_url})


@require_POST
def ajax_signin(request):
    """
    Expect JSON body: { "username": "...", "password":"..." }
    Returns JSON: { success: bool, message: str, redirect: url }
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)

    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return JsonResponse({'success': False, 'message': 'Username and password required.'}, status=400)

    # Try authenticate by username; optionally allow email login:
    user = authenticate(request, username=username, password=password)
    if user is None:
        # try email login
        try:
            u = CustomUser.objects.get(email=username)
            user = authenticate(request, username=u.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

    if user is not None:
        login(request, user)
        # Role-based redirect
        if user.is_doctor():
            redirect_url = 'users/doctor/dashboard/'
        elif user.is_platform_admin():
            redirect_url = 'users/admin/dashboard/'
        else:
            redirect_url = 'users/patient/dashboard/'

        return JsonResponse({'success': True, 'message': f'Welcome {user.username}!', 'redirect': redirect_url})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid credentials.'}, status=401)


@login_required
def patient_dashboard(request):
    # basic patient dashboard (render a template)
    if not request.user.is_patient():
        return redirect('/')  # or return 403
    return render(request, 'users/patient_dashboard.html')


@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor():
        return redirect('/')
    return render(request, 'users/doctor_dashboard.html')


@login_required
def platform_admin_dashboard(request):
    # This is NOT the Django admin site; it's your app-level admin
    if not request.user.is_platform_admin():
        return redirect('/')
    return render(request, 'users/admin_dashboard.html')


@login_required
def ajax_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logged out', 'redirect': '/'})
