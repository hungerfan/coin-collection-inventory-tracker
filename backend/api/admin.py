"""
Django admin configuration for coin collection tracker.

This creates a beautiful admin interface at http://localhost:8000/admin/
"""
from django.contrib import admin
from .models import Coin, CoinType, Condition, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin interface for Country model."""
    list_display = ['id', 'name', 'country_code']
    search_fields = ['name', 'country_code']
    ordering = ['name']


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    """Admin interface for Condition model."""
    list_display = ['id', 'name', 'description']
    search_fields = ['name', 'description']
    ordering = ['id']


@admin.register(CoinType)
class CoinTypeAdmin(admin.ModelAdmin):
    """Admin interface for CoinType model."""
    list_display = ['id', 'name', 'denomination', 'country', 'metal']
    list_filter = ['country', 'metal']
    search_fields = ['name', 'denomination']
    ordering = ['country__name', 'name']


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    """Admin interface for Coin model."""
    list_display = [
        'id',
        'reference_number',
        'type',
        'year',
        'mint_mark',
        'condition',
        'quantity',
        'value_estimate',
        'created_at'
    ]
    list_filter = ['type', 'condition', 'year']
    search_fields = ['reference_number',
                     'type__name', 'year', 'mint_mark', 'notes']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    # Group fields in the form
    fieldsets = (
        ('Coin Information', {
            'fields': ('reference_number', 'type', 'year', 'mint_mark'),
            'description': 'Leave Reference # blank to auto-assign next number'
        }),
        ('Condition and Value', {
            'fields': ('condition', 'quantity', 'value_estimate')
        }),
        ('Acquisition', {
            'fields': ('acquired_from', 'notes')
        }),
    )
