from django.contrib import admin
from .models import Package, Review

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'duration', 'price', 'get_reviews_count')
    list_filter = ('category', 'duration')
    search_fields = ('name', 'description', 'inclusions')
    ordering = ('category', 'price')
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    get_reviews_count.short_description = 'Reviews Count'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'package__category')
    search_fields = ('package__name', 'user__username', 'text')
    readonly_fields = ('created_at',)
