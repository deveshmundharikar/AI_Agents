from agent.state import AgentState
from core.logger import get_logger
from core.config import settings

import logging

log = get_logger(__name__)
log.setLevel(settings.LOG_LEVEL)

TOOL_REGISTRY = {
    "jira.create": ("integrations.jira.jira_tools", "create_jira_ticket"),
    "slack.post": ("integrations.slack.slack_tools", "post_slack_message"),
    "email.read": ("integrations.email.email_tools", "read_email"),
    "calendar.create": ("integrations.calendar.calendar_tools", "create_calendar_event"),
}

def executor_node(state: AgentState):
    step = state["plan"][state["current_step"]]
    tool = step["tool"]
    params = step.get("params", {})

    log.info(f"Executing tool: {tool}")

    tool_info = TOOL_REGISTRY.get(tool)
    if tool_info is None:
        result = f"Tool not found: {tool}"
        log.error(result)
    else:
        tool_fn_module, tool_fn_name = tool_info
        try:
            # Normalize parameter names and channel for slack.post
            if tool == "slack.post":
                # Map "message" to "text" if needed
                if "message" in params and "text" not in params:
                    params["text"] = params.pop("message")
                
                # Normalize channel: remove # and default to agent_channal
                channel = params.get("channel", "agent_channal")
                channel = channel.replace("#", "")
                # Override with agent_channal if general or empty
                if channel == "general" or not channel:
                    channel = "agent_channal"
                params["channel"] = channel
            
            # Normalize parameter names for jira.create
            elif tool == "jira.create":
                # Map "project" to "project_key" if needed
                if "project" in params and "project_key" not in params:
                    params["project_key"] = params.pop("project")
            
            module = __import__(tool_fn_module, fromlist=[tool_fn_name])
            tool_fn = getattr(module, tool_fn_name)
            result = tool_fn(**params)
        except TypeError as e:
            result = f"Parameter error for {tool}: {str(e)}. Got params: {params}"
            log.error(result)
        except Exception as e:
            result = f"Error executing {tool}: {str(e)}"
            log.error(result)

    state["history"].append(f"{tool} → {result}")

    return {
        "tool_result": result,
        "current_step": state["current_step"] + 1,
        "history": state["history"]
    }
