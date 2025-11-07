"""
Django models for coin collection tracker.

These models map to the existing MySQL database tables.
Django will NOT create new tables - it will use the existing ones!
"""
from django.db import models


class Country(models.Model):
    """Country model - represents countries that issue coins."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3, unique=True)

    class Meta:
        db_table = 'countries'
        managed = False  # Table managed by CLI app, not Django
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __str__(self):
        """String representation."""
        return f"{self.name} ({self.country_code})"


class CoinType(models.Model):
    """CoinType model - represents types of coins (Morgan Dollar, Lincoln Cent, etc.)."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    denomination = models.CharField(max_length=50, null=True, blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,  # Don't allow deleting countries with coin types
        db_column='country_id',
        related_name='coin_types'
    )
    metal = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'coin_types'
        managed = False  # Table managed by CLI app, not Django
        ordering = ['country__name', 'name']

    def __str__(self):
        """String representation."""
        return f"{self.name} - {self.denomination}" if self.denomination else self.name


class Condition(models.Model):
    """Condition model - represents coin conditions (MS-65, AU-58, etc.)."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'conditions'
        managed = False  # Table managed by CLI app, not Django
        ordering = ['id']

    def __str__(self):
        """String representation."""
        return self.name


class Coin(models.Model):
    """Coin model - represents individual coins in the collection."""

    id = models.AutoField(primary_key=True)
    reference_number = models.IntegerField(
        unique=True,
        null=True,
        blank=True,
        verbose_name='Ref #'
    )
    type = models.ForeignKey(
        CoinType,
        on_delete=models.PROTECT,  # Don't allow deleting coin types with coins
        db_column='type_id',
        related_name='coins'
    )
    # Required in forms, optional in DB
    year = models.IntegerField(null=True, blank=False)
    mint_mark = models.CharField(max_length=10, null=True, blank=True)
    condition = models.ForeignKey(
        Condition,
        on_delete=models.PROTECT,
        db_column='condition_id',
        related_name='coins'
    )
    quantity = models.IntegerField(default=1)
    value_estimate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    acquired_from = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'coins'
        managed = False  # Table managed by CLI app, not Django
        ordering = ['-created_at']  # Newest first

    def save(self, *args, **kwargs):
        """Override save to auto-assign reference_number if not provided."""
        if self.reference_number is None:
            # Get the next available reference number
            from django.db.models import Max
            max_ref = Coin.objects.aggregate(Max('reference_number'))[
                'reference_number__max']
            self.reference_number = (max_ref or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation."""
        return f"{self.type.name} ({self.year or 'N/A'})"

    @property
    def coin_type_name(self):
        """Get coin type name for serialization."""
        return self.type.name if self.type else None

    @property
    def condition_name(self):
        """Get condition name for serialization."""
        return self.condition.name if self.condition else None

    @property
    def country_name(self):
        """Get country name for serialization."""
        return self.type.country.name if self.type and self.type.country else None

    @property
    def country_code(self):
        """Get country code for serialization."""
        return self.type.country.country_code if self.type and self.type.country else None
