from django.contrib import admin
from .models import Destination, Review

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_features_count', 'get_reviews_count')
    search_fields = ('name', 'description')
    list_filter = ('features',)
    
    def get_features_count(self, obj):
        return len(obj.features or [])
    get_features_count.short_description = 'Features Count'
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    get_reviews_count.short_description = 'Reviews Count'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'destination')
    search_fields = ('destination__name', 'user__username', 'text')
    readonly_fields = ('created_at',)
