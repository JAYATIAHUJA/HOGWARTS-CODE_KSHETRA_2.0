from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from events.models import Event, EventTicketType
from datetime import timedelta
import random

User = get_user_model()

SAMPLE_EVENTS = [
    {
        'title': 'TechFest 2025 - IIT Delhi',
        'description': 'Annual technical festival featuring robotics competitions, hackathons, and tech exhibitions.',
        'location': 'Indian Institute of Technology Delhi, Hauz Khas, New Delhi, Delhi 110016',
        'location_map_link': 'https://maps.app.goo.gl/XXXXX',
        'agenda': '''
09:00 AM - Registration
10:00 AM - Opening Ceremony
11:00 AM - Hackathon Begins
02:00 PM - Robotics Competition
05:00 PM - Tech Talks
07:00 PM - Prize Distribution''',
        'speakers': 'Dr. Ramesh Kumar (AI Expert), Prof. Sarah Johnson (Robotics), Mr. Amit Sharma (Industry Leader)',
        'ticket_types': [
            {'name': 'Student Entry', 'price': 299, 'quantity': 500, 'description': 'Valid student ID required'},
            {'name': 'Professional', 'price': 999, 'quantity': 200, 'description': 'Full access to all events'},
            {'name': 'VIP Pass', 'price': 2499, 'quantity': 50, 'description': 'Includes lunch and workshop access'}
        ]
    },
    {
        'title': 'Cultural Fusion - Delhi University',
        'description': 'Inter-college cultural festival with music, dance, and theatrical performances.',
        'location': 'Delhi University North Campus, University Enclave, Delhi 110007',
        'location_map_link': 'https://maps.app.goo.gl/YYYYY',
        'agenda': '''
11:00 AM - Inauguration
12:00 PM - Dance Competition
02:30 PM - Music Performance
04:00 PM - Theatre Play
06:00 PM - Fashion Show
08:00 PM - Celebrity Performance''',
        'ticket_types': [
            {'name': 'General Entry', 'price': 199, 'quantity': 1000, 'description': 'Basic entry pass'},
            {'name': 'Premium Pass', 'price': 499, 'quantity': 300, 'description': 'Priority seating'}
        ]
    },
    {
        'title': 'Business Conclave - SRCC',
        'description': 'Annual business summit featuring industry leaders and entrepreneurship workshops.',
        'location': 'Shri Ram College of Commerce, Maurice Nagar, Delhi 110007',
        'location_map_link': 'https://maps.app.goo.gl/ZZZZZ',
        'agenda': '''
09:30 AM - Registration
10:00 AM - Keynote Speech
11:30 AM - Panel Discussion
02:00 PM - Startup Pitching
04:00 PM - Networking Session''',
        'ticket_types': [
            {'name': 'Student Delegate', 'price': 399, 'quantity': 300, 'description': 'For college students'},
            {'name': 'Corporate Delegate', 'price': 1499, 'quantity': 100, 'description': 'For professionals'}
        ]
    },
    {
        'title': 'Sports Meet 2025 - JNU',
        'description': 'Inter-university sports competition featuring multiple sporting events.',
        'location': 'Jawaharlal Nehru University, New Mehrauli Road, Delhi 110067',
        'location_map_link': 'https://maps.app.goo.gl/WWWWW',
        'agenda': '''
08:00 AM - Opening Ceremony
09:00 AM - Track Events
02:00 PM - Team Sports
05:00 PM - Prize Distribution''',
        'ticket_types': [
            {'name': 'Participant Entry', 'price': 149, 'quantity': 400, 'description': 'For registered athletes'},
            {'name': 'Spectator Pass', 'price': 99, 'quantity': 1000, 'description': 'General entry'}
        ]
    }
]

class Command(BaseCommand):
    help = 'Creates sample events in Delhi colleges'

    def handle(self, *args, **kwargs):
        try:
            # Get or create a default organizer
            organizer, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                organizer.set_password('admin123')
                organizer.save()

            # Create events
            for event_data in SAMPLE_EVENTS:
                # Random date within next 3 months
                random_days = random.randint(7, 90)
                event_date = timezone.now() + timedelta(days=random_days)
                
                event = Event.objects.create(
                    title=event_data['title'],
                    description=event_data['description'],
                    date=event_date,
                    location=event_data['location'],
                    location_map_link=event_data.get('location_map_link', ''),
                    organizer=organizer,
                    agenda=event_data.get('agenda', ''),
                    speakers=event_data.get('speakers', '')
                )

                # Create ticket types for the event
                for ticket_data in event_data['ticket_types']:
                    EventTicketType.objects.create(
                        event=event,
                        name=ticket_data['name'],
                        price=ticket_data['price'],
                        quantity_available=ticket_data['quantity'],
                        description=ticket_data['description']
                    )

            self.stdout.write(self.style.SUCCESS('Successfully created sample events'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating events: {str(e)}')) 