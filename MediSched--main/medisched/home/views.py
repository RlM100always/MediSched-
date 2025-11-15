# home/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json

@csrf_protect
def home(request):
    """Main home page view"""
    context = {
        'page_title': 'MediSched+ | Modern Telemedicine Platform',
        'is_authenticated': request.user.is_authenticated,
        'user': request.user if request.user.is_authenticated else None
    }
    return render(request, 'home/index.html', context)


@csrf_protect
def signup_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            user_type = data.get('user_type', 'patient')  # default patient

            # Validation
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})
            
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already registered'})

            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=user_type
            )

            login(request, user)

            # Redirect based on role
            if user.is_doctor():
                redirect_url = '/users/doctor/dashboard/'
            elif user.is_patient():
                redirect_url = '/patient/dashboard/'
            else:
                redirect_url = '/admin/'

            return JsonResponse({
                'success': True,
                'message': 'Account created successfully!',
                'redirect': redirect_url
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@csrf_protect
def signin_view(request):
    """Handle user login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # ✅ redirect based on role
                if user.is_doctor():
                    redirect_url = '/users/doctor/dashboard/'
                elif user.is_patient():
                    redirect_url = '/patient/dashboard/'
                elif user.is_platform_admin():
                    redirect_url = '/admin/'
                else:
                    redirect_url = '/'

                return JsonResponse({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect': redirect_url
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid username or password'
                })

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home:home')
