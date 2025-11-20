from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from adminapp.models import Department, Symptom  # admin app এর model import

@csrf_protect
def home(request):
    """Main home page view with departments and symptoms"""
    departments = Department.objects.all()[:10]  
    symptoms = Symptom.objects.all()[:5]       

    context = {
        'page_title': 'MediSched+ | Modern Telemedicine Platform',
        'is_authenticated': request.user.is_authenticated,
        'user': request.user if request.user.is_authenticated else None,
        'departments': departments,
        'symptoms': symptoms,
    }
    return render(request, 'home/index.html', context)
