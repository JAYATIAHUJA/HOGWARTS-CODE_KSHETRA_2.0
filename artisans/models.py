from django.db import models
from django.conf import settings

class State(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}, {self.city.name}"

class Artisan(models.Model):
    CRAFT_CHOICES = [
        ('pottery', 'Pottery'),
        ('weaving', 'Weaving'),
        ('woodcarving', 'Wood Carving'),
        ('jewelry', 'Jewelry Making'),
        ('painting', 'Traditional Painting'),
        ('textile', 'Textile Art'),
        ('metalwork', 'Metal Work'),
        ('other', 'Other Crafts')
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Changed from User to settings.AUTH_USER_MODEL
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    craft_type = models.CharField(max_length=50, choices=CRAFT_CHOICES)
    description = models.TextField()
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    years_of_experience = models.IntegerField()
    profile_image = models.ImageField(upload_to='artisan_profiles/', blank=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.get_craft_type_display()}" 