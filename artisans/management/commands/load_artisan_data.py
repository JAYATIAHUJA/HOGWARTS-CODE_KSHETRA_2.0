from django.core.management.base import BaseCommand
from artisans.models import State, City, Area, Artisan
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Loads sample data for artisans app'

    def handle(self, *args, **kwargs):
        # Sample States
        states_data = [
            "Rajasthan",
            "Gujarat",
            "Uttar Pradesh",
            "Maharashtra",
            "West Bengal"
        ]

        # Create States
        states = []
        for state_name in states_data:
            state, created = State.objects.get_or_create(name=state_name)
            states.append(state)
            self.stdout.write(f'Created state: {state_name}')

        # Sample Cities for each state
        cities_data = {
            "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur"],
            "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
            "Uttar Pradesh": ["Lucknow", "Varanasi", "Agra"],
            "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
            "West Bengal": ["Kolkata", "Howrah", "Siliguri"]
        }

        # Create Cities
        cities = []
        for state in states:
            for city_name in cities_data[state.name]:
                city, created = City.objects.get_or_create(
                    name=city_name,
                    state=state
                )
                cities.append(city)
                self.stdout.write(f'Created city: {city_name} in {state.name}')

        # Sample Areas for each city
        areas_data = ["Central", "North", "South", "East", "West"]
        
        # Create Areas
        areas = []
        for city in cities:
            for area_name in areas_data:
                area, created = Area.objects.get_or_create(
                    name=f"{area_name} {city.name}",
                    city=city
                )
                areas.append(area)
                self.stdout.write(f'Created area: {area_name} in {city.name}')

        # Sample Artisan Data
        craft_types = ['pottery', 'weaving', 'woodcarving', 'jewelry', 'painting', 'textile', 'metalwork']
        artisan_first_names = ["Raj", "Priya", "Amit", "Sunita", "Mohan", "Lakshmi", "Krishna", "Radha"]
        artisan_last_names = ["Kumar", "Singh", "Sharma", "Patel", "Das", "Gupta", "Verma", "Rao"]

        # Create Artisans
        for i in range(30):  # Create 30 sample artisans
            username = f"artisan{i+1}"
            email = f"artisan{i+1}@example.com"
            
            # Create User
            user, created = User.objects.get_or_create(
                username=username,
                email=email
            )
            if created:
                user.set_password('password123')
                user.save()

            # Create Artisan
            name = f"{random.choice(artisan_first_names)} {random.choice(artisan_last_names)}"
            craft = random.choice(craft_types)
            area = random.choice(areas)
            experience = random.randint(5, 30)

            artisan, created = Artisan.objects.get_or_create(
                user=user,
                defaults={
                    'name': name,
                    'craft_type': craft,
                    'description': f"Expert {craft} artisan with {experience} years of experience in traditional {craft} techniques.",
                    'area': area,
                    'address': f"{random.randint(1, 100)}, {area.name}, {area.city.name}",
                    'phone': f"+91 {random.randint(7000000000, 9999999999)}",
                    'email': email,
                    'years_of_experience': experience,
                    'is_verified': True
                }
            )
            if created:
                self.stdout.write(f'Created artisan: {name} - {craft}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data')) 