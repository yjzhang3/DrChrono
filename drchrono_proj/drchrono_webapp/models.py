from django.db import models
from django import forms
from jsonfield import JSONField

class PatientInformation(models.Model):
    patient_first_name = models.CharField(max_length=100)
    patient_last_name = models.CharField(max_length=100)
    patient_data_json = JSONField(default={})

    def __str__(self):
        return (self.patient_first_name + ' ' + self.patient_last_name)

class DoctorInformation(models.Model):
    doctor_id = models.IntegerField()
    doctor_first_name = models.CharField(max_length=100)
    doctor_last_name = models.CharField(max_length=100)
    doctor_data_json = JSONField(default={})

    def __str__(self):
        return (self.doctor_id + ': ' + self.doctor_first_name + ' ' + self.doctor_last_name)