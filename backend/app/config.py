"""
Application Configuration

Loads configuration from environment variables using pydantic-settings.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="Nike Agentic Commerce POC")
    app_version: str = Field(default="1.0.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=True)
    
    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    
    # Database
    database_url: str = Field(default="sqlite:///./data/checkout.db")
    test_database_url: str = Field(default="sqlite:///./data/test_checkout.db")
    
    # Stripe
    stripe_secret_key: str = Field(default="")
    stripe_publishable_key: str = Field(default="")
    stripe_webhook_secret: str = Field(default="")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production")
    api_key: str = Field(default="test-api-key")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    
    # CORS
    cors_origins: str = Field(default="http://localhost:5173,http://localhost:3000")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60)
    
    # Logging
    log_level: str = Field(default="INFO")
    log_file: str = Field(default="logs/app.log")
    
    # External Services
    nike_base_url: str = Field(default="https://www.nike.com")
    
    # Testing
    testing: bool = Field(default=False)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()

