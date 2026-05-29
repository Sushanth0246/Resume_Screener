from __future__ import annotations
 
from functools import lru_cache
 
from pydantic_settings import BaseSettings
 
 
class Settings(BaseSettings):
    google_api_key: str = "AIzaSyBhyk0KkhYe_oNdaxh4wpDll4fJmybOUmQ"
    # gemini-1.5-flash and all 1.x models shut down — use gemini-2.5-flash
    # text-embedding-004 / text-embedding-001 shut down Jan 2026 — use gemini-embedding-001
    embedding_model: str = "models/gemini-embedding-001"
    chat_model: str = "gemini-2.5-flash"
    max_upload_mb: int = 5
 
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
 
 
@lru_cache
def get_settings() -> Settings:
    return Settings()