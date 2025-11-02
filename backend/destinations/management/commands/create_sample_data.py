from django.core.management.base import BaseCommand
from destinations.models import Destination
from django.core.files import File
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates sample destination data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample destinations...')

        destinations_data = [
            {
                'name': 'Taj Mahal, Agra',
                'description': 'The Taj Mahal is an ivory-white marble mausoleum on the right bank of the river Yamuna in Agra, India. It was commissioned in 1632 by the Mughal emperor Shah Jahan to house the tomb of his favourite wife, Mumtaz Mahal.',
                'coords': {'lat': 27.1751, 'lng': 78.0421},
                'features': [
                    'UNESCO World Heritage Site',
                    'Architectural Marvel',
                    'Historical Monument',
                    'Guided Tours Available',
                    'Photography Allowed'
                ]
            },
            {
                'name': 'Jaipur City Palace',
                'description': 'The City Palace, Jaipur was established in 1727 by Maharaja Sawai Jai Singh II, who moved his court to Jaipur from Amber. Architecturally the Palace is a fusion of Rajput and Mughal styles.',
                'coords': {'lat': 26.9255, 'lng': 75.8236},
                'features': [
                    'Royal Architecture',
                    'Museum',
                    'Cultural Heritage',
                    'Light and Sound Show',
                    'Shopping Area'
                ]
            },
            {
                'name': 'Varanasi Ghats',
                'description': 'The Ghats in Varanasi are riverfront steps leading to the banks of the River Ganges. The city has 88 ghats. Most of the ghats are bathing and puja ceremony ghats, while two ghats are used exclusively as cremation sites.',
                'coords': {'lat': 25.3176, 'lng': 83.0064},
                'features': [
                    'Spiritual Experience',
                    'Boat Rides',
                    'Evening Aarti Ceremony',
                    'Cultural Performances',
                    'Historical Significance'
                ]
            },
            {
                'name': 'Kerala Backwaters',
                'description': 'The Kerala backwaters are a network of interconnected canals, rivers, lakes and inlets, a labyrinthine system formed by more than 900 km of waterways. Traditional houseboats offer luxurious rides through the serene waters.',
                'coords': {'lat': 9.4981, 'lng': 76.3388},
                'features': [
                    'Houseboat Stay',
                    'Natural Beauty',
                    'Local Cuisine',
                    'Village Life Experience',
                    'Birdwatching'
                ]
            },
            {
                'name': 'Hampi Ruins',
                'description': 'Hampi is an ancient village in Karnataka, India. It was one of the richest and largest cities in the world during its prime. The ruins of Hampi represent the last remnants of a lost empire.',
                'coords': {'lat': 15.3350, 'lng': 76.4600},
                'features': [
                    'UNESCO World Heritage Site',
                    'Ancient Ruins',
                    'Rock Climbing',
                    'Temple Architecture',
                    'Riverside Location'
                ]
            }
        ]

        for dest_data in destinations_data:
            destination = Destination.objects.create(
                name=dest_data['name'],
                description=dest_data['description'],
                coords=dest_data['coords'],
                features=dest_data['features']
            )
            self.stdout.write(f'Created destination: {destination.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample destinations'))