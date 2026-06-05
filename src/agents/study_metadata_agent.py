from config.settings import settings

from src.agents.base_agent import BaseAgent
from src.agents.schemas import StudyMetadataSchema

from langchain_openai import ChatOpenAI

STUDY_METADATA_PROMPT = """
You are an expert scientific data extractor. Your job is to analyze the research paper and extract its high-level metadata matching the requested schema. 

Focus heavily on the first few pages, headers, footers, and acknowledgments to find this information.

Strictly adhere to the following extraction rules:
1. AUTHORS AND YEAR: Extract all author names and the publication year. You may extrapolate or infer the publicatioon year of the study. Format exactly as: LastNameA, FirstNameA; LastNameB, FirstNameB; LastNameC, FirstNameC; (Year).
2. TITLE: Extract the full, official title of the research paper.
4. PUBLISHED STATUS: Classify the document type strictly using one of these integers:
   - Use 1 if it is published in a peer-reviewed journal or conference proceedings.
   - Use 2 if it represents raw, unformatted data or a pre-print repository snapshot.
   - Use 3 if it is explicitly a Doctoral Dissertation / PhD Thesis.
   - Use 4 if it is listed as a working paper, white paper, or report.
   - Use 5 if it is a Master's Thesis.

Do not guess or extrapolate. If a field cannot be found, use 'N/A' for strings or default to the closest matching classification for integers based on the document layout.
"""
# 3. STUDY NUMBER: If this paper is part of a larger clinical trial, systematic registry, grant series, or sequential project, extract the trial/study ID or registered number (e.g., NCT01234567, Grant #98765). If no specific study number or trial ID is mentioned, return "N/A".

class StudyMetadataAgent(BaseAgent):
    def __init__(self):
        llm = ChatOpenAI(
                model=settings.CHAT_MODEL, 
                api_key=settings.LITELLM_API_KEY,
                base_url=settings.LITELLM_BASE_URL,
                temperature=0)

        super().__init__(
            llm=llm,
            system_prompt=STUDY_METADATA_PROMPT,
            output_schema=StudyMetadataSchema
        )

# Instantiate the node function to be imported directly by your LangGraph workflow
study_metadata_node = StudyMetadataAgent()
