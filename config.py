"""Configuration management for Coin Tracker application."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    """Database configuration settings.

    Attributes:
        host: Database host address
        user: Database username
        password: Database password
        name: Database name
        port: Database port number
    """
    host: str
    user: str
    password: str
    name: str
    port: int

    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create database configuration from environment variables.

        Returns:
            DatabaseConfig instance populated from environment

        Raises:
            ValueError: If required configuration is missing
        """
        config = cls(
            host=os.getenv("DB_HOST", ""),
            user=os.getenv("DB_USER", ""),
            password=os.getenv("DB_PASSWORD", ""),
            name=os.getenv("DB_NAME", ""),
            port=int(os.getenv("DB_PORT", "3306"))
        )
        config.validate()
        return config

    def validate(self) -> None:
        """Validate required configuration values.

        Raises:
            ValueError: If required configuration is missing
        """
        if not self.host:
            raise ValueError("DB_HOST environment variable is required")
        if not self.user:
            raise ValueError("DB_USER environment variable is required")
        if not self.name:
            raise ValueError("DB_NAME environment variable is required")


# Global configuration instance
db_config = DatabaseConfig.from_env()
