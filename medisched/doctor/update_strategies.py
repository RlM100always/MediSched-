from abc import ABC, abstractmethod
from django.contrib import messages
from adminapp.models import Division, District, Upazila
from .models import Doctor

class UpdateStrategy(ABC):
    """Abstract base class for all update strategies."""
    @abstractmethod
    def update(self, request, doctor: Doctor):
        """Applies the specific update logic."""
        pass

class UserUpdateStrategy(UpdateStrategy):
    """Strategy for updating the CustomUser fields."""
    def update(self, request, doctor: Doctor):
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', getattr(user, 'phone', ''))
        user.save()
        messages.info(request, "User account details updated.")

class DoctorProfileUpdateStrategy(UpdateStrategy):
    """Strategy for updating the Doctor profile fields and image."""
    def update(self, request, doctor: Doctor):
        doctor.about = request.POST.get('about', doctor.about)
        doctor.qualification = request.POST.get('qualification', doctor.qualification)
        doctor.total_experience = request.POST.get('total_experience', doctor.total_experience)
        doctor.bmdc_number = request.POST.get('bmdc_number', doctor.bmdc_number)
        
        # Profile image upload
        if 'profile_image' in request.FILES:
            doctor.profile_image = request.FILES['profile_image']
        
        doctor.save()
        messages.info(request, "Doctor profile details updated.")

class LocationUpdateStrategy(UpdateStrategy):
    """Strategy for updating the location ForeignKeys (Division, District, Upazila)."""
    def update(self, request, doctor: Doctor):
        division_id = request.POST.get('division')
        district_id = request.POST.get('district')
        upazila_id = request.POST.get('upazila')

        # Safe ForeignKey assignment for Division
        try:
            doctor.division = Division.objects.get(id=division_id) if division_id else None
        except Division.DoesNotExist:
            doctor.division = None

        # Safe ForeignKey assignment for District
        try:
            doctor.district = District.objects.get(id=district_id) if district_id else None
        except District.DoesNotExist:
            doctor.district = None

        # Safe ForeignKey assignment for Upazila
        try:
            doctor.upazila = Upazila.objects.get(id=upazila_id) if upazila_id else None
        except Upazila.DoesNotExist:
            doctor.upazila = None

        doctor.save()
        messages.info(request, "Location details updated.")

class DoctorProfileEditContext:
    """The Context class that uses the strategies."""
    def __init__(self, strategies: list[UpdateStrategy]):
        self.strategies = strategies

    def execute_updates(self, request, doctor: Doctor):
        for strategy in self.strategies:
            strategy.update(request, doctor)
