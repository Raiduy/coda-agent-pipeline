from src.agents.methodology import methodology_node
from src.agents.results import results_node
from src.agents.synthesis import synthesis_node
from src.graph.state import AgentState

from langgraph.graph import StateGraph, END

def build_workflow():
    # 1. Initialize graph with our shared state schema
    workflow = StateGraph(AgentState)

    # 2. Add our agents as nodes
    workflow.add_node("methodology_agent", methodology_node)
    workflow.add_node("results_agent", results_node)
    workflow.add_node("synthesis_agent", synthesis_node)

    # 3. Set the Entry Point
    # We want methodology and results to run at the SAME time (Parallel)
    workflow.set_entry_point("methodology_agent")
    workflow.set_entry_point("results_agent") 

    # 4. Define Collaboration (Sequential)
    # Both parallel agents must finish before sending data to the synthesis agent
    workflow.add_edge("methodology_agent", "synthesis_agent")
    workflow.add_edge("results_agent", "synthesis_agent")

    # 5. Define the End
    workflow.add_edge("synthesis_agent", END)

    return workflow.compile()
