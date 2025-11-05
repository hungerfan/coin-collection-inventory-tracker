"""Coin collection inventory tracker - Coin data model.

This module provides the Coin class for representing individual coins in a collection.
The Coin class serves as the primary data model for storing coin metadata including
identification, condition, value estimates, and acquisition details.
"""

try:
    from .base_model import BaseModel  # pylint: disable=import-error
except ImportError:
    from base_model import BaseModel


class Coin(BaseModel):  # pylint: disable=too-many-instance-attributes
    """Represents a single coin in a collection with all relevant metadata.

    This class encapsulates all the information needed to track and manage
    individual coins, including identification, condition, value, and any relevant notes.

    Attributes:
        id: Unique identifier for the coin in the database
        reference_number: Physical label number for coin flip (001-999)
        type_id: Foreign key reference to the coin type (e.g., Morgan Dollar)
        year: Year the coin was minted
        mint_mark: Mint location identifier (e.g., 'S' for San Francisco)
        condition_id: Coin condition grade ID reference
        quantity: Number of this specific coin in the collection
        value_estimate: Estimated current value of the coin
        acquired_from: Source or method of acquisition
        notes: Additional notes or observations about the coin
    """

    def __init__(self, **kwargs):
        """Initialize Coin with optional attribute values.

        Args:
            **kwargs: Coin attributes (id, reference_number, type_id, year, mint_mark, etc.)
        """
        self.id = kwargs.get("id", None)
        self.reference_number = kwargs.get("reference_number", None)
        self.type_id = kwargs.get("type_id", None)
        self.year = kwargs.get("year", None)
        self.mint_mark = kwargs.get("mint_mark", None)
        self.condition_id = kwargs.get("condition_id", None)
        self.quantity = kwargs.get("quantity", None)
        self.value_estimate = kwargs.get("value_estimate", None)
        self.acquired_from = kwargs.get("acquired_from", None)
        self.notes = kwargs.get("notes", None)
