from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Review, Destination
from .serializers import DestinationReviewSerializer
from rest_framework.exceptions import PermissionDenied

class DestinationReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = DestinationReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        destination_id = self.kwargs["destination_id"]
        return Review.objects.filter(destination_id=destination_id).order_by("-created_at")

    def perform_create(self, serializer):
        destination_id = self.kwargs["destination_id"]
        try:
            destination = Destination.objects.get(id=destination_id)
            serializer.save(user=self.request.user, destination=destination)
        except Destination.DoesNotExist:
            raise serializers.ValidationError("Destination not found")

class DestinationReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = DestinationReviewSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            raise PermissionDenied("You can only delete your own review.")
        return super().delete(request, *args, **kwargs)

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Destination
from .serializers import DestinationSerializer
from django.conf import settings
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

@method_decorator(ensure_csrf_cookie, name='dispatch')
class DestinationDetailView(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if settings.DEBUG:
            context.update({'request': self.request})
        return context

class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]
