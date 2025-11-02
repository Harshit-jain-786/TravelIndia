from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from hotels.models import Hotel
from hotels.serializers import HotelSerializer
from packages.models import Package
from packages.serializers import PackageSerializer
from destinations.models import Destination
from destinations.serializers import DestinationSerializer
from flights.models import Flight
from flights.serializers import FlightSerializer
from django.db.models import Q

class GlobalSearchView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.GET.get('q', '').strip()
        if not query:
            return Response({'results': []})

        hotels = Hotel.objects.filter(name__icontains=query)
        packages = Package.objects.filter(name__icontains=query)
        destinations = Destination.objects.filter(name__icontains=query)
        # Search across multiple flight fields that exist on the Flight model.
        # The original code referenced `from_location` and `to_location` which do not exist
        # on the model and caused a FieldError.
        flights = Flight.objects.filter(
            Q(from_city__icontains=query)
            | Q(to_city__icontains=query)
            | Q(from_airport_code__icontains=query)
            | Q(to_airport_code__icontains=query)
            | Q(flight_number__icontains=query)
            | Q(airline__icontains=query)
        )

        return Response({
            'hotels': HotelSerializer(hotels, many=True, context={'request': request}).data,
            'packages': PackageSerializer(packages, many=True, context={'request': request}).data,
            'destinations': DestinationSerializer(destinations, many=True, context={'request': request}).data,
            'flights': FlightSerializer(flights, many=True, context={'request': request}).data,
        }, status=status.HTTP_200_OK)
