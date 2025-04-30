from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Review, Cart, CartItem, Wishlist
from .forms import ProductForm, ReviewForm
from django.http import JsonResponse
import logging
from django.http import Http404
from django.urls import reverse

logger = logging.getLogger(__name__)

def product_list_view(request):
    products = Product.objects.filter(is_active=True)
    query = request.GET.get('q')
    category = request.GET.get('category')
    sort = request.GET.get('sort')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    if category:
        products = products.filter(category__slug=category)

    if sort:
        if sort == 'price_low':
            products = products.order_by('price')
        elif sort == 'price_high':
            products = products.order_by('-price')
        elif sort == 'newest':
            products = products.order_by('-created_at')
        elif sort == 'popular':
            products = products.order_by('-views')

    # Get all categories from the database
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'current_sort': sort,
        'query': query
    }
    return render(request, 'products/product_list.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('products:product_detail', slug=slug)
    else:
        form = ReviewForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'form': form,
    }
    return render(request, 'products/product_detail.html', context)

def category_list_view(request):
    categories = Category.objects.all()
    
    # Make sure all categories have descriptions
    for category in categories:
        if not category.description:
            # Set a custom description based on category name
            category.description = f"Explore our beautiful collection of {category.name.lower()} crafted by talented artisans."
    
    return render(request, 'products/category_list.html', {'categories': categories})

def category_products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products,
    })

def product_create_view(request):
    if request.user.user_type != 'SELLER':
        messages.error(request, 'Only sellers can create products.')
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Create'})

def product_edit_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.user != product.seller:
        messages.error(request, 'You can only edit your own products.')
        return redirect('products:product_detail', slug=product.slug)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:product_detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {
        'form': form,
        'product': product,
        'action': 'Edit'
    })

def product_delete_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.user != product.seller:
        messages.error(request, 'You can only delete your own products.')
        return redirect('products:product_detail', slug=product.slug)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:product_list')
    
    return render(request, 'products/product_confirm_delete.html', {'product': product})

def product_search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__name__icontains=query),
        is_active=True
    )
    return render(request, 'products/product_search.html', {
        'products': products,
        'query': query
    })

def product_filter_view(request):
    products = Product.objects.filter(is_active=True)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    return render(request, 'products/product_filter.html', {'products': products})

def add_review_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
        else:
            messages.error(request, 'Error adding review. Please try again.')
    
    return redirect('products:product_detail', slug=product.slug)

def product_reviews_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by('-created_at')
    return render(request, 'products/product_reviews.html', {
        'product': product,
        'reviews': reviews
    })

# API views for dynamic loading
def api_product_list(request):
    products = Product.objects.filter(is_active=True)
    data = [{
        'id': p.id,
        'name': p.name,
        'price': str(p.price),
        'image': p.images.first().image.url if p.images.exists() else None,
    } for p in products]
    return JsonResponse({'products': data})

def api_category_list(request):
    categories = Category.objects.all()
    data = [{
        'id': c.id,
        'name': c.name,
        'image': c.image.url if c.image else None,
    } for c in categories]
    return JsonResponse({'categories': data})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    recommended_products = Product.objects.filter(is_active=True).exclude(
        id__in=[item.product.id for item in cart.items.all()]
    )[:4]
    
    return render(request, 'products/cart.html', {
        'cart': cart,
        'recommended_products': recommended_products
    })

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        if product.stock < 1:
            return JsonResponse({
                'status': 'error',
                'message': 'Sorry, this product is out of stock.'
            })

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1
            if cart_item.quantity > product.stock:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Sorry, not enough stock available.'
                })
            cart_item.save()

        return JsonResponse({
            'status': 'success',
            'cart_total': cart.total_items,
            'message': 'Item added to cart successfully!'
        })

    return JsonResponse({
        'status': 'login_required',
        'redirect_url': reverse('accounts:login') + f'?next={request.path}'
    })

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        try:
            quantity = int(request.POST.get('quantity', 0))
            if quantity < 0:
                raise ValueError
            
            if quantity > cart_item.product.stock:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Sorry, not enough stock available.',
                    'current_quantity': cart_item.quantity
                })
            
            if quantity == 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()

            cart = cart_item.cart
            return JsonResponse({
                'status': 'success',
                'cart_total': cart.total_items,
                'subtotal': str(cart.subtotal),
                'total': str(cart.total),
                'item_subtotal': str(cart_item.subtotal),
                'item_id': cart_item.id
            })

        except (ValueError, TypeError):
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid quantity provided',
                'current_quantity': cart_item.quantity
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'status': 'success',
            'cart_total': cart.total_items,
            'subtotal': str(cart.subtotal),
            'total': str(cart.total)
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'products': products
    }
    
    return render(request, 'products/category_detail.html', context)

@login_required
def checkout_view(request):
    # Get the user's cart
    cart = Cart.objects.get_or_create(user=request.user)[0]
    
    # Check if cart is empty
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('products:cart')
        
    context = {
        'cart': cart,
    }
    return render(request, 'products/checkout.html', context)

@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # Check if user has a wishlist, create if not
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        # Add product to wishlist if not already there
        if product not in wishlist.products.all():
            wishlist.products.add(product)
            return JsonResponse({
                'status': 'success',
                'message': 'Added to your wishlist!'
            })
        else:
            # Product already in wishlist
            return JsonResponse({
                'status': 'error',
                'message': 'This item is already in your wishlist!'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })
