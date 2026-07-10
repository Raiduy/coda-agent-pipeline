from typing import TypedDict, Annotated, List, Dict, Any
from langchain_chroma import Chroma
import operator

# class AgentState(TypedDict):
#     # The path or ID of the paper being processed
#     paper_id: str
#
#     # Combined vector store tool access
#     vector_store: Chroma
#
#     # Parallel agents append their findings to this list
#     extracted_features: Annotated[List[dict], operator.add]
#
#     # The final polished output
#     final_consolidated_record: Dict[str, Any]
#
#     translated_cookbook_record: Dict[str, Any]

class AgentState(TypedDict):
    paper_id: str
    vector_store: Chroma
    target_study_num: str       # e.g., "1a"
    target_study_desc: str      # e.g., "Prisoner's Dilemma Lab Experiment"
    extracted_features: Annotated[List[dict], operator.add]
    final_consolidated_record: Dict[str, Any]
    translated_cookbook_record: Dict[str, Any]

class MainState(TypedDict):
    paper_id: str
    vector_store: Chroma
    identified_studies: List[Dict[str, str]]
    # This collects the final dictionaries from ALL sub-studies
    all_extracted_records: Annotated[List[Dict[str, Any]], operator.add]
