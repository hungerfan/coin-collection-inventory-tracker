"""Condition data model for coin collection inventory tracker.

This module provides the Condition class for representing coin grading conditions
such as MS-65, AU-58, VF-20, etc. Used for describing the wear and state of coins.
"""

try:
    from .base_model import LookupModel  # pylint: disable=import-error
except ImportError:
    from base_model import LookupModel


class Condition(LookupModel):
    """Represents a coin condition grade.

    Coin conditions describe the wear, luster, and overall state of coins.
    Examples include "MS-65" (Mint State), "AU-58" (About Uncirculated),
    "VF-20" (Very Fine), etc.

    Attributes:
        id: Unique identifier for the condition in the database
        name: Condition grade name (e.g., 'MS-65', 'AU-58', 'VF-20')
        description: Detailed description of the condition grade
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
