from src.agents.splitter_agent import splitter_node
from src.agents.sample_demographics_agent import sample_demographics_node
from src.agents.study_metadata_agent import study_metadata_node
from src.agents.game_design_agent import game_design_node
from src.agents.game_parameters_agent import game_parameters_node
from src.agents.results_agent import results_node
from src.agents.synthesis_agent import synthesis_node

from src.graph.state import AgentState, MainState

from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send

def build_sub_graph():
    # 1. Initialize graph with our shared state schema
    sg = StateGraph(AgentState)

    # 2. Add our agents as nodes
    sg.add_node("demographics_agent", sample_demographics_node)
    sg.add_node("metadata_agent", study_metadata_node)
    sg.add_node("game_design_agent", game_design_node)
    sg.add_node("game_parameters_agent", game_parameters_node)
    sg.add_node("results_agent", results_node)
    sg.add_node("synthesis_agent", synthesis_node)

    # 3. Set entry points for full parallel execution (Fan-Out)
    # Drawing directed edges from START to all 5 extraction nodes tells 
    # the LangGraph engine to process all 5 RAG-LLM chains concurrently.
    sg.add_edge(START, "demographics_agent")
    sg.add_edge(START, "metadata_agent")
    sg.add_edge(START, "game_design_agent")
    sg.add_edge(START, "game_parameters_agent")
    sg.add_edge(START, "results_agent")

    # 4. Define Synchronization Merge Point (Fan-In Barrier)
    # Because all upstream agents route directly to the "synthesis_agent",
    # the runtime manager acts as a synchronization barrier, holding execution 
    # until ALL 5 threads complete. The append-reducer seamlessly combines their payloads.
    sg.add_edge("metadata_agent", "synthesis_agent")
    sg.add_edge("demographics_agent", "synthesis_agent")
    sg.add_edge("game_design_agent", "synthesis_agent")
    sg.add_edge("game_parameters_agent", "synthesis_agent")
    sg.add_edge("results_agent", "synthesis_agent")

    # 5. Define the End
    sg.add_edge("synthesis_agent", END)

    return sg.compile()


def route_to_sub_studies(state: MainState):
    """
    This function acts as the MAPPER. For every study identified by the splitter,
    it Spawns a dedicated Sub-Graph using the `Send` API.
    """
    studies = state.get("identified_studies", [])
    
    # If no studies found, fallback to a default study 1
    if not studies:
        studies = [{"study_num": "1", "description": "Main study"}]
        
    sends = []
    for study in studies:
        # Create a clean sub-state for this specific run
        sub_state = {
            "paper_id": state["paper_id"],
            "vector_store": state["vector_store"],
            "target_study_num": study["study_num"],
            "target_study_desc": study["description"],
            "extracted_features": [], # Start empty!
            "final_consolidated_record": {},
            "translated_cookbook_record": {}
        }
        # Spawn a branch of "process_sub_study" with this state
        sends.append(Send("process_sub_study", sub_state))
        
    return sends


def aggregate_sub_studies(state: AgentState):
    """
    This function acts as the REDUCER. It takes the final compiled record 
    from a finished sub-graph and appends it to the MainState list.
    """
    return {
        "all_extracted_records": [state["translated_cookbook_record"]]
    }


def build_workflow():
    main = StateGraph(MainState)
    
    # Add the initial splitter
    main.add_node("splitter", splitter_node)
    
    # Add the nested sub-graph as a single node
    sub_graph_app = build_sub_graph()
    main.add_node("process_sub_study", sub_graph_app)
    
    # When the sub-graph finishes, run the reducer
    main.add_node("aggregate", aggregate_sub_studies)
    
    # 1. Start at the splitter
    main.add_edge(START, "splitter")
    
    # 2. Map-Reduce Router: Spawns parallel branches based on identified studies
    main.add_conditional_edges("splitter", route_to_sub_studies, ["process_sub_study"])
    
    # 3. Funnel finished sub-graphs into the aggregator
    main.add_edge("process_sub_study", "aggregate")
    main.add_edge("aggregate", END)
    
    return main.compile()
