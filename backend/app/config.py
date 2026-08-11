from functools import lru_cache
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    app_name: str = "Company Application"
    environment: Literal["development", "test", "production"] = "development"
    database_url: str = "sqlite:///./data/app.db"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    allowed_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "testserver"]
    )
    log_level: str = "INFO"
    auto_create_schema: bool = True

    @model_validator(mode="after")
    def validate_production_safety(self) -> "Settings":
        if self.environment == "production" and "*" in self.cors_origins:
            raise ValueError("Wildcard CORS is forbidden in production")
        if self.environment == "production" and self.auto_create_schema:
            raise ValueError("Production must use Alembic migrations")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
