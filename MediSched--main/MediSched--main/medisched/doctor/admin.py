from django.contrib import admin
from .models import Doctor, DoctorExperience, DoctorSpecializationDepartment, DoctorSpecializationSymptom,DoctorAppointmentFee



# Register doctor-related models
admin.site.register(Doctor)
admin.site.register(DoctorExperience)
admin.site.register(DoctorSpecializationDepartment)
admin.site.register(DoctorSpecializationSymptom)
admin.site.register(DoctorAppointmentFee)

