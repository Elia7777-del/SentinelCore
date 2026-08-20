"""Configuration loaded from environment variables."""
from __future__ import annotations
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("SENTINELCORE_APP_NAME", "SentinelCore")
    environment: str = os.getenv("SENTINELCORE_ENV", "development")
    log_level: str = os.getenv("SENTINELCORE_LOG_LEVEL", "INFO")
    ai_api_url: str = os.getenv("AI_API_URL", "")
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    database_url: str = os.getenv("SENTINELCORE_DATABASE_URL", "sqlite:///sentinelcore.db")

settings = Settings()
