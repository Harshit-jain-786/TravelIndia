from rest_framework import serializers
from .models import Adventure

class AdventureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adventure
        fields = '__all__'
