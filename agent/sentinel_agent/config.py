from pydantic_settings import BaseSettings, SettingsConfigDict

class AgentSettings(BaseSettings):
    server_url: str = "http://localhost:8000"
    agent_token: str = ""
    verify_tls: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = AgentSettings()
