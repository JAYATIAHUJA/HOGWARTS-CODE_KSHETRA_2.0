from django.core.management.base import BaseCommand
from artisans.models import State, City, Area

class Command(BaseCommand):
    help = 'Load initial data for states and cities'

    def handle(self, *args, **kwargs):
        # Clear existing data
        State.objects.all().delete()
        
        # Create states and cities
        states_data = {
            'Maharashtra': ['Mumbai', 'Pune', 'Nagpur'],
            'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara'],
            'Rajasthan': ['Jaipur', 'Udaipur', 'Jodhpur'],
            'Uttar Pradesh': ['Lucknow', 'Varanasi', 'Agra'],
            'West Bengal': ['Kolkata', 'Howrah', 'Darjeeling'],
            'Tamil Nadu': ['Chennai', 'Madurai', 'Coimbatore'],
            'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode'],
            'Karnataka': ['Bangalore', 'Mysore', 'Hampi'],
            'Madhya Pradesh': ['Bhopal', 'Indore', 'Gwalior'],
            'Delhi': ['New Delhi', 'Old Delhi', 'Dwarka']
        }

        for state_name, cities in states_data.items():
            state = State.objects.create(name=state_name)
            self.stdout.write(f'Created state: {state_name}')
            
            for city_name in cities:
                city = City.objects.create(name=city_name, state=state)
                self.stdout.write(f'Created city: {city_name} in {state_name}')
                
                # Create areas for each city
                areas = ['North', 'South', 'East', 'West', 'Central']
                for area_name in areas:
                    area = Area.objects.create(
                        name=f'{area_name} {city_name}',
                        city=city
                    )
                    self.stdout.write(f'Created area: {area.name}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data')) 