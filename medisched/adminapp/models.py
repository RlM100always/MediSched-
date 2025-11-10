from django.db import models

# Division model
class Division(models.Model):
    division_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.division_name


# District model
class District(models.Model):
    district_name = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        unique_together = ('district_name', 'division')

    def __str__(self):
        return f"{self.district_name} ({self.division.division_name})"


# Upazila model
class Upazila(models.Model):
    upazila_name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='upazilas')

    class Meta:
        unique_together = ('upazila_name', 'district')

    def __str__(self):
        return f"{self.upazila_name} ({self.district.district_name})"


# Department (Specialization)
class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    department_image = models.ImageField(upload_to='department/',  blank=True, null=True)

    def __str__(self):
        return self.department_name


# Symptom (Expertise)
class Symptom(models.Model):
    symptom_name = models.CharField(max_length=100, unique=True)
    symptom_image = models.ImageField(upload_to='symptoms/', blank=True, null=True)

    def __str__(self):
        return self.symptom_name

