import logging

from typing import TypedDict, List, Any


class AgentState(TypedDict):
    user_input: str
    plan: List[dict]
    current_step: int
    tool_result: Any
    history: List[str]


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
