from django.core.management.base import BaseCommand
from django.utils import timezone
from flights.models import Flight
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Creates sample flight data'

    def handle(self, *args, **kwargs):
        # Delete flights older than 24 hours to keep DB tidy
        cutoff = timezone.now() - timedelta(hours=24)
        Flight.objects.filter(departure__lt=cutoff).delete()

        # Popular Indian cities and their airports with proper names
        AIRPORTS = [
            ('DEL', 'New Delhi', 'Indira Gandhi International Airport'),
            ('BOM', 'Mumbai', 'Chhatrapati Shivaji International Airport'),
            ('BLR', 'Bengaluru', 'Kempegowda International Airport'),
            ('HYD', 'Hyderabad', 'Rajiv Gandhi International Airport'),
            ('CCU', 'Kolkata', 'Netaji Subhas Chandra Bose International Airport'),
            ('MAA', 'Chennai', 'Chennai International Airport'),
            ('GOI', 'Goa', 'Dabolim Airport'),
            ('JAI', 'Jaipur', 'Jaipur International Airport')
        ]

        # Airlines
        AIRLINES = [
            ('Air India', 'AI'),
            ('IndiGo', '6E'),
            ('SpiceJet', 'SG'),
            ('Vistara', 'UK'),
            ('Go First', 'G8')
        ]

        # Flight classes
        CLASSES = [
            ('Economy', 1.0),
            ('Premium Economy', 1.5),
            ('Business', 2.5),
            ('First', 4.0)
        ]

        # Base prices for different flight durations
        base_prices = {
            'short': (3000, 5000),    # < 2 hours
            'medium': (5000, 8000),   # 2-4 hours
            'long': (8000, 12000)     # > 4 hours
        }

        # Current time
        current_time = timezone.now()
        end_time = current_time + timedelta(days=1)

        # Create flights for the next 24 hours
        while current_time < end_time:
            # Create multiple flights for each time slot
            for _ in range(3):  # 3 flights per time slot
                # Random origin and destination
                origin = random.choice(AIRPORTS)
                destination = random.choice([ap for ap in AIRPORTS if ap != origin])
                
                # Random airline
                airline, code = random.choice(AIRLINES)
                
                # Get full airport names
                from_airport_name = origin[2]
                to_airport_name = destination[2]
                
                # Flight duration (1.5 to 4 hours)
                flight_duration = random.randint(90, 240)
                
                # Base price based on duration
                if flight_duration < 120:
                    base_price_range = base_prices['short']
                elif flight_duration < 180:
                    base_price_range = base_prices['medium']
                else:
                    base_price_range = base_prices['long']
                
                base_price = random.randint(base_price_range[0], base_price_range[1])

                # Create flights for different classes
                for flight_class, price_multiplier in CLASSES:
                    # Generate flight number
                    flight_number = f'{code}{random.randint(1000, 9999)}'
                    
                    # Calculate final price
                    price = int(base_price * price_multiplier)
                    
                    # Skip if duplicate exists
                    if Flight.objects.filter(
                        departure=current_time,
                        from_city=origin[1],
                        to_city=destination[1],
                        flight_class=flight_class
                    ).exists():
                        continue

                    # Create the flight
                    Flight.objects.create(
                        airline=airline,
                        flight_number=flight_number,
                        from_city=origin[1],
                        to_city=destination[1],
                        from_airport_code=origin[0],
                        to_airport_code=destination[0],
                        departure=current_time,
                        duration=timedelta(minutes=flight_duration),
                        price=price,
                        seats_available=random.randint(5, 50),
                        flight_class=flight_class,
                        trip_type='one_way'
                    )

            # Next batch of flights after 2 hours
            current_time += timedelta(hours=2)

        self.stdout.write(self.style.SUCCESS('Successfully created sample flight data'))