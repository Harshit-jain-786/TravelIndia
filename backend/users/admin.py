from django.contrib import admin
from .models import User
from .contactmodels import ContactMessage

admin.site.register(User)
admin.site.register(ContactMessage)
