'''
Models package for coin collection inventory tracker.

This package contains all data model classes used throughout the application.
Organized into separate modules for better maintainability and import clarity.

Available models:
    - Coin: Individual coin entities with full metadata
    - CoinType: Coin type lookup (Morgan Dollar, etc.)
    - Condition: Coin condition grades (MS-65, AU-58, etc.)
    - Country: Country/region lookup (US, CA, AU, etc.)
    - BaseModel: Shared functionality and utilities
    - LookupModel: Base class for lookup table models
'''

from .coin import Coin
from .coin_type import CoinType
from .condition import Condition
from .country import Country
from .base_model import BaseModel, LookupModel

__all__ = [
    'Coin',
    'CoinType',
    'Condition',
    'Country',
    'BaseModel',
    'LookupModel'
]

__version__ = '1.0.0'
