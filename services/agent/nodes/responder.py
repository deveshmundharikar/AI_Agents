import logging

from core.llm import get_llm
from core.memory import get_memory_store
from agent.prompts import RESPONDER_PROMPT
from agent.state import AgentState
from core.logger import get_logger

log = get_logger(__name__)

def responder_node(state: AgentState):
    llm = get_llm()
    
    # Try to use memory store, but handle if Pinecone is not available
    try:
        memory = get_memory_store()
        memory.add_texts([
            f"User action: {state['history']}"
        ])
    except Exception as e:
        print(f"Memory store not available: {e}")

    response = llm.invoke(
        RESPONDER_PROMPT + "\n" + "\n".join(state["history"])
    )

    return {"final_response": response.content}
