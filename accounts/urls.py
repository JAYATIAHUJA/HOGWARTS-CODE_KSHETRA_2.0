from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/seller/', views.register_seller_view, name='register_seller'),
    
    # Profile URLs
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    
    # Seller URLs
    path('seller/dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
    path('seller/kyc/', views.seller_kyc_view, name='seller_kyc'),
    path('seller/products/', views.seller_products_view, name='seller_products'),
    path('seller/orders/', views.seller_orders_view, name='seller_orders'),
    path('seller/insights/', views.seller_insights_view, name='seller_insights'),
    
    # Customer URLs
    path('customer/dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    path('customer/orders/', views.customer_orders_view, name='customer_orders'),
    path('customer/wishlist/', views.customer_wishlist_view, name='customer_wishlist'),
] 