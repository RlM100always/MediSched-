# core/models.py
from django.db import models

# লিঙ্গের জন্য
class Gender(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

# বিভাগ (Division)
class Division(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# জেলা (District)
class District(models.Model):
    name = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        unique_together = ('name', 'division')

    def __str__(self):
        return f"{self.name}, {self.division.name}"

# উপজেলা (Upazila)
class Upazila(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='upazilas')

    class Meta:
        unique_together = ('name', 'district')

    def __str__(self):
        return f"{self.name}, {self.district.name}"

# Department (ডিপার্টমেন্ট)
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='department_images/', blank=True, null=True)

    def __str__(self):
        return self.name

# Symptom (উপসর্গ)
class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='symptom_images/', blank=True, null=True)

    def __str__(self):
        return self.name
