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
            user_type = data.get('user_type', 'patient')
            
            # Validation
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already registered'})
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # TODO: Create associated patient/doctor profile based on user_type
            # This should link to your patients or doctors app models
            
            login(request, user)
            return JsonResponse({
                'success': True, 
                'message': 'Account created successfully!',
                'redirect': '/dashboard/'  # Change based on user type
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
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect': '/dashboard/'  # Change based on user role
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
    return redirect('home')