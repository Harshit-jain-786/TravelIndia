

from django.db import models
from django.conf import settings

class Package(models.Model):
	name = models.CharField(max_length=100)
	category = models.CharField(max_length=50)
	duration = models.IntegerField(help_text="Number of days")
	inclusions = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	description = models.TextField(blank=True)
	photo = models.ImageField(upload_to='package_photos/', blank=True, null=True)

	def __str__(self):
		return self.name

class Review(models.Model):
	package = models.ForeignKey(Package, related_name='reviews', on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='package_reviews', on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField(default=5)
	text = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Review by {self.user.username} for package {self.package.name} ({self.rating}/5)"

# Create your models here.
