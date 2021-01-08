from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DoctorInformation, PatientInformation

# register models
admin.site.register(DoctorInformation)
admin.site.register(PatientInformation)