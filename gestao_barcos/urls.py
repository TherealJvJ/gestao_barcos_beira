"""URLs do projecto gestao_barcos."""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', lambda request: redirect('login'), name='home'),
    path('api/', include('core.api_urls')),
    path('', include('core.urls')),
]
