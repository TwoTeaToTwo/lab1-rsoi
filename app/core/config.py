from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # в будущем можно будет это получать из .env файла
    database_url: str = "postgresql+asyncpg://program:test@localhost:5432/persons"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# А зачем это здесь?
@lru_cache
def get_settings() -> Settings:
    return Settings()

