import logging
import requests
from requests.auth import HTTPBasicAuth
import os

log = logging.getLogger(__name__)

def create_jira_ticket(summary, description, project_key="PROJ"):
    """
    Create a Jira ticket with the given summary and description.
    
    Args:
        summary (str): The summary/title of the ticket
        description (str): The detailed description of the ticket
        project_key (str): The Jira project key (defaults to "PROJ")
    
    Returns:
        dict: Response from Jira API or error information
    """
    # Validate required environment variables
    jira_base_url = os.getenv('JIRA_BASE_URL')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_api_token = os.getenv('JIRA_API_TOKEN')
    
    if not all([jira_base_url, jira_email, jira_api_token]):
        missing_vars = [var for var, value in {
            'JIRA_BASE_URL': jira_base_url,
            'JIRA_EMAIL': jira_email,
            'JIRA_API_TOKEN': jira_api_token
        }.items() if not value]
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        log.error(error_msg)
        return {"error": error_msg}
    
    url = f"{jira_base_url}/rest/api/3/issue"
    
    auth = HTTPBasicAuth(jira_email, jira_api_token)
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"}
        }
    }
    
    try:
        log.info(f"Creating Jira ticket: {summary} in project {project_key}")
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            log.info(f"Successfully created Jira ticket: {result.get('key', 'Unknown key')}")
            return result
        else:
            error_msg = f"Failed to create Jira ticket. Status: {response.status_code}, Response: {response.text}"
            log.error(error_msg)
            return {"error": error_msg}
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {str(e)}"
        log.error(error_msg)
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        log.error(error_msg)
        return {"error": error_msg}
