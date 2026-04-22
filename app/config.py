from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    openai_api_key: str
    langsmith_api_key: str = ""
    helicone_api_key: str = ""
    postgres_url: str = "postgresql://user:pass@localhost/knowledge_db"
    redis_url: str = "redis://localhost:6379"
    chroma_path: str = "data/chroma"
    upload_dir: str = "data/raw"
    langchain_tracing_v2: str = "true"
    langchain_project: str = "personal-ai-assistant"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()