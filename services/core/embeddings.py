import os
import logging

from langchain_openai import OpenAIEmbeddings
from core.config import settings

log = logging.getLogger(__name__)

def get_embeddings():
    log.info("Creating OpenAI embeddings")
    return OpenAIEmbeddings(
        openai_api_key=settings.OPENROUTER_API_KEY,
        openai_api_base=settings.OPENROUTER_BASE_URL,
        model=os.getenv("MODEL_NAME", "text-embedding-3-large")
    )
