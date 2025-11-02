
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	phone = models.CharField(max_length=20, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=10, blank=True)
	is_verified = models.BooleanField(default=False)
	otp_code = models.CharField(max_length=6, blank=True)

# Create your models here.
