from abc import ABC, abstractmethod
from .models import Doctor
# from users.models import Patient # Assuming a Patient model exists in users app

class ProfileFactory(ABC):
    """Abstract Creator: Defines the factory method."""
    @abstractmethod
    def get_or_create_profile(self, user):
        """Factory Method: Returns a profile object (Doctor, Patient, etc.)."""
        pass

class DoctorProfileFactory(ProfileFactory):
    """Concrete Creator: Implements the factory method for Doctor profiles."""
    def get_or_create_profile(self, user):
        # The 'product' is the Doctor object
        doctor, created = Doctor.objects.get_or_create(user=user)
        return doctor, created

# class PatientProfileFactory(ProfileFactory):
#     """Concrete Creator: Implements the factory method for Patient profiles."""
#     def get_or_create_profile(self, user):
#         # The 'product' is the Patient object
#         patient, created = Patient.objects.get_or_create(user=user)
#         return patient, created
