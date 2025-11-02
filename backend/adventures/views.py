from rest_framework import generics
from .models import Adventure
from .serializers import AdventureSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated

class AdventureListCreateView(generics.ListCreateAPIView):
    serializer_class = AdventureSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = Adventure.objects.all().order_by('-created_at')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset
