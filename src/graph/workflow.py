from src.agents.sample_demographics_agent import sample_demographics_node
from src.agents.study_metadata_agent import study_metadata_node
from src.agents.game_design_agent import game_design_node
from src.agents.game_parameters_agent import game_parameters_node
from src.agents.results_agent import results_node
from src.agents.synthesis_agent import synthesis_node

from src.graph.state import AgentState

from langgraph.graph import StateGraph, START, END

def build_workflow():
    # 1. Initialize graph with our shared state schema
    workflow = StateGraph(AgentState)

    # 2. Add our agents as nodes
    workflow.add_node("demographics_agent", sample_demographics_node)
    workflow.add_node("metadata_agent", study_metadata_node)
    workflow.add_node("game_design_agent", game_design_node)
    workflow.add_node("game_parameters_agent", game_parameters_node)
    workflow.add_node("results_agent", results_node)
    workflow.add_node("synthesis_agent", synthesis_node)

    # 3. Set entry points for full parallel execution (Fan-Out)
    # Drawing directed edges from START to all 5 extraction nodes tells 
    # the LangGraph engine to process all 5 RAG-LLM chains concurrently.
    workflow.add_edge(START, "demographics_agent")
    workflow.add_edge(START, "metadata_agent")
    workflow.add_edge(START, "game_design_agent")
    workflow.add_edge(START, "game_parameters_agent")
    workflow.add_edge(START, "results_agent")

    # 4. Define Synchronization Merge Point (Fan-In Barrier)
    # Because all upstream agents route directly to the "synthesis_agent",
    # the runtime manager acts as a synchronization barrier, holding execution 
    # until ALL 5 threads complete. The append-reducer seamlessly combines their payloads.
    workflow.add_edge("metadata_agent", "synthesis_agent")
    workflow.add_edge("demographics_agent", "synthesis_agent")
    workflow.add_edge("game_design_agent", "synthesis_agent")
    workflow.add_edge("game_parameters_agent", "synthesis_agent")
    workflow.add_edge("results_agent", "synthesis_agent")

    # 5. Define the End
    workflow.add_edge("synthesis_agent", END)

    return workflow.compile()
