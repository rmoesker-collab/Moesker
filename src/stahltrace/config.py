from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    database_url: str = Field(
        default="postgresql://stahltrace:stahltrace@localhost:5432/stahltrace",
        alias="DATABASE_URL",
    )
    model: str = Field(default="claude-sonnet-4-6", alias="STAHLTRACE_MODEL")


settings = Settings()
