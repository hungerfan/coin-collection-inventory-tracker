"""
URL routing for coin collection tracker API.

Maps URL patterns to views/viewsets.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CoinViewSet,
    CoinTypeViewSet,
    ConditionViewSet,
    CountryViewSet,
    stats_view,
    api_root
)

# Create a router for automatic URL generation
router = DefaultRouter()

# Register viewsets with the router
# This automatically creates URLs for CRUD operations
router.register(r'coins', CoinViewSet, basename='coin')
router.register(r'coin-types', CoinTypeViewSet, basename='cointype')
router.register(r'conditions', ConditionViewSet, basename='condition')
router.register(r'countries', CountryViewSet, basename='country')

# URL patterns
urlpatterns = [
    # API root
    path('', api_root, name='api-root'),

    # Statistics endpoint
    path('stats/', stats_view, name='stats'),

    # Include router URLs (all CRUD endpoints)
    path('', include(router.urls)),
]

