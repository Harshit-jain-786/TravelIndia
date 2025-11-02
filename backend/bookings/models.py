
from django.db import models
from flights.models import Flight
from hotels.models import Hotel
from packages.models import Package
from django.contrib.auth import get_user_model

class Booking(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True)
	hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
	package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
	booking_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=20, default='pending')

	def __str__(self):
		return f"Booking {self.id} by {self.user}"

# Create your models here.
