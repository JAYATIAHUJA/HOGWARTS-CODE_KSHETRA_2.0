from django.urls import path
from . import views

app_name = 'artisans'

urlpatterns = [
    path('nearby/', views.nearby_artisans, name='nearby'),
] 