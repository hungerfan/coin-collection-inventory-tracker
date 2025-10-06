"""
Condition data model for coin collection inventory tracker.

This module provides the Condition class for representing coin grading conditions
such as MS-65, AU-58, VF-20, etc. Used for describing the wear and state of coins.
"""

try:
    from .base_model import LookupModel  # pylint: disable=import-error
except ImportError:
    from base_model import LookupModel


class Condition(LookupModel):
    """
    Represents a coin condition grade.

    Coin conditions describe the wear, luster, and overall state of coins.
    Examples include "MS-65" (Mint State), "AU-58" (About Uncirculated),
    "VF-20" (Very Fine), etc.

    Attributes:
        id (int): Unique identifier for the condition in the database.
        name (str): Condition grade name (e.g., 'MS-65', 'AU-58', 'VF-20').
        description (str, optional): Detailed description of the condition grade.
    """

    def __init__(self, **kwargs):
        """Initialize Condition with optional attribute values.

        Args:
            **kwargs: Condition attributes (id, name, description)
        """
        super().__init__(**kwargs)
        self.description = kwargs.get("description", None)

    def __str__(self):
        """Human-readable string representation of the condition."""
        desc_info = f" - {self.description}" if self.description else ""
        return f"{self.name}{desc_info}" if self.name else f"Condition(id={self.id})"

    def to_dict(self):
        """Convert the condition object to a dictionary for database operations.

        Returns:
            dict: A dictionary containing all condition attributes as key-value pairs.
        """
        return {"id": self.id, "name": self.name, "description": self.description}


if __name__ == "__main__":
    # Test examples
    ms65 = Condition(
        id=1, name="MS-65", description="Mint State 65 - Choice Brilliant Uncirculated"
    )

    au58 = Condition(
        id=2, name="AU-58", description="About Uncirculated 58 - Trace of wear"
    )

    vf20 = Condition(id=3, name="VF-20", description="Very Fine 20 - Well worn")

    print("MS-65:", ms65)
    print("AU-58:", au58)
    print("VF-20:", vf20)
    print("MS-65 dict:", ms65.to_dict())
