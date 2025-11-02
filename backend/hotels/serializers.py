
from rest_framework import serializers
from .models import Hotel, Review, Room

class RoomSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = ['id', 'type', 'description', 'price', 'max_guests', 'image']
        
    def get_image(self, obj):
        request = self.context.get('request')
        try:
            if obj.image and hasattr(obj.image, 'url'):
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
        except Exception:
            pass
        return None


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'text', 'created_at']

class HotelSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'description', 'location', 'star_rating',
            'price_per_night', 'photo', 'gallery', 'reviews', 'rooms',
            'average_rating', 'total_reviews', 'email', 'phone',
            'website', 'policies', 'amenities', 'landmarks'
        ]
        
    def get_photo(self, obj):
        request = self.context.get('request')
        try:
            if obj.photo and hasattr(obj.photo, 'url'):
                if request:
                    return request.build_absolute_uri(obj.photo.url)
                return obj.photo.url
        except Exception:
            pass
        return None
        
    def get_average_rating(self, obj):
        return obj.average_rating
        
    def get_total_reviews(self, obj):
        return obj.reviews.count()
