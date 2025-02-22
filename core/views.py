from django.shortcuts import render, redirect
from products.models import Product, Category
from django.http import JsonResponse
from django.contrib import messages

def home_view(request):
    featured_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()[:6]
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about_view(request):
    return render(request, 'core/about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save to database
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('core:contact')
    
    return render(request, 'core/contact.html')

def terms_view(request):
    return render(request, 'core/terms.html')

def privacy_view(request):
    return render(request, 'core/privacy.html')

def sell_online_view(request):
    return render(request, 'core/sell_online.html')

def how_it_works_view(request):
    return render(request, 'core/how_it_works.html')

def pricing_view(request):
    return render(request, 'core/pricing.html')

def shipping_view(request):
    return render(request, 'core/shipping.html')

def events_view(request):
    return render(request, 'core/events.html')

def news_view(request):
    return render(request, 'core/news.html')

def faq_view(request):
    return render(request, 'core/faq.html')

def support_view(request):
    return render(request, 'core/support.html')

def newsletter_subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Add newsletter subscription logic here
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
