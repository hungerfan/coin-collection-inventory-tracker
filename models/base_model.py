'''
Base model classes for coin collection inventory tracker.

This module provides base functionality shared across all model classes,
including database connection utilities and common methods.
'''

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseModel:
    '''Base class for all model entities with common functionality.'''

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the model object to a dictionary for database operations.

        Returns:
            dict: A dictionary containing all instance attributes as key-value pairs.
                 Keys match the database column names for easy database integration.
        '''
        return {key: value for key, value in self.__dict__.items()
                if not key.startswith('_')}

    def from_dict(self, data: Dict[str, Any]) -> 'BaseModel':
        '''Populate the model object from a dictionary (typically from database).

        Args:
            data (dict): Dictionary containing model data from database

        Returns:
            BaseModel: Self for method chaining
        '''
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def __str__(self) -> str:
        '''Default string representation of the model.'''
        attrs = []
        for key, value in self.to_dict().items():
            if value is not None:
                attrs.append(f"{key}={value}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __repr__(self) -> str:
        '''Detailed representation for debugging.'''
        return self.__str__()


class LookupModel(BaseModel):
    '''Base class for lookup/reference table models (CoinType, Condition, Country).'''

    def __init__(self, **kwargs):
        '''Initialize lookup model with database values.

        Args:
            **kwargs: Model attributes (id, name, etc.)
        '''
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)

    def __str__(self) -> str:
        '''Human-readable string representation.

        Returns:
            str: Formatted string showing id and name
        '''
        if self.name:
            return f"{self.name} (ID: {self.id})"
        return f"{self.__class__.__name__}(id={self.id})"
