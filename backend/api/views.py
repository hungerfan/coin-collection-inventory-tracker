"""
API Views for coin collection tracker.

ViewSets provide CRUD operations for models automatically.
Additional views provide custom endpoints like statistics.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Sum, Count
from decimal import Decimal

from .models import Coin, CoinType, Condition, Country
from .serializers import (
    CoinSerializer,
    CoinDetailSerializer,
    CoinTypeSerializer,
    ConditionSerializer,
    CountrySerializer,
    StatsSerializer
)


class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for countries.

    Provides:
    - GET    /api/countries/       - List all countries
    - POST   /api/countries/       - Create new country
    - GET    /api/countries/{id}/  - Get specific country
    - PUT    /api/countries/{id}/  - Update country
    - DELETE /api/countries/{id}/  - Delete country
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class ConditionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for coin conditions.

    Provides full CRUD operations for conditions (MS-65, AU-58, etc.)
    """
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


class CoinTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for coin types.

    Provides full CRUD operations for coin types (Morgan Dollar, Lincoln Cent, etc.)
    Includes related country information.
    """
    queryset = CoinType.objects.select_related('country').all()
    serializer_class = CoinTypeSerializer


class CoinViewSet(viewsets.ModelViewSet):
    """
    API endpoint for coins.

    Provides full CRUD operations for individual coins.
    Includes related coin type, condition, and country information.
    """
    queryset = Coin.objects.select_related(
        'type',
        'type__country',
        'condition'
    ).all()

    def get_serializer_class(self):
        """Use detailed serializer for single coin retrieval."""
        if self.action == 'retrieve':
            return CoinDetailSerializer
        return CoinSerializer

    @action(detail=False, methods=['get'], url_path='year/(?P<year>\d+)')
    def by_year(self, request, year: int):
        """
        Get all coins for a given year.

        Args:
            year: Year of the coins to get

        Returns:
            List of coins based on the year given
        """
        coins = self.queryset.filter(year=year)

        serializer = self.get_serializer(coins, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='year_range/(?P<start_year>\d+)/(?P<end_year>\d+)')
    def by_year_range(self, request, start_year: int, end_year: int):
        """
        Get all coins for a given year range.

        Args:
            start_year: Start year of the range
            end_year: End year of the range

        Returns:
            List of coins based on the year range given
        """
        coins = self.queryset.filter(year__gte=start_year, year__lte=end_year)

        serializer = self.get_serializer(coins, many=True)

        return Response(serializer.data)


@api_view(['GET'])
def stats_view(request):
    """
    Get collection statistics.

    Returns:
    - Total number of coins
    - Total estimated value
    - Total melt value (estimated at $35 per coin)
    - Number of unique coin types
    - Number of countries
    - Number of conditions

    Example response:
    {
        "total_coins": 19,
        "total_estimated_value": "450.00",
        "total_melt_value": "665.00",
        "coin_types_count": 5,
        "countries_count": 2,
        "conditions_count": 7
    }
    """
    # Calculate statistics
    coins = Coin.objects.all()
    total_coins = coins.count()

    # Sum of all coin value estimates
    value_aggregate = coins.aggregate(
        total_value=Sum('value_estimate')
    )
    total_estimated_value = value_aggregate['total_value'] or Decimal('0.00')

    # Melt value calculation ($35 per coin as in your CLI app)
    total_melt_value = Decimal('35.00') * total_coins

    # Count unique entities
    coin_types_count = CoinType.objects.count()
    countries_count = Country.objects.count()
    conditions_count = Condition.objects.count()

    # Prepare response data
    stats_data = {
        'total_coins': total_coins,
        'total_estimated_value': total_estimated_value,
        'total_melt_value': total_melt_value,
        'coin_types_count': coin_types_count,
        'countries_count': countries_count,
        'conditions_count': conditions_count,
    }

    # Validate and return
    serializer = StatsSerializer(stats_data)
    return Response(serializer.data)


@api_view(['GET'])
def api_root(request):
    """
    API root endpoint - provides overview of available endpoints.
    """
    return Response({
        'message': 'Welcome to the Coin Collection Tracker API!',
        'version': '1.0',
        'endpoints': {
            'coins': '/api/coins/',
            'coin_types': '/api/coin-types/',
            'conditions': '/api/conditions/',
            'countries': '/api/countries/',
            'stats': '/api/stats/',
        },
        'documentation': 'Visit any endpoint to see available operations.',
    })
