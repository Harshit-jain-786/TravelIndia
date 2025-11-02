from rest_framework import serializers
from .models import Review

class PackageReviewSerializer(serializers.ModelSerializer):
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
from .models import Package

class PackageSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    originalPrice = serializers.SerializerMethodField()
    shortDescription = serializers.SerializerMethodField()
    inclusions = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'category', 'duration', 'inclusions', 'price', 'description', 'photo',
            'rating', 'originalPrice', 'shortDescription'
        ]

    def get_rating(self, obj):
        return 4.5

    def get_originalPrice(self, obj):
        try:
            return float(obj.price) * 1.1 if obj.price else None
        except Exception:
            return None

    def get_shortDescription(self, obj):
        if obj.description:
            return obj.description[:100] + ('...' if len(obj.description) > 100 else '')
        return ''

    def get_inclusions(self, obj):
        if not obj.inclusions:
            return []
        try:
            import json
            val = json.loads(obj.inclusions)
            if isinstance(val, list):
                return val
        except Exception:
            pass
        return [a.strip() for a in obj.inclusions.split(',') if a.strip()]

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
