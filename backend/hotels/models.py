from django.db import models
from django.conf import settings
from django.db.models import Avg

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    star_rating = models.IntegerField(default=3)
    amenities = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='hotel_photos/', blank=True, null=True)
    gallery = models.TextField(blank=True, null=True)  # Store JSON as text
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    policies = models.TextField(blank=True, null=True)  # Store JSON as text
    landmarks = models.TextField(blank=True, null=True)  # Store JSON as text

    def __str__(self):
        return f"{self.name} ({self.location})"
        
    @property
    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg']

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveSmallIntegerField(default=2)
    image = models.ImageField(upload_to='room_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.type} at {self.hotel.name}"

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='hotel_reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.hotel.name} ({self.rating}/5)"
