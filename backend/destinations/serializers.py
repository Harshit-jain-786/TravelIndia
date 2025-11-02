from rest_framework import serializers
from .models import Review

class DestinationReviewSerializer(serializers.ModelSerializer):
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
from .models import Destination


class DestinationSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    reviews = DestinationReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = ['id', 'name', 'description', 'image', 'gallery', 'coords', 'features', 'reviews', 'rating']

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

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return None
