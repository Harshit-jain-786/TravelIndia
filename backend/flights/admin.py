from django.contrib import admin
from .models import Flight, Review

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'from_city', 'to_city', 'departure', 'arrival', 'price', 'flight_class', 'seats_available')
    list_filter = ('airline', 'flight_class', 'from_city', 'to_city')
    search_fields = ('flight_number', 'airline', 'from_city', 'to_city')
    date_hierarchy = 'departure'
    ordering = ('departure', 'airline')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('flight', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'flight__airline')
    search_fields = ('flight__flightNumber', 'user__username', 'text')
    readonly_fields = ('created_at',)
