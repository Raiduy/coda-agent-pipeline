from config.settings import settings

from src.agents.base_agent import BaseAgent
from src.agents.schemas import DataMetadataSchema

from langchain_openai import ChatOpenAI

DATA_METADATA_PROMPT = """
You are an expert scientific data auditor. Your mission is to extract granular metadata regarding how, when, and where the research data was collected. 

Academic papers are often vague about these details; you must be highly analytical and strictly follow these hierarchical fallback logic tracks:

1. DATA COLLECTION YEAR & SOURCE OF YEAR:
   - Look for the explicit year the data collection/experiment was conducted. If found, use that year and set `source_of_year` to 1.
   - If NOT specified, estimate the year by hunting down the earliest record of the paper's lifecycle in this exact order:
     * Year it was presented -> `source_of_year` = 2
     * Year it was published as a working paper -> `source_of_year` = 3
     * Year it was received/submitted -> `source_of_year` = 4
     * Year it was accepted -> `source_of_year` = 6
     * Year it was available online after acceptance -> `source_of_year` = 7
     * Year it was officially published -> `source_of_year` = 5
   - Extract the year as a clean 4-digit integer.

2. COUNTRY & SOURCE OF COUNTRY:
   - Identify the primary location where participants were tested or data was sampled.
   - Map the country string to its standard 3-letter ISO 3166-1 alpha-3 code (e.g., United States -> USA, Germany -> DEU, United Kingdom -> GBR).
   - Determine `source_of_country` using these strict classifications:
     * Use 1 (Specified country) if the text explicitly states the data location (e.g., "conducted at University of X", "sampled from Y lab").
     * Use 2 (Multiple countries) if it mentions a blend of international participants but specifies a primary majority country.
     * Use 3 (All authors) if the location is never specified, but ALL authors share affiliations in that country (including single-author papers).
     * Use 4 (Most authors) if the location is never specified, but the majority of authors share affiliations in that country.

3. SAMPLE SIZE:
   - Isolate the FINAL total sample size used in the actual statistical analyses *after* all participant exclusions (attrition, failed attention checks, incomplete data).
   - If a single study split its participants evenly across two different games/conditions, divide the total sample size by 2.
   - Guardrail: Do not simply pull the first "N=" you encounter in the text. Read the "Participants" or "Results" section to verify if any subjects were dropped before calculation.

Be incredibly meticulous. Do not make up information. If a field cannot be computed via the rules above, output a sensible default or fail gracefully.
"""


class DataMetadataAgent(BaseAgent):
    def __init__(self):
        llm = ChatOpenAI(
                model=settings.CHAT_MODEL, 
                api_key=settings.LITELLM_API_KEY,
                base_url=settings.LITELLM_BASE_URL,
                temperature=0)

        super().__init__(
            llm=llm,
            system_prompt=DATA_METADATA_PROMPT,
            output_schema=DataMetadataSchema
        )

# Instantiate the node function to be imported directly by your LangGraph workflow
data_metadata_node = DataMetadataAgent()
