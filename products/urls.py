from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product URLs
    path('', views.product_list_view, name='product_list'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    
    # Category URLs
    path('categories/', views.category_list_view, name='category_list'),
    path('category/<str:category_slug>/', views.category_detail, name='category_detail'),
    
    # Product Management URLs (for sellers)
    path('manage/create/', views.product_create_view, name='product_create'),
    path('manage/<slug:slug>/edit/', views.product_edit_view, name='product_edit'),
    path('manage/<slug:slug>/delete/', views.product_delete_view, name='product_delete'),
    
    # Product Review URLs
    path('product/<slug:slug>/reviews/', views.product_reviews_view, name='product_reviews'),
    path('product/<slug:slug>/reviews/add/', views.add_review_view, name='add_review'),
    
    # Search and Filter URLs
    path('search/', views.product_search_view, name='product_search'),
    path('filter/', views.product_filter_view, name='product_filter'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # API endpoints for dynamic loading
    path('api/products/', views.api_product_list, name='api_product_list'),
    path('api/categories/', views.api_category_list, name='api_category_list'),
] 