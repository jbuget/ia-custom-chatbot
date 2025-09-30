from __future__ import annotations

from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


def _default_cors_origins() -> List[str]:
    return ["http://localhost:3000", "http://127.0.0.1:3000"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_prefix="",
        extra="ignore",
    )

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gpt-oss:20b"
    ollama_timeout_seconds: float = 60.0

    database_url: str = "postgresql://admin:password@localhost:5432/chatbot"

    embedding_model: str = "nomic-embed-text"
    embedding_timeout_seconds: float = 60.0
    embedding_expected_dimensions: int = 768

    retriever_top_k: int = 3
    retriever_context_char_limit: int = 2000

    cors_allow_origins: List[str] = _default_cors_origins()
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]


settings = Settings()

__all__ = ["Settings", "settings"]
