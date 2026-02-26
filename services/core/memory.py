import os
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

log = logging.getLogger(__name__)
log.setLevel(os.getenv("LOG_LEVEL", "INFO"))
handler = logging.StreamHandler()
formatter = logging.Formatter(os.getenv("LOG_FORMAT", "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"))
handler.setFormatter(formatter)
log.addHandler(handler)

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from .embeddings import get_embeddings
from .config import settings

def get_memory_store():
    """Get Pinecone memory store with proper SDK v3+ initialization"""
    embeddings = get_embeddings()
    
    # Initialize PineconeVectorStore with index name
    # This uses the new langchain-pinecone package which handles SDK v3+ properly
    return PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings,
        text_key="text"
    )
