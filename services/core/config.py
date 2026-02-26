
import os
from pathlib import Path
import requests
from typing import Optional

# Find the project root directory (where .env is located)
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'

# Check if .env file exists
if not env_path.exists():
    raise FileNotFoundError(f'.env file not found at {env_path}')

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(dotenv_path=env_path)

# Environment variables are loaded from .env file

def check_connection_stability(url: str, timeout: int = 5) -> bool:
    """
    Check if the connection to the given URL is stable.
    
    Args:
        url: The URL to check
        timeout: Timeout in seconds for the request
        
    Returns:
        bool: True if connection is stable, False otherwise
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return True
        else:
            return False
    except (requests.ConnectionError, requests.Timeout, requests.RequestException):
        return False

class Settings:
    # OpenRouter API configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    MODEL_NAME = os.getenv("OPENROUTER_MODEL")

    # Langsmith API configuration
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

    # Pinecone configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "indexix")
    PINECONE_HOST = os.getenv("PINECONE_HOST", "https://indexix-lh6msbk.svc.aped-4627-b74a.pinecone.io")
    PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

    # Slack configuration
    SLACK_DEFAULT_CHANNEL = os.getenv("SLACK_DEFAULT_CHANNEL", "agent_channal")

    # Logger configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @staticmethod
    def verify_connections() -> dict:
        """
        Verify if connections to external services are stable.
        
        Returns:
            dict: Dictionary with connection status for each service
        """
        connection_status = {}
        
        # Check OpenRouter connection
        if Settings.OPENROUTER_BASE_URL:
            is_stable = check_connection_stability(Settings.OPENROUTER_BASE_URL)
            if is_stable:
                connection_status['openrouter'] = 'stable'
            else:
                connection_status['openrouter'] = 'unstable'
        else:
            connection_status['openrouter'] = 'not_configured'
        
        # Check Langsmith connection (if applicable)
        langsmith_url = "https://api.smith.langchain.com"
        if Settings.LANGSMITH_API_KEY:
            is_stable = check_connection_stability(langsmith_url)
            if is_stable:
                connection_status['langsmith'] = 'stable'
            else:
                connection_status['langsmith'] = 'unstable'
        else:
            connection_status['langsmith'] = 'not_configured'
        
        return connection_status

settings = Settings()

# Optionally verify connections on initialization
# Uncomment the following lines if you want to check connections when config is loaded
# connection_status = settings.verify_connections()
# if connection_status.get('openrouter') == 'unstable':
#     print("Warning: OpenRouter connection is unstable")
# if connection_status.get('langsmith') == 'unstable':
#     print("Warning: Langsmith connection is unstable")
