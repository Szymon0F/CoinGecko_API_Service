from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings."""

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "CoinGecko API Service"
    VERSION: str = "0.1.0"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/coingecko")

    # CoinGecko API
    COINGECKO_API_URL: str = os.getenv(
        "COINGECKO_API_URL", "https://api.coingecko.com/api/v3")

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
