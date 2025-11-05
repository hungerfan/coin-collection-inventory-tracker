"""
Serializers for coin collection tracker API.

Serializers convert Django models to/from JSON for API responses.
They handle validation and data transformation.
"""
from rest_framework import serializers
from .models import Coin, CoinType, Condition, Country


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model."""

    class Meta:
        model = Country
        fields = ['id', 'name', 'country_code']
        read_only_fields = ['id']


class ConditionSerializer(serializers.ModelSerializer):
    """Serializer for Condition model."""

    class Meta:
        model = Condition
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class CoinTypeSerializer(serializers.ModelSerializer):
    """Serializer for CoinType model."""

    country_name = serializers.CharField(source='country.name', read_only=True)
    country_code = serializers.CharField(
        source='country.country_code', read_only=True)

    class Meta:
        model = CoinType
        fields = [
            'id',
            'name',
            'denomination',
            'country',
            'country_name',
            'country_code',
            'metal'
        ]
        read_only_fields = ['id']


class CoinSerializer(serializers.ModelSerializer):
    """Serializer for Coin model."""

    # Read-only fields for displaying related data
    coin_type_name = serializers.CharField(source='type.name', read_only=True)
    condition_name = serializers.CharField(
        source='condition.name', read_only=True)
    country_name = serializers.CharField(
        source='type.country.name', read_only=True)
    country_code = serializers.CharField(
        source='type.country.country_code', read_only=True)
    denomination = serializers.CharField(
        source='type.denomination', read_only=True)
    metal = serializers.CharField(source='type.metal', read_only=True)

    class Meta:
        model = Coin
        fields = [
            'id',
            'type',
            'coin_type_name',
            'year',
            'mint_mark',
            'condition',
            'condition_name',
            'quantity',
            'value_estimate',
            'acquired_from',
            'notes',
            'country_name',
            'country_code',
            'denomination',
            'metal',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CoinDetailSerializer(CoinSerializer):
    """
    Detailed serializer for Coin with full nested objects.
    Used for single coin retrieval.
    """

    type_details = CoinTypeSerializer(source='type', read_only=True)
    condition_details = ConditionSerializer(source='condition', read_only=True)

    class Meta(CoinSerializer.Meta):
        fields = CoinSerializer.Meta.fields + \
            ['type_details', 'condition_details']


class StatsSerializer(serializers.Serializer):
    """Serializer for collection statistics."""

    total_coins = serializers.IntegerField()
    total_quantity = serializers.IntegerField()
    total_estimated_value = serializers.DecimalField(
        max_digits=10, decimal_places=2)
    total_melt_value = serializers.DecimalField(
        max_digits=10, decimal_places=2)
    coin_types_count = serializers.IntegerField()
    countries_count = serializers.IntegerField()
    conditions_count = serializers.IntegerField()
