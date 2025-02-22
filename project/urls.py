from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # assuming you have core.urls
    path('events/', include('events.urls')),  # remove the namespace parameter for now
    path('artisans/', include('artisans.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 