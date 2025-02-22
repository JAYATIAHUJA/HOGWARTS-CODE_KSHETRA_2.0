from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Event(models.Model):
    # Basic Info
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    location_map_link = models.URLField(blank=True)
    
    # Media
    main_image = models.ImageField(upload_to='event_images/', blank=True)
    additional_images = models.ManyToManyField('EventImage', blank=True)
    
    # Organizer Info
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organizer_website = models.URLField(blank=True)
    organizer_phone = models.CharField(max_length=20, blank=True)
    
    # Event Details
    agenda = models.TextField(blank=True)
    speakers = models.TextField(blank=True)
    
    # Additional Info
    faq = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class EventTicketType(models.Model):
    event = models.ForeignKey(Event, related_name='available_tickets', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., VIP, Early Bird
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event.title} - {self.name}"

class EventImage(models.Model):
    image = models.ImageField(upload_to='event_images/')
    caption = models.CharField(max_length=200, blank=True)

class EventBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(EventTicketType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.ticket_type.event.title}"

class EventReview(models.Model):
    event = models.ForeignKey(Event, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username}'s review of {self.event.title}" 