from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import State, City, Area, Artisan

def nearby_artisans(request):
    states = State.objects.all().order_by('name')
    cities = City.objects.all().order_by('name')
    areas = Area.objects.all().order_by('name')
    craft_choices = dict(Artisan.CRAFT_CHOICES)
    
    # Get filter parameters
    selected_state = request.GET.get('state')
    selected_city = request.GET.get('city')
    selected_area = request.GET.get('area')
    selected_craft = request.GET.get('craft')
    search_query = request.GET.get('search', '')

    # Filter artisans
    artisans = Artisan.objects.filter(is_verified=True)
    
    if search_query:
        artisans = artisans.filter(name__icontains=search_query)
    
    if selected_state:
        artisans = artisans.filter(area__city__state_id=selected_state)
    if selected_city:
        artisans = artisans.filter(area__city_id=selected_city)
    if selected_area:
        artisans = artisans.filter(area_id=selected_area)
    if selected_craft:
        artisans = artisans.filter(craft_type=selected_craft)

    context = {
        'states': states,
        'cities': cities,
        'areas': areas,
        'craft_choices': craft_choices,
        'artisans': artisans,
        'selected_state': selected_state,
        'selected_city': selected_city,
        'selected_area': selected_area,
        'selected_craft': selected_craft,
        'search_query': search_query,
    }
    return render(request, 'artisans/nearby.html', context)

def get_cities(request):
    state_id = request.GET.get('state_id')
    if state_id:
        cities = City.objects.filter(state_id=state_id).values('id', 'name').order_by('name')
    else:
        cities = City.objects.all().values('id', 'name').order_by('name')
    return JsonResponse(list(cities), safe=False)

def get_areas(request):
    city_id = request.GET.get('city_id')
    if city_id:
        areas = Area.objects.filter(city_id=city_id).values('id', 'name').order_by('name')
    else:
        areas = Area.objects.all().values('id', 'name').order_by('name')
    return JsonResponse(list(areas), safe=False) 