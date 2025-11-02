from django.core.management.base import BaseCommand
from packages.models import Package
from decimal import Decimal

class Command(BaseCommand):
    help = 'Creates sample package data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample packages...')

        packages_data = [
            {
                'name': 'Kashmir Paradise Tour',
                'category': 'Hill Stations',
                'duration': 7,
                'price': Decimal('42000.00'),
                'description': '''Experience the heaven on earth with our comprehensive Kashmir tour package. Visit the beautiful Dal Lake, Mughal Gardens, and enjoy a shikara ride. Perfect for nature lovers and photography enthusiasts.''',
                'inclusions': '''
                - 6 nights luxury accommodation
                - Daily breakfast and dinner
                - Shikara ride on Dal Lake
                - Gulmarg Gondola tickets
                - Pahalgam sightseeing
                - Local guide services
                - All transfers in luxury vehicle
                - Airport pickup and drop
                - Welcome drink on arrival
                - All applicable taxes
                '''
            },
            {
                'name': 'Punjabi Heritage Trail',
                'category': 'Cultural',
                'duration': 5,
                'price': Decimal('25000.00'),
                'description': '''Immerse yourself in the rich culture of Punjab. Visit the Golden Temple, witness the Wagah Border ceremony, and experience the vibrant Punjabi lifestyle and cuisine.''',
                'inclusions': '''
                - 4 nights accommodation in heritage hotels
                - All meals with authentic Punjabi cuisine
                - Golden Temple visit with guide
                - Wagah Border ceremony
                - Jallianwala Bagh visit
                - Traditional village tour
                - Folk dance performance
                - All transfers and sightseeing
                - Expert guide services
                - Travel insurance
                '''
            },
            {
                'name': 'Mumbai City Explorer',
                'category': 'Cultural',
                'duration': 4,
                'price': Decimal('28000.00'),
                'description': '''Discover the city that never sleeps. Experience the vibrant culture, historic landmarks, and bustling streets of Mumbai, from Bollywood to colonial heritage.''',
                'inclusions': '''
                - 3 nights in premium hotel
                - Daily breakfast
                - Bollywood studio tour
                - Gateway of India visit
                - Dharavi cultural walk
                - Evening Marine Drive tour
                - Elephanta Caves excursion
                - Local train experience
                - Street food tour
                - Airport transfers
                '''
            },
            {
                'name': 'Kolkata Heritage Tour',
                'category': 'Cultural',
                'duration': 4,
                'price': Decimal('24000.00'),
                'description': '''Experience the cultural capital of India. Explore colonial architecture, taste Bengali cuisine, and immerse yourself in the city's rich artistic heritage.''',
                'inclusions': '''
                - 3 nights in boutique hotel
                - Daily breakfast with Bengali sweets
                - Victoria Memorial tour
                - Howrah Bridge visit
                - Tram ride experience
                - Bengali cooking class
                - Durga Puja workshop (seasonal)
                - Kolkata street food tour
                - Cultural performance
                - All transfers and guide services
                '''
            },
            {
                'name': 'Golden Triangle Tour',
                'category': 'Cultural',
                'duration': 6,
                'price': Decimal('35000.00'),
                'description': '''Experience the rich history and culture of India's famous Golden Triangle. Visit Delhi's historic monuments, Agra's magnificent Taj Mahal, and Jaipur's majestic palaces and forts. Perfect for first-time visitors to India.''',
                'inclusions': '''
                - 5 nights accommodation in 4-star hotels
                - Daily breakfast and dinner
                - Air-conditioned private vehicle
                - Professional English-speaking guide
                - All monument entrance fees
                - Airport transfers
                - Welcome drink on arrival
                - All applicable taxes
                '''
            },
            {
                'name': 'Kerala Backwaters Bliss',
                'category': 'Nature',
                'duration': 5,
                'price': Decimal('28000.00'),
                'description': '''Discover the serene beauty of Kerala's backwaters. Experience traditional houseboat stays, ayurvedic treatments, pristine beaches, and lush green landscapes. A perfect escape into nature's paradise.''',
                'inclusions': '''
                - 4 nights accommodation (2 nights in hotel, 2 nights in houseboat)
                - All meals included
                - Houseboat cruise
                - Ayurvedic massage session
                - Cultural performance
                - Spice plantation tour
                - Airport transfers
                - Local English-speaking guide
                '''
            },
            {
                'name': 'Royal Rajasthan Adventure',
                'category': 'Adventure',
                'duration': 8,
                'price': Decimal('45000.00'),
                'description': '''Explore the royal heritage of Rajasthan combined with desert adventures. Visit majestic forts, experience desert camping, enjoy camel safaris, and witness the vibrant culture of the state.''',
                'inclusions': '''
                - 7 nights accommodation (5 in hotels, 2 in luxury desert camp)
                - All meals
                - Desert safari with camel ride
                - Cultural evening with folk dance
                - Fort visits with guide
                - Jeep safari
                - Traditional Rajasthani dinner
                - Transport in AC vehicle
                - Expert guide services
                '''
            },
            {
                'name': 'Himalayan Retreat',
                'category': 'Adventure',
                'duration': 7,
                'price': Decimal('32000.00'),
                'description': '''Experience the majestic Himalayas in all their glory. Trek through beautiful valleys, visit ancient monasteries, and enjoy stunning mountain views. Perfect for adventure enthusiasts and nature lovers.''',
                'inclusions': '''
                - 6 nights accommodation in hotels and mountain lodges
                - All meals during the trek
                - Professional trekking guide
                - Porter services
                - Camping equipment
                - First aid kit
                - Permits and fees
                - Transport from Manali
                - Photography sessions
                '''
            },
            {
                'name': 'Goa Beach Holiday',
                'category': 'Leisure',
                'duration': 4,
                'price': Decimal('22000.00'),
                'description': '''Relax on the beautiful beaches of Goa. Enjoy water sports, explore Portuguese heritage, experience vibrant nightlife, and savor delicious seafood. Perfect for a short beach getaway.''',
                'inclusions': '''
                - 3 nights in beach resort
                - Daily breakfast
                - Water sports activities
                - Heritage site tours
                - Evening cruise
                - Beach activities
                - Airport transfers
                - Local assistance
                '''
            },
            {
                'name': 'Wildlife Safari Experience',
                'category': 'Wildlife',
                'duration': 6,
                'price': Decimal('38000.00'),
                'description': '''Explore India's diverse wildlife in its natural habitat. Visit renowned national parks, spot tigers, elephants, and exotic birds. A must for wildlife enthusiasts and photographers.''',
                'inclusions': '''
                - 5 nights accommodation in jungle lodges
                - All meals
                - Morning and evening safaris
                - Naturalist guide
                - Photography workshop
                - Park entrance fees
                - Transport in safari vehicles
                - Bird watching sessions
                - All transfers
                '''
            },
            {
                'name': 'Buddhist Circuit Tour',
                'category': 'Spiritual',
                'duration': 7,
                'price': Decimal('40000.00'),
                'description': '''Follow the footsteps of Buddha on this spiritual journey. Visit sacred sites like Bodhgaya, Sarnath, and Kushinagar. Experience meditation sessions and learn about Buddhist philosophy.''',
                'inclusions': '''
                - 6 nights accommodation in heritage hotels
                - All meals (vegetarian)
                - Meditation sessions
                - Buddhist scholar guide
                - Monument entrance fees
                - Air-conditioned transport
                - Airport transfers
                - Prayer ceremony participation
                - All applicable taxes
                '''
            }
        ]

        for package_data in packages_data:
            package = Package.objects.create(
                name=package_data['name'],
                category=package_data['category'],
                duration=package_data['duration'],
                price=package_data['price'],
                description=package_data['description'],
                inclusions=package_data['inclusions']
            )
            self.stdout.write(f'Created package: {package.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample packages'))