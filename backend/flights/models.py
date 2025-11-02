

from django.db import models
from django.conf import settings
from django.utils import timezone

class Flight(models.Model):
	destination_image = models.ImageField(upload_to='destination_photos/', blank=True, null=True)
	flight_number = models.CharField(max_length=20)
	airline = models.CharField(max_length=100)
	from_city = models.CharField(max_length=100)
	to_city = models.CharField(max_length=100)
	from_airport_code = models.CharField(max_length=3)
	to_airport_code = models.CharField(max_length=3)
	departure = models.DateTimeField()
	duration = models.DurationField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	seats_available = models.PositiveIntegerField()
	flight_class = models.CharField(max_length=20)
	trip_type = models.CharField(max_length=10, default='round-trip')  # Changed to match frontend
	from_coords = models.CharField(max_length=50, blank=True, null=True)
	to_coords = models.CharField(max_length=50, blank=True, null=True)
	
	CITY_COORDS = {
		# Delhi
		"Delhi": [28.5562, 77.1000],
		"New Delhi": [28.5562, 77.1000],
		"DEL": [28.5562, 77.1000],
		# Mumbai
		"Mumbai": [19.0896, 72.8656],
		"Bombay": [19.0896, 72.8656],
		"BOM": [19.0896, 72.8656],
		# Bangalore
		"Bangalore": [13.1986, 77.7066],
		"Bengaluru": [13.1986, 77.7066],
		"BLR": [13.1986, 77.7066],
		# Chennai
		"Chennai": [13.0827, 80.2707],
		"MAA": [13.0827, 80.2707],
		# Kolkata
		"Kolkata": [22.6520, 88.4463],
		"Calcutta": [22.6520, 88.4463],
		"CCU": [22.6520, 88.4463],
		# Hyderabad
		"Hyderabad": [17.2403, 78.4294],
		"HYD": [17.2403, 78.4294],
		# Goa
		"Goa": [15.3803, 73.8352],
		"GOI": [15.3803, 73.8352],
		# Jaipur
		"Jaipur": [26.8288, 75.8093],
		"JAI": [26.8288, 75.8093],
		# Amritsar
		"Amritsar": [31.6340, 74.8723],
		"ATQ": [31.6340, 74.8723],
		# Ludhiana
		"Ludhiana": [30.9010, 75.8573],
		"LUH": [30.9010, 75.8573],
		# Chandigarh
		"Chandigarh": [30.7333, 76.7794],
		"IXC": [30.7333, 76.7794],
		# Jalandhar
		"Jalandhar": [31.3260, 75.5762],
		"JUC": [31.3260, 75.5762],
		# Patiala
		"Patiala": [30.3398, 76.3869],
		"IXP": [30.3398, 76.3869]
	}

	def save(self, *args, **kwargs):
		# Always update coordinates based on current city/airport values
		# Set from coordinates
		if self.from_city in self.CITY_COORDS:
			coords = self.CITY_COORDS[self.from_city]
			self.from_coords = f"{coords[0]},{coords[1]}"
		elif self.from_airport_code in self.CITY_COORDS:
			coords = self.CITY_COORDS[self.from_airport_code]
			self.from_coords = f"{coords[0]},{coords[1]}"
		
		# Set to coordinates
		if self.to_city in self.CITY_COORDS:
			coords = self.CITY_COORDS[self.to_city]
			self.to_coords = f"{coords[0]},{coords[1]}"
		elif self.to_airport_code in self.CITY_COORDS:
			coords = self.CITY_COORDS[self.to_airport_code]
			self.to_coords = f"{coords[0]},{coords[1]}"
		
		super().save(*args, **kwargs)
		
	@property
	def arrival(self):
		return self.departure + self.duration
		
	@property
	def is_available(self):
		return self.departure > timezone.now() and self.seats_available > 0
		
	def __str__(self):
		# human readable representation: flight number and route
		try:
			return f"{self.flight_number} - {self.from_city} to {self.to_city} ({self.departure.strftime('%Y-%m-%d %H:%M')})"
		except Exception:
			# fallback
			return f"{self.from_city} to {self.to_city}"

class Review(models.Model):
	flight = models.ForeignKey(Flight, related_name='reviews', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='flight_reviews', on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField(default=5)
	text = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Review by {self.user.username} for flight {self.flight} ({self.rating}/5)"

# Create your models here.
