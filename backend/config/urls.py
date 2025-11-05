"""
URL configuration for coin collection tracker backend.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # All API endpoints will be under /api/
]

