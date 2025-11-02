from django.core.management.base import BaseCommand
from hotels.models import Hotel
from decimal import Decimal

class Command(BaseCommand):
    help = 'Creates sample hotel data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample hotels...')

        hotels_data = [
            {
                'name': 'The Taj Palace',
                'location': 'New Delhi',
                'star_rating': 5,
                'amenities': '''
                - Luxury Spa & Wellness Center
                - Multiple Fine Dining Restaurants
                - Outdoor Swimming Pool
                - 24/7 Room Service
                - Business Center
                - Concierge Services
                - Valet Parking
                - Free High-Speed WiFi
                - Fitness Center
                ''',
                'price_per_night': Decimal('15000.00')
            },
            {
                'name': 'The Oberoi Udaivilas',
                'location': 'Udaipur',
                'star_rating': 5,
                'amenities': '''
                - Lake View Rooms
                - Luxury Spa
                - Private Pool Suites
                - Traditional Cultural Shows
                - Boat Rides
                - Fine Dining
                - Butler Service
                - Yoga Classes
                - Heritage Walks
                ''',
                'price_per_night': Decimal('25000.00')
            },
            {
                'name': 'Leela Palace',
                'location': 'Bangalore',
                'star_rating': 5,
                'amenities': '''
                - Rooftop Pool
                - Multiple Restaurants
                - Spa & Wellness
                - Business Center
                - Airport Transfers
                - Executive Lounge
                - 24/7 Fitness Center
                - Art Gallery
                ''',
                'price_per_night': Decimal('18000.00')
            },
            {
                'name': 'Taj Malabar Resort',
                'location': 'Kochi',
                'star_rating': 4,
                'amenities': '''
                - Sea View Rooms
                - Ayurvedic Spa
                - Waterfront Dining
                - Pool
                - Traditional Dance Shows
                - Water Sports
                - Heritage Tours
                - Sunset Cruise
                ''',
                'price_per_night': Decimal('12000.00')
            },
            {
                'name': 'The Park Hotel',
                'location': 'Kolkata',
                'star_rating': 4,
                'amenities': '''
                - City Center Location
                - Nightclub
                - Multiple Restaurants
                - Spa Services
                - Meeting Rooms
                - Fitness Center
                - WiFi
                - Room Service
                ''',
                'price_per_night': Decimal('8000.00')
            },
            {
                'name': 'Ginger Hotel',
                'location': 'Mumbai',
                'star_rating': 3,
                'amenities': '''
                - Budget Friendly
                - Clean Rooms
                - Restaurant
                - Free WiFi
                - Business Center
                - 24/7 Reception
                - Laundry Service
                - Room Service
                ''',
                'price_per_night': Decimal('3000.00')
            },
            {
                'name': 'Orange County Resort',
                'location': 'Coorg',
                'star_rating': 4,
                'amenities': '''
                - Coffee Estate Tours
                - Infinity Pool
                - Spa & Ayurveda Center
                - Nature Walks
                - Bird Watching
                - Traditional Cuisine
                - Eco-Friendly
                - Adventure Activities
                ''',
                'price_per_night': Decimal('15000.00')
            }
        ]

        for hotel_data in hotels_data:
            hotel = Hotel.objects.create(
                name=hotel_data['name'],
                location=hotel_data['location'],
                star_rating=hotel_data['star_rating'],
                amenities=hotel_data['amenities'],
                price_per_night=hotel_data['price_per_night']
            )
            self.stdout.write(f'Created hotel: {hotel.name} in {hotel.location}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample hotels'))