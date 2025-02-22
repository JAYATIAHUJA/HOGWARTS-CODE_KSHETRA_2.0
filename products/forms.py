from django import forms
from .models import Product, ProductImage, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'description', 'price', 'compare_price',
            'stock', 'main_image', 'material', 'dimensions', 'weight',
            'customization_available', 'shipping_info'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'shipping_info': forms.Textarea(attrs={'rows': 3}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        } 