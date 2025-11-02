from django.contrib import admin
from .models import Hotel, Review

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'star_rating', 'price_per_night', 'get_reviews_count')
    list_filter = ('star_rating', 'location')
    search_fields = ('name', 'location', 'amenities')
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    get_reviews_count.short_description = 'Reviews Count'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'hotel')
    search_fields = ('hotel__name', 'user__username', 'text')
    readonly_fields = ('created_at',)
