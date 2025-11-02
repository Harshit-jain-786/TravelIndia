import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import hmac
import hashlib

class CreateRazorpayOrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount = request.data.get('amount')
        order = client.order.create({
            'amount': int(amount),
            'currency': 'INR',
            'payment_capture': 1
        })
        return Response(order)

@method_decorator(csrf_exempt, name='dispatch')
class VerifyRazorpayPaymentView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        payment_id = request.data.get('razorpay_payment_id')
        order_id = request.data.get('razorpay_order_id')
        signature = request.data.get('razorpay_signature')
        key_secret = settings.RAZORPAY_KEY_SECRET
        generated_signature = hmac.new(
            key_secret.encode(),
            (order_id + '|' + payment_id).encode(),
            hashlib.sha256
        ).hexdigest()
        if generated_signature == signature:
            # Payment verified, create booking here
            from .models import Booking
            from .serializers import BookingSerializer
            from django.contrib.auth import get_user_model
            user_id = request.data.get('userId')
            booking_type = request.data.get('bookingType')
            package_id = request.data.get('packageId')
            flight_id = request.data.get('flightId')
            hotel_id = request.data.get('hotelId')
            number_of_travelers = request.data.get('numberOfTravelers', 1)
            total_amount = request.data.get('totalAmount')
            # Find user
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'success': False, 'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            booking = Booking.objects.create(
                user=user,
                package_id=package_id if booking_type == 'package' else None,
                flight_id=flight_id if booking_type == 'flight' else None,
                hotel_id=hotel_id if booking_type == 'hotel' else None,
                status='confirmed',
            )
            serializer = BookingSerializer(booking)
            return Response({'success': True, 'bookingId': booking.id, 'booking': serializer.data})
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
