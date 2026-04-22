import os
from app.config import get_settings

settings = get_settings()

def setup_tracing():
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"]    = settings.langsmith_api_key
    os.environ["LANGCHAIN_PROJECT"]    = settings.langchain_project

def get_callbacks():
    try:
        from langsmith import Client
        from langchain.callbacks import LangChainTracer
        return [LangChainTracer(
            project_name=settings.langchain_project,
            client=Client(api_key=settings.langsmith_api_key),
        )]
    except Exception:
        return []