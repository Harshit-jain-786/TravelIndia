from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Review
from .serializers import FlightReviewSerializer
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import AllowAny
from .models import Flight
from .serializers import FlightSerializer

class FlightReviewListCreateView(generics.ListCreateAPIView):
	serializer_class = FlightReviewSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		flight_id = self.kwargs["flight_id"]
		return Review.objects.filter(flight_id=flight_id).order_by("-created_at")

	def perform_create(self, serializer):
		flight_id = self.kwargs["flight_id"]
		serializer.save(user=self.request.user, flight_id=flight_id)

class FlightReviewDeleteView(generics.DestroyAPIView):
	queryset = Review.objects.all()
	serializer_class = FlightReviewSerializer
	permission_classes = [IsAuthenticated]

	def delete(self, request, *args, **kwargs):
		review = self.get_object()
		if review.user != request.user:
			raise PermissionDenied("You can only delete your own review.")
		return super().delete(request, *args, **kwargs)

from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncDate
from collections import defaultdict
from datetime import datetime, date

class FlightListCreateView(generics.ListCreateAPIView):
    serializer_class = FlightSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        now = timezone.now()
        # Keep flights that depart in the future OR departed within the last 24 hours
        cutoff = now - timedelta(hours=24)
        return Flight.objects.filter(departure__gte=cutoff).order_by('departure')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Get query parameters for filtering
        from_city = request.query_params.get('from_city', None)
        to_city = request.query_params.get('to_city', None)
        departure_date = request.query_params.get('departure_date', None)
        flight_class = request.query_params.get('flight_class', None)

        # Apply filters if provided
        if from_city:
            queryset = queryset.filter(from_city__icontains=from_city)
        if to_city:
            queryset = queryset.filter(to_city__icontains=to_city)
        if departure_date:
            try:
                departure_date = datetime.strptime(departure_date, '%Y-%m-%d').date()
                queryset = queryset.filter(departure__date=departure_date)
            except ValueError:
                pass
        if flight_class:
            queryset = queryset.filter(flight_class=flight_class)

        # Group flights by date
        flights_by_date = defaultdict(list)
        for flight in queryset:
            departure_date = flight.departure.date()
            serialized_flight = FlightSerializer(flight).data
            flights_by_date[departure_date.isoformat()].append(serialized_flight)

        # Sort dates and create final response
        sorted_dates = sorted(flights_by_date.keys())
        response_data = []
        
        for date_str in sorted_dates:
            flights = flights_by_date[date_str]
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            # Format the date for display
            formatted_date = {
                'date': date_str,
                'display_date': date_obj.strftime('%A, %B %d, %Y'),
                'flights_count': len(flights),
                'flights': flights
            }
            response_data.append(formatted_date)

        return Response(response_data)

class FlightDetailView(generics.RetrieveAPIView):
	queryset = Flight.objects.all()
	serializer_class = FlightSerializer
	permission_classes = [AllowAny]

# Create your views here.
