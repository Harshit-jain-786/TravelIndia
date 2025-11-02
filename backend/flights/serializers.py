from rest_framework import serializers
from .models import Review

class FlightReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username
        }

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'text', 'created_at']
from rest_framework import serializers
from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    arrival = serializers.DateTimeField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    duration_hours = serializers.SerializerMethodField()
    from_location = serializers.CharField(source='from_city')
    to_location = serializers.CharField(source='to_city')
    flightNumber = serializers.CharField(source='flight_number')
    from_coords = serializers.SerializerMethodField()
    to_coords = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = [
            'id', 'flightNumber', 'airline', 'from_location', 'to_location',
            'from_airport_code', 'to_airport_code', 'departure', 'arrival',
            'duration', 'duration_hours', 'price', 'seats_available',
            'flight_class', 'trip_type', 'from_coords', 'to_coords',
            'is_available', 'destination_image'
        ]
    
    def get_duration_hours(self, obj):
        minutes = obj.duration.total_seconds() / 60
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return f"{hours}h {mins}m"
    
    def get_from_coords(self, obj):
        if not obj.from_coords:
            return None
        try:
            lat, lon = obj.from_coords.split(',')
            return [float(lat), float(lon)]
        except (ValueError, AttributeError):
            return None
            
    def get_to_coords(self, obj):
        if not obj.to_coords:
            return None
        try:
            lat, lon = obj.to_coords.split(',')
            return [float(lat), float(lon)]
        except (ValueError, AttributeError):
            return None
