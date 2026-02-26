import os
from core.config import settings

def setup_langsmith():
    if not settings.LANGSMITH_API_KEY:
        raise ValueError("LANGSMITH_API_KEY is not set in environment variables")
    
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT or "task-automation-agent"
