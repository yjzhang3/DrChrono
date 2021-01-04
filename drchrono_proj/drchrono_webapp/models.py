from django.db import models
from django import forms

# login auth. model?

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

