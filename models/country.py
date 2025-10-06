'''
Country data model for coin collection inventory tracker.

This module provides the Country class for representing country/region information
for coin types. Contains country names and ISO codes for internationalization.
'''

try:
    from .base_model import LookupModel  # pylint: disable=import-error
except ImportError:
    from base_model import LookupModel


class Country(LookupModel):
    '''
    Represents a country or region that issues coins.

    Countries define the origin of coin types. Examples include "United States",
    "Canada", "Australia", etc. Includes both full names and ISO country codes.

    Attributes:
        id (int): Unique identifier for the country in the database.
        name (str): Full country name (e.g., 'United States').
        country_code (str): ISO country code (e.g., 'US', 'CA', 'AU').
    '''

    def __init__(self, **kwargs):
        '''Initialize Country with optional attribute values.

        Args:
            **kwargs: Country attributes (id, name, country_code)
        '''
        super().__init__(**kwargs)
        self.country_code = kwargs.get('country_code', None)

    def __str__(self):
        '''Human-readable string representation of the country.'''
        code_info = f" ({self.country_code})" if self.country_code else ""
        return f"{self.name}{code_info}" if self.name else f"Country(id={self.id})"

    def to_dict(self):
        '''Convert the country object to a dictionary for database operations.

        Returns:
            dict: A dictionary containing all country attributes as key-value pairs.
        '''
        return {
            'id': self.id,
            'name': self.name,
            'country_code': self.country_code
        }


if __name__ == "__main__":
    # Test examples
    usa = Country(id=1, name="United States", country_code="US")

    canada = Country(id=2, name="Canada", country_code="CA")

    australia = Country(id=3, name="Australia", country_code="AU")

    print('USA:', usa)
    print('Canada:', canada)
    print('Australia:', australia)
    print('USA dict:', usa.to_dict())
