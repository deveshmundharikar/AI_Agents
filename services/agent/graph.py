import logging

from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes.planner import planner_node
from agent.nodes.executor import executor_node
from agent.nodes.responder import responder_node

logger = logging.getLogger(__name__)

def has_more_steps(state: AgentState):
    return state["current_step"] < len(state["plan"])

def create_graph():
    logger.info("Building graph")
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("responder", responder_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")

    graph.add_conditional_edges(
        "executor",
        has_more_steps,
        {True: "executor", False: "responder"}
    )

    graph.add_edge("responder", END)

    logger.info("Graph built")
    return graph.compile()
