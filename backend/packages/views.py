from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Review
from .serializers import PackageReviewSerializer
from rest_framework.exceptions import PermissionDenied

class PackageReviewListCreateView(generics.ListCreateAPIView):
	serializer_class = PackageReviewSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		package_id = self.kwargs["package_id"]
		return Review.objects.filter(package_id=package_id).order_by("-created_at")

	def perform_create(self, serializer):
		package_id = self.kwargs["package_id"]
		serializer.save(user=self.request.user, package_id=package_id)

class PackageReviewDeleteView(generics.DestroyAPIView):
	queryset = Review.objects.all()
	serializer_class = PackageReviewSerializer
	permission_classes = [IsAuthenticated]

	def delete(self, request, *args, **kwargs):
		review = self.get_object()
		if review.user != request.user:
			raise PermissionDenied("You can only delete your own review.")
		return super().delete(request, *args, **kwargs)
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Package
from .serializers import PackageSerializer

class PackageDetailView(generics.RetrieveAPIView):
	queryset = Package.objects.all()
	serializer_class = PackageSerializer
	permission_classes = [AllowAny]

class PackageListCreateView(generics.ListCreateAPIView):
	queryset = Package.objects.all()
	serializer_class = PackageSerializer
	permission_classes = [AllowAny]

# Create your views here.
