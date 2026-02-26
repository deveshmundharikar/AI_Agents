import os
import logging
from dotenv import load_dotenv
from core.config import settings
from pinecone import Pinecone

load_dotenv()

log = logging.getLogger(__name__)
log.setLevel(os.getenv("LOG_LEVEL", "INFO"))

def init_pinecone():
    log.info("Initializing Pinecone")
    
    # Use settings from config
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    
    index_name = settings.PINECONE_INDEX_NAME
    
    # Check if index exists
    existing_indexes = [index.name for index in pc.list_indexes()]
    if index_name not in existing_indexes:
        log.info(f"Creating Pinecone index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec={"serverless": {"cloud": "aws", "region": settings.PINECONE_REGION}}
        )
    
    log.info(f"Returning Pinecone index: {index_name}")
    # Use index name only for SDK v3+
    return pc.Index(index_name)


