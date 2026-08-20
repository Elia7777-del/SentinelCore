from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SentinelCore API"
    environment: str = "development"

    # MUST be replaced in production.
    secret_key: str = "CHANGE_ME_IN_PRODUCTION_TO_A_LONG_RANDOM_SECRET"
    database_url: str = "sqlite:///./sentinelcore.db"

    access_token_minutes: int = 30
    refresh_token_days: int = 7
    agent_token_days: int = 30

    cors_origins: str = "http://localhost:8501,http://localhost:3000"
    require_https: bool = False

    # AI Security Analyst (narrative layer only -- see
    # sentinelcore.analysis.analyst for why the deterministic pipeline
    # never depends on these being set). These are the DEPLOYMENT-WIDE
    # fallback provider, used only for organizations that haven't
    # configured their own AI credentials (see Organization.ai_api_url /
    # ai_api_key_encrypted and app.services.secrets_crypto). Empty
    # values disable the AI layer entirely for orgs without their own
    # config, and the analyst falls back to deterministic-only output.
    ai_api_url: str = ""
    ai_api_key: str = ""
    ai_model: str = "claude-sonnet-4-6"

    # Master key for encrypting per-organization secrets at rest (Fernet
    # key -- generate with app.services.secrets_crypto.generate_encryption_key()).
    # Required before any organization can store its own AI API key.
    encryption_key: str = ""

    model_config = SettingsConfigDict(
        env_prefix="SENTINELCORE_",
        env_file=".env",
        extra="ignore",
    )

settings = Settings()
