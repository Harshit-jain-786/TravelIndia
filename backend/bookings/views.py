
from rest_framework import generics
from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateView(generics.ListCreateAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserBookingsView(APIView):
	permission_classes = [AllowAny]

	def get(self, request, user_id):
		bookings = Booking.objects.filter(user_id=user_id)
		serializer = BookingSerializer(bookings, many=True)
		return Response(serializer.data)
