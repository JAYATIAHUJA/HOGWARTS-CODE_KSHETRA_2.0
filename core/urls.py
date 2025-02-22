from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home and Static Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    
    # Seller Information Pages
    path('sell-online/', views.sell_online_view, name='sell_online'),
    path('how-it-works/', views.how_it_works_view, name='how_it_works'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('shipping/', views.shipping_view, name='shipping'),
    
    # Events and News
    path('events/', views.events_view, name='events'),
    path('news/', views.news_view, name='news'),
    
    # Customer Support
    path('faq/', views.faq_view, name='faq'),
    path('support/', views.support_view, name='support'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe_view, name='newsletter_subscribe'),
] 