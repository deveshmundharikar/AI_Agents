import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from core.config import settings

def get_llm():
    model_name = os.getenv("OPENROUTER_MODEL")
    return ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        model=model_name,
        temperature=0
    )
