"""CoinType data model for coin collection inventory tracker.

This module provides the CoinType class for representing coin type information
such as Morgan Dollar, Lincoln Cent, etc. Contains denomination, metal type,
and country information.
"""

try:
    from .base_model import LookupModel  # pylint: disable=import-error
except ImportError:
    from base_model import LookupModel


class CoinType(LookupModel):
    """Represents a type of coin with its characteristics.

    Coin types define the general characteristics of coins like denomination,
    metal composition, and country of origin. Examples include "Morgan Dollar",
    "Lincoln Cent", "Buffalo Nickel".

    Attributes:
        id: Unique identifier for the coin type in the database
        name: Name of the coin type (e.g., 'Morgan Dollar')
        denomination: Coin denomination (e.g., '1 Dollar', '1 Cent')
        country_id: Foreign key reference to the country table
        metal: Primary metal composition (e.g., 'Silver', 'Gold')
    """

    def __init__(self, **kwargs):
        """Initialize CoinType with optional attribute values.

        Args:
            **kwargs: CoinType attributes (id, name, denomination, country_id, metal)
        """
        super().__init__(**kwargs)
        self.denomination = kwargs.get("denomination", None)
        self.country_id = kwargs.get("country_id", None)
        self.metal = kwargs.get("metal", None)

    def __str__(self):
        """Human-readable string representation of the coin type."""
        metal_info = f" ({self.metal})" if self.metal else ""
        denomination_info = f" - {self.denomination}" if self.denomination else ""
        return f"{self.name}{denomination_info}{metal_info}"
