'''
CoinType data model for coin collection inventory tracker.

This module provides the CoinType class for representing coin type information
such as Morgan Dollar, Lincoln Cent, etc. Contains denomination, metal type,
and country information.
'''

try:
    from .base_model import LookupModel  # pylint: disable=import-error
except ImportError:
    from base_model import LookupModel


class CoinType(LookupModel):
    '''
    Represents a type of coin with its characteristics.

    Coin types define the general characteristics of coins like denomination,
    metal composition, and country of origin. Examples include "Morgan Dollar",
    "Lincoln Cent", "Buffalo Nickel".

    Attributes:
        id (int): Unique identifier for the coin type in the database.
        name (str): Name of the coin type (e.g., 'Morgan Dollar').
        denomination (str): Coin denomination (e.g., '1 Dollar', '1 Cent').
        country_id (int): Foreign key reference to the country table.
        metal (str, optional): Primary metal composition (e.g., 'Silver', 'Gold').
    '''

    def __init__(self, **kwargs):
        '''Initialize CoinType with optional attribute values.

        Args:
            **kwargs: CoinType attributes (id, name, denomination, country_id, metal)
       '''
        super().__init__(**kwargs)
        self.denomination = kwargs.get('denomination', None)
        self.country_id = kwargs.get('country_id', None)
        self.metal = kwargs.get('metal', None)

    def __str__(self):
        '''Human-readable string representation of the coin type.'''
        metal_info = f" ({self.metal})" if self.metal else ""
        denomination_info = f" - {self.denomination}" if self.denomination else ""
        return f"{self.name}{denomination_info}{metal_info}"

    def to_dict(self):
        '''Convert the coin type object to a dictionary for database operations.

        Returns:
            dict: A dictionary containing all coin type attributes as key-value pairs.
        '''
        return {
            'id': self.id,
            'name': self.name,
            'denomination': self.denomination,
            'country_id': self.country_id,
            'metal': self.metal
        }


if __name__ == "__main__":
    # Test examples
    morgan_dollar = CoinType(id=1, name="Morgan Dollar", denomination="1 Dollar",
                             country_id=1, metal="Silver")

    lincoln_cent = CoinType(id=2, name="Lincoln Cent", denomination="1 Cent",
                            country_id=1, metal="Copper")

    print('Morgan Dollar:', morgan_dollar)
    print('Lincoln Cent:', lincoln_cent)
    print('Morgan dict:', morgan_dollar.to_dict())
