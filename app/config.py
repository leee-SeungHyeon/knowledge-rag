from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"

    notes_dir: Path = Path("./sample_notes")
    chroma_dir: Path = Path("./chroma_db")

    chunk_size: int = 800
    chunk_overlap: int = 100
    top_k: int = 4


settings = Settings()
