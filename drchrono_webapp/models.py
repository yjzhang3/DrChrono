from django.db import models
from django import forms
from jsonfield import JSONField

class DoctorInformation(models.Model):
    doctor_data_json = JSONField(default={})

    def __str__(self):
        return (f'{self.doctor_data_json.id} {self.doctor_data_json.first_name} {self.doctor_data_json.last_name}')

class PatientInformation(models.Model):
    doctor = models.ForeignKey(DoctorInformation, on_delete=models.CASCADE, default=JSONField(default={}))
    patient_data_json = JSONField(default={})

    def __str__(self):
        return (f'{self.patient_data_json.first_name} {self.patient_data_json.last_name}')