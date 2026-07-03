from typing import TypedDict, Annotated, List, Dict, Any
from langchain_chroma import Chroma
import operator

class AgentState(TypedDict):
    # The path or ID of the paper being processed
    paper_id: str

    # Combined vector store tool access
    vector_store: Chroma

    # Parallel agents append their findings to this list
    extracted_features: Annotated[List[dict], operator.add]

    # The final polished output
    final_consolidated_record: Dict[str, Any]

    translated_cookbook_record: Dict[str, Any]
