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

