from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_api_key: str = ""
    embedding_model: str = "models/text-embedding-004"
    chat_model: str = "gemini-1.5-flash"
    max_upload_mb: int = 5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
