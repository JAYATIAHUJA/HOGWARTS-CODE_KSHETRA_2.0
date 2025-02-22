from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('SELLER', 'Seller'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='CUSTOMER')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Additional fields for sellers
    business_name = models.CharField(max_length=100, blank=True)
    gstin = models.CharField(max_length=15, blank=True)  # GST Identification Number
    business_description = models.TextField(blank=True)
    is_verified_seller = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class SellerKYC(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    id_proof = models.ImageField(upload_to='kyc/id_proofs/')
    address_proof = models.ImageField(upload_to='kyc/address_proofs/')
    business_proof = models.ImageField(upload_to='kyc/business_proofs/')
    bank_details = models.JSONField()
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('VERIFIED', 'Verified'),
            ('REJECTED', 'Rejected'),
        ],
        default='PENDING'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"KYC for {self.user.username}"
