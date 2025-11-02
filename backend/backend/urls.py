from packages.views import PackageReviewListCreateView, PackageReviewDeleteView
from destinations.views import DestinationReviewListCreateView, DestinationReviewDeleteView
from flights.views import FlightReviewListCreateView, FlightReviewDeleteView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from flights.views import FlightListCreateView, FlightDetailView
from hotels.views import HotelListCreateView, HotelDetailView, HotelReviewListCreateView, HotelReviewDeleteView
from packages.views import PackageListCreateView, PackageDetailView
from destinations.views import DestinationListCreateView, DestinationDetailView
from bookings.views import BookingListCreateView, UserBookingsView
from users.views import UserListCreateView, RegisterView, LoginView, VerifyOTPView
from .search import GlobalSearchView
from users.contactviews import ContactMessageView
from users.views import ForgotPasswordRequestView, ForgotPasswordVerifyView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/', admin.site.urls),
    path('api/flights/', FlightListCreateView.as_view(), name='flight-list-create'),
    path('api/flights/<int:pk>/', FlightDetailView.as_view(), name='flight-detail'),
    path('api/hotels/', HotelListCreateView.as_view(), name='hotel-list-create'),
    path('api/hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),
    path('api/hotels/<int:hotel_id>/reviews/', HotelReviewListCreateView.as_view(), name='hotel-reviews'),
    path('api/hotels/reviews/<int:pk>/', HotelReviewDeleteView.as_view(), name='hotel-review-delete'),
    path('api/packages/', PackageListCreateView.as_view(), name='package-list-create'),
    path('api/packages/<int:pk>/', PackageDetailView.as_view(), name='package-detail'),
    path('api/packages/<int:package_id>/reviews/', PackageReviewListCreateView.as_view(), name='package-reviews'),
    path('api/packages/reviews/<int:pk>/', PackageReviewDeleteView.as_view(), name='package-review-delete'),
    path('api/destinations/', DestinationListCreateView.as_view(), name='destination-list-create'),
    path('api/destinations/<int:pk>/', DestinationDetailView.as_view(), name='destination-detail'),
    path('api/destinations/<int:destination_id>/reviews/', DestinationReviewListCreateView.as_view(), name='destination-reviews'),
    path('api/destinations/reviews/<int:pk>/', DestinationReviewDeleteView.as_view(), name='destination-review-delete'),
    path('api/flights/<int:flight_id>/reviews/', FlightReviewListCreateView.as_view(), name='flight-reviews'),
    path('api/flights/reviews/<int:pk>/', FlightReviewDeleteView.as_view(), name='flight-review-delete'),
    path('api/bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path('api/users/<int:user_id>/bookings', UserBookingsView.as_view(), name='user-bookings'),
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/register', RegisterView.as_view(), name='user-register'),
    path('api/users/login', LoginView.as_view(), name='user-login'),
    path('api/users/verify-otp', VerifyOTPView.as_view(), name='user-verify-otp'),
    path('api/search/', GlobalSearchView.as_view(), name='global-search'),
    path('api/contact', ContactMessageView.as_view(), name='contact-message'),
    path('api/users/forgot-password-request/', ForgotPasswordRequestView.as_view(), name='forgot-password-request'),
    path('api/users/forgot-password-verify/', ForgotPasswordVerifyView.as_view(), name='forgot-password-verify'),
    path('api/adventures/', __import__('adventures.views').views.AdventureListCreateView.as_view(), name='adventure-list-create'),
]
# Serve media files in development
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
