import os
import logging
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from pathlib import Path


# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

log = logging.getLogger(__name__)

# Initialize Slack client with bot token
slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    # Try loading directly from env file
    load_dotenv('.env')
    slack_token = os.getenv("SLACK_BOT_TOKEN")

client = WebClient(token=slack_token) if slack_token else None


def post_slack_message(channel="#general", text=""):
    """Post a message to a Slack channel"""
    if not client:
        log.error("Slack bot token not configured")
        return "Error: Slack bot token not configured"
    
    try:
        log.info(f"Posting Slack message to {channel}")
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
        log.info(f"Message sent successfully: {response['ts']}")
        return f"Slack message sent to {channel}: {text}"
    except SlackApiError as e:
        error_msg = f"Slack API error: {e.response['error']}"
        log.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error sending Slack message: {str(e)}"
        log.error(error_msg)
        return error_msg
