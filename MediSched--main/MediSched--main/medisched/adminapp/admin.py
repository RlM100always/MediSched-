from django.contrib import admin
from .models import Division, District, Upazila, Department, Symptom

# Register your models here.
# Register your models here
admin.site.register(Division)
admin.site.register(District)
admin.site.register(Upazila)
admin.site.register(Department)
admin.site.register(Symptom)
