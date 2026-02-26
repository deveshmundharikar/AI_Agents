import json
from core.memory import get_memory_store
from core.llm import get_llm
from agent.prompts import PLANNER_PROMPT

def planner_node(state):
    llm = get_llm()
    
    # Try to get memory, but handle if Pinecone is not available
    try:
        memory = get_memory_store()
        memories = memory.similarity_search(
            state["user_input"], k=3
        )
        memory_context = "\n".join(
            [m.page_content for m in memories]
        )
    except Exception as e:
        print(f"Memory store not available: {e}")
        memory_context = "No previous context available"

    # Use safer string formatting to avoid KeyError with curly braces
    prompt = PLANNER_PROMPT.replace("{input}", state["user_input"]).replace("{memory}", memory_context)

    response = llm.invoke(prompt)
    
    # Try to parse JSON response
    try:
        content = response.content.strip()
        print(f"Raw LLM response: {content[:200]}...")
        
        # Remove markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        plan = json.loads(content)
        
        # Validate plan structure
        if not isinstance(plan, list):
            print(f"Warning: Plan is not a list, got: {type(plan)}")
            if isinstance(plan, dict) and "tool" in plan:
                plan = [plan]
            else:
                plan = [{"tool": "slack.post", "params": {"text": state["user_input"]}}]
        
        print(f"Parsed plan: {plan}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response as JSON: {e}")
        print(f"Response content: {response.content}")
        # Return a default plan
        plan = [{"tool": "slack.post", "params": {"text": state["user_input"]}}]

    return {
        "plan": plan,
        "current_step": 0,
        "history": []
    }

