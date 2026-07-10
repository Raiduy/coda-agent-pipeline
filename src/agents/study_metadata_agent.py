from config.settings import settings

from src.agents.base_agent import BaseAgent
from src.agents.schemas import StudyMetadataSchema

from langchain_openai import ChatOpenAI

STUDY_METADATA_PROMPT = """
You are a specialized Meta-Analysis Data Extraction Agent. Your task is to extract administrative and publication metadata from the provided academic paper text or context, strictly following the Cooperation Database Codebook guidelines.

CRITICAL INSTRUCTIONS FOR CODING FIELDS:
1. **authors_and_year (Variable 2)**: Extract all author names and the publication year. You may extrapolate or infer the publicatioon year of the study. Format exactly as: LastNameA, FirstNameA; LastNameB, FirstNameB; LastNameC, FirstNameC; (Year).
2. **title (Variable 3)**: Extract the full title of the paper exactly as it appears.
3. **published_status (Variable 6)**: Code strictly as an integer:
   - 1 = Published peer-reviewed journal article
   - 2 = Raw data / unpublished dataset
   - 3 = Doctoral Dissertation
   - 4 = Working paper
   - 5 = Master's thesis

Strictly output values matching the defined schema types. If any textual information is missing or not mentioned, default to "999" or "N/A" as directed by the field descriptions.
"""
# 4. **study_num (Variable 4)**: Code as 1, 1a, 1b, 2, 3, etc. 
#    - *CRITICAL SPLIT RULE*: If a single study involves dependent variable (DV) measures across different games (e.g., Prisoner's Dilemma vs. Public Goods Game), different countries, or different choice ranges in a between-subject setting, split them! Code them as 1a, 1b, etc., in separate rows. 
# 5. **overlaps_with (Variable 5)**: If the paper explicitly states that the data overlaps with another paper/dataset, code the DOI or paper_ID/study_ID. If it does not overlap, code as "N/A". If it is completely unmentioned or unclear, code "999".
#
# """
# You are an expert scientific data extractor. Your job is to analyze the research paper and extract its high-level metadata matching the requested schema. 
#
# Focus heavily on the first few pages, headers, footers, and acknowledgments to find this information.
#
# Strictly adhere to the following extraction rules:
# 1. AUTHORS AND YEAR: Extract all author names and the publication year. You may extrapolate or infer the publicatioon year of the study. Format exactly as: LastNameA, FirstNameA; LastNameB, FirstNameB; LastNameC, FirstNameC; (Year).
# 2. TITLE: Extract the full, official title of the research paper.
# 4. PUBLISHED STATUS: Classify the document type strictly using one of these integers:
#    - Use 1 if it is published in a peer-reviewed journal or conference proceedings.
#    - Use 2 if it represents raw, unformatted data or a pre-print repository snapshot.
#    - Use 3 if it is explicitly a Doctoral Dissertation / PhD Thesis.
#    - Use 4 if it is listed as a working paper, white paper, or report.
#    - Use 5 if it is a Master's Thesis.
#
# Do not guess or extrapolate. If a field cannot be found, use 'N/A' for strings or default to the closest matching classification for integers based on the document layout.
# """
# 3. STUDY NUMBER: If this paper is part of a larger clinical trial, systematic registry, grant series, or sequential project, extract the trial/study ID or registered number (e.g., NCT01234567, Grant #98765). If no specific study number or trial ID is mentioned, return "N/A".

class StudyMetadataAgent(BaseAgent):
    def __init__(self):
        llm = ChatOpenAI(
            model=settings.CHAT_MODEL,
            api_key=settings.LITELLM_API_KEY,
            base_url=settings.LITELLM_BASE_URL,
            temperature=settings.TEMPERATURE
        )

        super().__init__(
            llm=llm,
            system_prompt=STUDY_METADATA_PROMPT,
            output_schema=StudyMetadataSchema,
            query_intent="paper title, author names, publication year, journal details, abstract, sub-study numbering"
        )

# Instantiate the node function to be imported directly by your LangGraph workflow
study_metadata_node = StudyMetadataAgent()
