from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    # The path or ID of the paper being processed
    paper_id: str

    # Combined vector store tool access
    vector_store_id: str

    # Parallel agents append their findings to this list
    extracted_features: Annotated[List[dict], operator.add]

    # The final polished output
    final_report: dict

