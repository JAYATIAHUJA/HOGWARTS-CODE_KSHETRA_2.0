from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SellerKYC

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'password1', 'password2')

class SellerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    business_name = forms.CharField(max_length=100, required=True)
    business_description = forms.CharField(widget=forms.Textarea, required=True)
    gstin = forms.CharField(max_length=15, required=True, label='GSTIN')
    
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'phone_number', 'address',
            'business_name', 'business_description', 'gstin',
            'password1', 'password2'
        )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'email', 'phone_number',
            'address', 'profile_picture'
        )
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class SellerKYCForm(forms.ModelForm):
    bank_details = forms.JSONField(widget=forms.HiddenInput())
    
    class Meta:
        model = SellerKYC
        fields = ('id_proof', 'address_proof', 'business_proof', 'bank_details')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom bank details fields
        self.fields['bank_account_number'] = forms.CharField(max_length=20)
        self.fields['bank_ifsc'] = forms.CharField(max_length=11)
        self.fields['bank_account_name'] = forms.CharField(max_length=100)
        self.fields['bank_name'] = forms.CharField(max_length=100)
        
        # If instance exists, populate bank details fields
        if self.instance and self.instance.bank_details:
            for field in ['bank_account_number', 'bank_ifsc', 'bank_account_name', 'bank_name']:
                self.fields[field].initial = self.instance.bank_details.get(field, '')
    
    def clean(self):
        cleaned_data = super().clean()
        # Combine bank details fields into JSON
        bank_details = {
            'bank_account_number': cleaned_data.get('bank_account_number'),
            'bank_ifsc': cleaned_data.get('bank_ifsc'),
            'bank_account_name': cleaned_data.get('bank_account_name'),
            'bank_name': cleaned_data.get('bank_name'),
        }
        cleaned_data['bank_details'] = bank_details
        return cleaned_data 