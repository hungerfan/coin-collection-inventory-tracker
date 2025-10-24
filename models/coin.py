"""
Coin collection inventory tracker - Coin data model.

This module provides the Coin class for representing individual coins in a collection.
The Coin class serves as the primary data model for storing coin metadata including
identification, condition, value estimates, and acquisition details.

Key features:
    - Structured data storage for coin attributes
    - Dictionary conversion for database operations
    - String representation for display and debugging
    - Integration with the coin collection inventory system
"""

try:
    from .base_model import BaseModel  # pylint: disable=import-error
except ImportError:
    from base_model import BaseModel


class Coin(BaseModel):  # pylint: disable=too-many-instance-attributes
    """
    Represents a single coin in a collection with all relevant metadata.

    This class encapsulates all the information needed to track and manage
    individual coins, including identification, condition, value, and any relevant notes.

    Attributes:
        id (int): Unique identifier for the coin in the database.
        type_id (int): Foreign key reference to the coin type (e.g., Morgan Dollar).
        year (int): Year the coin was minted.
        mint_mark (str): Mint location identifier (e.g., 'S' for San Francisco).
        condition_id (str): Coin condition grade (e.g., 'MS-65', 'VF-20').
        quantity (int): Number of this specific coin in the collection.
        value_estimate (float): Estimated current value of the coin.
        acquired_from (str): Source or method of acquisition.
        notes (str): Additional notes or observations about the coin.
    """

    def __init__(self, **kwargs):
        """Initialize Coin with optional attribute values.

        Args:
            **kwargs: Coin attributes (id, type_id, year, mint_mark, etc.)
        """
        self.id = kwargs.get("id", None)
        self.type_id = kwargs.get("type_id", None)
        self.year = kwargs.get("year", None)
        self.mint_mark = kwargs.get("mint_mark", None)
        self.condition_id = kwargs.get("condition_id", None)
        self.quantity = kwargs.get("quantity", None)
        self.value_estimate = kwargs.get("value_estimate", None)
        self.acquired_from = kwargs.get("acquired_from", None)
        self.notes = kwargs.get("notes", None)

    def __str__(self):
        """Human-readable string representation of the coin."""
        return (
            f"ID: {self.id} - Type ID: {self.type_id} - Year: {self.year} - "
            f"Mint Mark: {self.mint_mark} - Condition: {self.condition_id} - "
            f"Quantity: {self.quantity} - Value Estimate: {self.value_estimate} - "
            f"Acquired From: {self.acquired_from} - Notes: {self.notes}"
        )

    def __repr__(self):
        """Detailed representation for debugging."""
        return (
            f"Coin(id={self.id}, type_id={self.type_id}, year={self.year}, "
            f"mint_mark={self.mint_mark}, condition_id={self.condition_id}, "
            f"quantity={self.quantity}, value_estimate={self.value_estimate}, "
            f"acquired_from={self.acquired_from}, notes={self.notes})"
        )

    def to_dict(self):
        """Convert the coin object to a dictionary for database operations or serialization.

        Returns:
            dict: A dictionary containing all coin attributes as key-value pairs.
                 Keys match the database column names for easy database integration.
        """
        return {
            "id": self.id,
            "type_id": self.type_id,
            "year": self.year,
            "mint_mark": self.mint_mark,
            "condition_id": self.condition_id,
            "quantity": self.quantity,
            "value_estimate": self.value_estimate,
            "acquired_from": self.acquired_from,
            "notes": self.notes,
        }


# TODO: remove this main function before deployment
if __name__ == "__main__":
    selected_coin = {
        "id": 1,
        "type_id": 1,
        "year": 1890,
        "mint_mark": "D",
        "condition_id": "VF-20",
        "quantity": 1,
        "value_estimate": 45.00,
        "acquired_from": "Bar",
        "notes": "Test Coin",
    }
    coin = Coin(
        **selected_coin
    )

    coin2 = Coin()
    coin2.id = 2
    coin2.type_id = 3
    coin2.year = 1999
    coin2.mint_mark = "S"
    coin2.condition_id = "VF-20"
    coin2.quantity = 1
    coin2.value_estimate = 45.00
    coin2.acquired_from = "Foo"
    coin2.notes = "Test Coin"

    print("coin:", coin)
    print("coin2:", coin2)
    print("--------------------------------")
    print("str(coin):", str(coin))
    print("repr(coin):", repr(coin))
    coin_dict = coin.to_dict()
    print("--------------------------------")
    print("coin_dict:", coin_dict)
    print('coin_dict["year"]:', coin_dict["year"])
