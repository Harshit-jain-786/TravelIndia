
from django.db import models
from django.conf import settings

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='destination_photos/', blank=True, null=True)
    # New fields
    gallery = models.JSONField(blank=True, null=True, default=list, help_text="List of image URLs for gallery")
    coords = models.JSONField(blank=True, null=True, help_text="Coordinates as {lat: float, lng: float}")
    features = models.JSONField(blank=True, null=True, default=list, help_text="List of features (strings)")

    def __str__(self):
        return self.name

class Review(models.Model):
    destination = models.ForeignKey(Destination, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='destination_reviews', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for destination {self.destination.name} ({self.rating}/5)"
