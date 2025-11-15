from django.db import models
from users.models import CustomUser
from adminapp.models import  Division, District, Upazila, Department, Symptom


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    about = models.TextField(blank=True, null=True)
    bmdc_number = models.CharField(max_length=255, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    total_experience = models.PositiveIntegerField(default=0)  # Only non-negative numbers
    working_hours = models.JSONField(blank=True, null=True)  # e.g., {"Mon": "9-5", "Tue": "10-4"}
    profile_image = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    # ForeignKeys with NULL support to prevent IntegrityError
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    upazila = models.ForeignKey(Upazila, on_delete=models.SET_NULL, null=True, blank=True)

    # Optional: use ManyToMany through intermediate tables
    departments = models.ManyToManyField(Department, through='DoctorSpecializationDepartment', blank=True)
    symptoms = models.ManyToManyField(Symptom, through='DoctorSpecializationSymptom', blank=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class DoctorExperience(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='experiences')
    hospital_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.doctor.user.first_name} - {self.hospital_name}"


class DoctorSpecializationDepartment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='specialized_departments')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('doctor', 'department')  # Prevent duplicates

    def __str__(self):
        return f"{self.doctor.user.first_name} - {self.department.department_name}"


class DoctorSpecializationSymptom(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='specialized_symptoms')
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('doctor', 'symptom')  # Prevent duplicates

    def __str__(self):
        return f"{self.doctor.user.first_name} - {self.symptom.symptom_name}"


class DoctorAppointmentFee(models.Model):
    """
    Represents the fee a doctor charges for a predefined appointment category.
    """
    APPOINTMENT_CATEGORIES = [
        ('General', 'General Consultation'),
        ('Special', 'Special Consultation'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment_fees')
    category = models.CharField(max_length=50, choices=APPOINTMENT_CATEGORIES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('doctor', 'category')  # Prevent duplicates

    def __str__(self):
        return f"{self.doctor.user.username} - {self.category} : {self.price}"
