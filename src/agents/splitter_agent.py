from config.settings import settings

from src.agents.base_agent import BaseAgent
from src.graph.state import MainState
from src.agents.schemas import SplitSchema

from langchain_openai import ChatOpenAI
from typing import Dict, Any



SPLITTER_PROMPT = """
You are a specialized Paper Parsing & Study Splitting Agent for a Meta-Analysis on social dilemmas. 
Your exact task is to analyze the methodology and experimental design of the provided text to determine how many distinct studies and sub-studies exist, strictly following the Codebook splitting rules.

CRITICAL SPLITTING RULES:
You must output a list of studies using the numbering format 1, 2, 3, etc. 
However, you MUST split a single study into a parent row (e.g., "1") and sub-study rows (e.g., "1a", "1b") IF ANY of the following conditions are met:

1. DIFFERENT GAMES: If a study measures Dependent Variables (DVs) in different types of games (e.g., Prisoner's Dilemma vs. Public Goods Dilemma) OR different formats of the same game (e.g., Continuous PGD vs. Step-level PGD), split them.
   - Output "1" (Description: Overall sample characteristics)
   - Output "1a" (Description: First game type, e.g., Continuous PGD)
   - Output "1b" (Description: Second game type, e.g., Step-level PGD)
   - *Note: This split applies whether the game manipulation is between-subjects OR within-subjects.*

2. DIFFERENT COUNTRIES OR LABS: If a study involves measures in different countries or different labs (e.g., multi-lab replication projects), split them.
   - Output "1" (Description: Overall sample characteristics)
   - Output "1a" (Description: Country/Lab 1)
   - Output "1b" (Description: Country/Lab 2)

3. DIFFERENT CHOICE RANGES (BETWEEN-SUBJECTS ONLY): If the study manipulates the 'choice range lower', 'choice range upper', or the 'number of choice options' in a BETWEEN-SUBJECTS setting, split them.
   - Output "1" (Description: Overall sample characteristics)
   - Output "1a" (Description: Choice range setting 1)
   - Output "1b" (Description: Choice range setting 2)
   - *EXCEPTION: DO NOT split into sub-studies if choice ranges are manipulated within-subjects (i.e., the same participants play multiple ranges). If it is within-subjects, do not create 1a/1b for this condition.*

OUTPUT FORMAT EXPECTATIONS:
- For every identified item, provide the `study_num` (e.g., "1", "1a", "2") and a brief 3-6 word `description`.
- If a study requires splitting based on the rules above, ALWAYS include the parent study first (e.g., "1") before listing its sub-studies ("1a", "1b").
- If none of the splitting conditions are met, simply return standard integers (e.g., "1", "2") for the studies presented in the paper.
- Base your numbering purely on the experimental design presented. Do not confuse literature review examples with actual conducted experiments.
"""


class SplitterAgent(BaseAgent):
    def __init__(self):
        llm = ChatOpenAI(
                model=settings.CHAT_MODEL, 
                api_key=settings.LITELLM_API_KEY,
                base_url=settings.LITELLM_BASE_URL,
                temperature=0.2)

        super().__init__(
            llm=llm,
            system_prompt=SPLITTER_PROMPT,
            output_schema=SplitSchema,
            query_intent="overview of studies, methodology, experiment 1, study 2, experimental design, general discussion overview"
        )

    def __call__(self, state: MainState) -> Dict[str, Any]:
        """
        OVERRIDE: We override the BaseAgent's __call__ here because this agent 
        outputs 'identified_studies' to the MainState for graph routing, 
        rather than appending to 'extracted_features'.
        """
        print("🔍 [StudySplitterAgent] Scanning paper context for distinct sub-studies...")

        vector_store = state.get("vector_store")

        if vector_store is not None:
            # Retrieve the most relevant chunks using the inherited query intent
            retriever = vector_store.as_retriever(search_kwargs={"k": 10})
            retrieved_docs = retriever.invoke(self.query_intent)
            paper_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        else:
            print('\n*******ERROR, NO CONTEXT AVAILABLE********')
            paper_context = state.get("paper_context", "No context provided.")

        # Invoke the LLM chain (inherited from BaseAgent)
        extracted_data = self.runnable.invoke({"context": paper_context})

        # Format the Pydantic output into the dictionary expected by MasterState
        studies = [
            {"study_num": s.study_num, "description": s.description} 
            for s in extracted_data.studies
        ]

        print(f"✅ Found {len(studies)} sub-studies: {[s['study_num'] for s in studies]}")

        # Return to MasterState so workflow.py can Map-Reduce (Spawn sub-graphs)
        return {
            "identified_studies": studies
        }

# Instantiate the node function to be imported directly by your LangGraph workflow
splitter_node = SplitterAgent()
