from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "local"
    database_url: str = "sqlite+pysqlite:///./app.sqlite3"

    llm_mode: str = "mock"  # mock|real
    embeddings_mode: str = "mock"  # mock|real

    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    log_level: str = "INFO"

settings = Settings()
