from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Review, Cart, CartItem
from .forms import ProductForm, ReviewForm
from django.http import JsonResponse

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
    return render(request, 'products/category_list.html', {'categories': categories})

def category_products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products,
    })

@login_required
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

@login_required
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

@login_required
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

@login_required
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

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

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
    categories_data = {
        'textile': {
            'name': 'Textile-Based Handicrafts',
            'description': 'Traditional textiles, embroidery, weaving, block printing, and fabric art',
            'products': [
                {
                    'id': 1,
                    'name': 'Traditional Embroidered Shawl',
                    'price': 2499.99,
                    'description': 'Handcrafted embroidered shawl with traditional patterns',
                    'is_available': True,
                    'slug': 'traditional-embroidered-shawl',
                },
                {
                    'id': 2,
                    'name': 'Block Print Cotton Bedsheet',
                    'price': 1899.99,
                    'description': 'Hand block printed cotton bedsheet with ethnic designs',
                    'is_available': True,
                    'slug': 'block-print-bedsheet',
                },
                # Add 4 more products...
            ]
        },
        'stone': {
            'name': 'Stone Handicrafts',
            'description': 'Exquisite stone carvings and sculptures',
            'products': [
                {
                    'id': 1,
                    'name': 'Marble Elephant Statue',
                    'price': 4999.99,
                    'description': 'Hand-carved marble elephant with intricate details',
                    'is_available': True,
                    'slug': 'marble-elephant',
                },
                {
                    'id': 2,
                    'name': 'Sandstone Wall Panel',
                    'price': 3499.99,
                    'description': 'Traditional sandstone wall panel with geometric patterns',
                    'is_available': True,
                    'slug': 'sandstone-panel',
                },
                # Add 4 more products...
            ]
        },
        'jewelry': {
            'name': 'Jewelry Handicrafts',
            'description': 'Traditional handcrafted jewelry and accessories',
            'products': [
                {
                    'id': 1,
                    'name': 'Silver Filigree Necklace',
                    'price': 3999.99,
                    'description': 'Handcrafted silver filigree necklace with traditional design',
                    'is_available': True,
                    'slug': 'silver-filigree-necklace',
                },
                {
                    'id': 2,
                    'name': 'Tribal Brass Earrings',
                    'price': 999.99,
                    'description': 'Traditional tribal brass earrings with ethnic patterns',
                    'is_available': True,
                    'slug': 'tribal-brass-earrings',
                },
                # Add 4 more products...
            ]
        },
        'metal': {
            'name': 'Metal Handicrafts',
            'description': 'Traditional metalwork and decorative items',
            'products': [
                {
                    'id': 1,
                    'name': 'Brass Buddha Statue',
                    'price': 5999.99,
                    'description': 'Hand-crafted brass Buddha statue with antique finish',
                    'is_available': True,
                    'slug': 'brass-buddha',
                },
                {
                    'id': 2,
                    'name': 'Copper Wall Hanging',
                    'price': 2499.99,
                    'description': 'Traditional copper wall hanging with peacock design',
                    'is_available': True,
                    'slug': 'copper-wall-hanging',
                },
                # Add 4 more products...
            ]
        },
        'ceramic': {
            'name': 'Clay & Ceramic Handicrafts',
            'description': 'Traditional pottery, terracotta, and ceramic art pieces',
            'products': [
                {
                    'id': 1,
                    'name': 'Blue Pottery Vase',
                    'price': 1999.99,
                    'description': 'Traditional blue pottery vase with hand-painted floral designs',
                    'is_available': True,
                    'slug': 'blue-pottery-vase',
                },
                {
                    'id': 2,
                    'name': 'Terracotta Wall Plates',
                    'price': 1499.99,
                    'description': 'Set of decorative terracotta wall plates with traditional motifs',
                    'is_available': True,
                    'slug': 'terracotta-wall-plates',
                },
                {
                    'id': 3,
                    'name': 'Ceramic Tea Set',
                    'price': 2499.99,
                    'description': 'Handcrafted ceramic tea set with intricate patterns',
                    'is_available': True,
                    'slug': 'ceramic-tea-set',
                },
                {
                    'id': 4,
                    'name': 'Clay Wind Chimes',
                    'price': 899.99,
                    'description': 'Traditional clay wind chimes with bell designs',
                    'is_available': True,
                    'slug': 'clay-wind-chimes',
                },
                {
                    'id': 5,
                    'name': 'Ceramic Incense Holder',
                    'price': 599.99,
                    'description': 'Handmade ceramic incense holder with glazed finish',
                    'is_available': True,
                    'slug': 'ceramic-incense-holder',
                },
                {
                    'id': 6,
                    'name': 'Pottery Garden Planters',
                    'price': 1299.99,
                    'description': 'Set of hand-thrown pottery planters for garden decor',
                    'is_available': True,
                    'slug': 'pottery-garden-planters',
                },
            ]
        },
        'wood': {
            'name': 'Wood & Bamboo Handicrafts',
            'description': 'Exquisite wooden carvings, bamboo crafts, and furniture pieces',
            'products': [
                {
                    'id': 1,
                    'name': 'Carved Wooden Box',
                    'price': 2999.99,
                    'description': 'Hand-carved wooden jewelry box with traditional designs',
                    'is_available': True,
                    'slug': 'carved-wooden-box',
                },
                {
                    'id': 2,
                    'name': 'Bamboo Table Lamp',
                    'price': 1799.99,
                    'description': 'Eco-friendly bamboo table lamp with woven shade',
                    'is_available': True,
                    'slug': 'bamboo-table-lamp',
                },
                {
                    'id': 3,
                    'name': 'Wooden Wall Mask',
                    'price': 3499.99,
                    'description': 'Traditional wooden tribal mask for wall decoration',
                    'is_available': True,
                    'slug': 'wooden-wall-mask',
                },
                {
                    'id': 4,
                    'name': 'Bamboo Storage Baskets',
                    'price': 999.99,
                    'description': 'Set of handwoven bamboo storage baskets',
                    'is_available': True,
                    'slug': 'bamboo-storage-baskets',
                },
                {
                    'id': 5,
                    'name': 'Wooden Photo Frame',
                    'price': 1299.99,
                    'description': 'Hand-carved wooden photo frame with floral patterns',
                    'is_available': True,
                    'slug': 'wooden-photo-frame',
                },
                {
                    'id': 6,
                    'name': 'Bamboo Wind Chimes',
                    'price': 799.99,
                    'description': 'Natural bamboo wind chimes with wooden beads',
                    'is_available': True,
                    'slug': 'bamboo-wind-chimes',
                },
            ]
        },
        # Add more categories...
    }

    # Get category data
    category_data = categories_data.get(category_slug)
    
    if not category_data:
        # Handle 404 with a proper template
        return render(request, '404.html', status=404)

    context = {
        'category': {
            'name': category_data['name'],
            'description': category_data['description'],
        },
        'products': category_data['products']
    }
    
    return render(request, 'products/category_detail.html', context)
