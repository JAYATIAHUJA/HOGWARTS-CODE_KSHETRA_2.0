from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from .models import CustomUser, SellerKYC
from products.models import Product, Order, Category
from .forms import (
    CustomUserCreationForm,
    SellerRegistrationForm,
    UserProfileForm,
    SellerKYCForm,
)

def products_list(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            
            # Redirect based on user type
            if user.user_type == 'SELLER':
                return redirect('accounts:seller_dashboard')
            else:
                return redirect('accounts:customer_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('core:home')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'CUSTOMER'
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('accounts:customer_dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def register_seller_view(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'SELLER'
            user.save()
            login(request, user)
            messages.success(request, 'Seller account created successfully! Please complete your KYC.')
            return redirect('accounts:seller_kyc')
    else:
        form = SellerRegistrationForm()
    
    return render(request, 'accounts/register_seller.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def seller_dashboard_view(request):
    if request.user.user_type != 'SELLER':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('core:home')
    
    # Get seller statistics
    products = Product.objects.filter(seller=request.user)
    total_products = products.count()
    total_orders = Order.objects.filter(items__product__seller=request.user).distinct().count()
    total_revenue = Order.objects.filter(
        items__product__seller=request.user,
        status='DELIVERED'
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': Order.objects.filter(
            items__product__seller=request.user
        ).distinct().order_by('-created_at')[:5],
        'top_products': products.annotate(
            order_count=Count('orderitem')
        ).order_by('-order_count')[:5],
    }
    
    return render(request, 'accounts/seller/dashboard.html', context)

@login_required
def seller_kyc_view(request):
    if request.user.user_type != 'SELLER':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('core:home')
    
    try:
        kyc = SellerKYC.objects.get(user=request.user)
    except SellerKYC.DoesNotExist:
        kyc = None
    
    if request.method == 'POST':
        form = SellerKYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.user = request.user
            kyc.save()
            messages.success(request, 'KYC information submitted successfully!')
            return redirect('accounts:seller_dashboard')
    else:
        form = SellerKYCForm(instance=kyc)
    
    return render(request, 'accounts/seller/kyc.html', {'form': form, 'kyc': kyc})

@login_required
def seller_products_view(request):
    if request.user.user_type != 'SELLER':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('core:home')
    
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'accounts/seller/products.html', {'products': products})

@login_required
def seller_orders_view(request):
    if request.user.user_type != 'SELLER':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('core:home')
    
    orders = Order.objects.filter(
        items__product__seller=request.user
    ).distinct().order_by('-created_at')
    
    return render(request, 'accounts/seller/orders.html', {'orders': orders})

@login_required
def seller_insights_view(request):
    if request.user.user_type != 'SELLER':
        messages.error(request, 'Access denied. Seller account required.')
        return redirect('core:home')
    
    # Get insights data
    products = Product.objects.filter(seller=request.user)
    
    context = {
        'total_revenue': Order.objects.filter(
            items__product__seller=request.user,
            status='DELIVERED'
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
        'product_performance': products.annotate(
            order_count=Count('orderitem'),
            revenue=Sum('orderitem__price')
        ).order_by('-revenue'),
        'monthly_sales': Order.objects.filter(
            items__product__seller=request.user,
            status='DELIVERED'
        ).values('created_at__month').annotate(
            total=Sum('total_amount')
        ).order_by('created_at__month'),
    }
    
    return render(request, 'accounts/seller/insights.html', context)

@login_required
def customer_dashboard_view(request):
    if request.user.user_type != 'CUSTOMER':
        messages.error(request, 'Access denied. Customer account required.')
        return redirect('core:home')
    
    context = {
        'recent_orders': Order.objects.filter(customer=request.user).order_by('-created_at')[:5],
        'wishlist_items': request.user.wishlist.all()[:5] if hasattr(request.user, 'wishlist') else [],
    }
    
    return render(request, 'accounts/customer/dashboard.html', context)

@login_required
def customer_orders_view(request):
    if request.user.user_type != 'CUSTOMER':
        messages.error(request, 'Access denied. Customer account required.')
        return redirect('core:home')
    
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'accounts/customer/orders.html', {'orders': orders})

@login_required
def customer_wishlist_view(request):
    if request.user.user_type != 'CUSTOMER':
        messages.error(request, 'Access denied. Customer account required.')
        return redirect('core:home')
    
    wishlist_items = request.user.wishlist.all() if hasattr(request.user, 'wishlist') else []
    return render(request, 'accounts/customer/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Check if current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('accounts:profile')
        
        # Check if new passwords match
        if new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('accounts:profile')
        
        # Check password strength (you can add more validation rules)
        if len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('accounts:profile')
        
        # Change password
        request.user.set_password(new_password1)
        request.user.save()
        
        # Update session to prevent logout
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Your password was successfully updated!')
        return redirect('accounts:profile')
    
    return redirect('accounts:profile')
