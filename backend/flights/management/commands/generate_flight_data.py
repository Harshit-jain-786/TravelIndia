from django.core.management.base import BaseCommand
from django.utils import timezone
from flights.models import Flight
from datetime import timedelta, datetime
import random

class Command(BaseCommand):
    help = 'Generates flight data for the next week'

    def handle(self, *args, **kwargs):
        # Delete existing future flights
        Flight.objects.filter(departure__gt=timezone.now()).delete()

        # List of cities with their corresponding airport codes
        cities = [
            ("Delhi", "DEL"),
            ("Mumbai", "BOM"),
            ("Bangalore", "BLR"),
            ("Chennai", "MAA"),
            ("Kolkata", "CCU"),
            ("Hyderabad", "HYD"),
            ("Goa", "GOI"),
            ("Jaipur", "JAI"),
            ("Amritsar", "ATQ"),
            ("Ludhiana", "LUH"),
            ("Chandigarh", "IXC"),
            ("Jalandhar", "JUC"),
            ("Patiala", "IXP")
        ]

        airlines = [
            "Air India",
            "IndiGo",
            "SpiceJet",
            "Vistara",
            "Go First",
            "Alliance Air"
        ]

        flight_classes = ["economy", "premium", "business", "first"]
        trip_types = ["round-trip", "one-way"]

        # Start date (today)
        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Generate flights for next 7 days
        for day in range(7):
            current_date = start_date + timedelta(days=day)
            
            # Generate multiple flights between city pairs
            for from_city, from_code in cities:
                for to_city, to_code in cities:
                    if from_city != to_city:  # Don't create flights to same city
                        # Generate 2-4 flights per route per day
                        num_flights = random.randint(2, 4)
                        
                        for _ in range(num_flights):
                            # Random departure time between 6 AM and 11 PM
                            departure_hour = random.randint(6, 23)
                            departure_minute = random.choice([0, 15, 30, 45])
                            departure_time = current_date.replace(hour=departure_hour, minute=departure_minute)
                            
                            # Flight duration between 1 to 4 hours
                            duration_minutes = random.randint(60, 240)
                            duration = timedelta(minutes=duration_minutes)
                            
                            # Generate price based on distance and class
                            base_price = random.randint(2000, 8000)
                            flight_class = random.choice(flight_classes)
                            if flight_class == "premium":
                                base_price *= 1.5
                            elif flight_class == "business":
                                base_price *= 2.5
                            elif flight_class == "first":
                                base_price *= 4
                            
                            # Create the flight
                            flight = Flight(
                                flight_number=f"{random.choice(airlines)[:2]}{random.randint(100, 999)}",
                                airline=random.choice(airlines),
                                from_city=from_city,
                                to_city=to_city,
                                from_airport_code=from_code,
                                to_airport_code=to_code,
                                departure=departure_time,
                                duration=duration,
                                price=round(base_price, -2),  # Round to nearest hundred
                                seats_available=random.randint(10, 180),
                                flight_class=flight_class,
                                trip_type=random.choice(trip_types)
                            )
                            flight.save()
                            
                            self.stdout.write(f"Created flight: {flight}")

        self.stdout.write(self.style.SUCCESS('Successfully generated flight data'))