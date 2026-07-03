from config.settings import settings

from src.agents.base_agent import BaseAgent
from src.agents.schemas import SampleDemographicsSchema

from langchain_openai import ChatOpenAI


SAMPLE_DEMOGRAPHICS_PROMPT = """
You are a specialized Meta-Analysis Demographics Extraction Agent. Your task is to extract sample demographics and data collection contexts from an academic paper, strictly following the Cooperation Database Codebook guidelines.

CRITICAL INSTRUCTIONS FOR CODING FIELDS:
1. **data_collection_year (Variable 7)**: Extract the calendar year when the experimental data was collected. 
   - *HEURISTIC FALLBACK*: If not specified, estimate from the paper's lifecycle tracking metadata in this priority order: year when first accessible as a working paper, presented at a conference, received/submitted, accepted, available online, or published. Code 999 if absolutely missing.
2. **source_of_year (Variable 8)**: Integer classification based on how you found Variable 7:
   - 1=Conducted, 2=Presented, 3=Working paper published, 4=Received/Submitted, 5=Published, 6=Accepted, 7=Available online. Code "999" if completely unknown.
3. **country (Variable 9)**: Output *only* the 3-letter country code following the ISO 3166-1 alpha-3 standard (e.g., USA, DEU, CHN, NLD, GBR). 
4. **source_of_country (Variable 10)**: Integer classification:
   - 1 = Specified country (paper explicitly names the lab, city, or country pool)
   - 2 = Multiple countries (most from Country X, but a smaller percentage elsewhere)
   - 3 = All authors (country not specified, but all author institutional affiliations match Country X)
   - 4 = Most authors (majority of author affiliations match Country X)
5. **sample_size (Variable 11)**: Total sample size (N) in a single study *AFTER* exclusion of participants. 
   - *CRITICAL SPLIT RULE*: Do not stop at the first N you see. Look carefully for participant attrition/exclusion. If a single study is split into two rows because participants were randomly assigned to two different games, divide N by two.
6. **prop_male (Variable 12)**: Proportion of male participants expressed as a float from 0.0 to 1.0. Code "999" if missing.
7. **m_age (Variable 13)**: Participants' mean age in years (float or int). Code "999" if missing.
8. **age_range_lower & age_range_upper (Variables 14 & 15)**: The absolute minimum and maximum ages in the sample. Code "999" if missing.
9. **students (Variable 16)**: Code as 1 if the sample was primarily or completely undergraduate/graduate students; 0 if a general public, MTurk, or field sample.
10. **discipline (Variable 17)**: Specific student discipline: 1=Economics, 2=Psychology, 3=Sociology, 4=Mixed, 5=Other (e.g., MBA). 
    - *RULE*: Code "N/A" for non-student samples. Code "999" if student sample but discipline is unmentioned.
11. **recr_meth (Variable 18)**: Recruitment mechanism code:
    - 1=Participant pool (or university recruitment without specification), 2=Mturk, 3=Advertisement, 4=Other (e.g., email invitations), 5=ORSEE, 6=Prolific.
12. **if_other_recr_meth (Variable 19)**: If Variable 18 was coded as 4, type the exact text detail here; otherwise code "N/A".

Always verify data types. When a numeric property is missing, provide "999" or "N/A" wrapped in strings as supported by the schema's Union types.
"""

# SAMPLE_DEMOGRAPHICS_PROMPT = """
# You are an expert scientific data auditor. Your mission is to extract granular metadata regarding how, when, and where the research data was collected. 
#
# Academic papers are often vague about these details; you must be highly analytical and strictly follow these hierarchical fallback logic tracks:
#
# 1. DATA COLLECTION YEAR & SOURCE OF YEAR:
#    - Look for the explicit year the data collection/experiment was conducted. If found, use that year and set `source_of_year` to 1.
#    - If NOT specified, estimate the year by hunting down the earliest record of the paper's lifecycle in this exact order:
#      * Year it was presented -> `source_of_year` = 2
#      * Year it was published as a working paper -> `source_of_year` = 3
#      * Year it was received/submitted -> `source_of_year` = 4
#      * Year it was accepted -> `source_of_year` = 6
#      * Year it was available online after acceptance -> `source_of_year` = 7
#      * Year it was officially published -> `source_of_year` = 5
#    - Extract the year as a clean 4-digit integer.
#
# 2. COUNTRY & SOURCE OF COUNTRY:
#    - Identify the primary location where participants were tested or data was sampled.
#    - Map the country string to its standard 3-letter ISO 3166-1 alpha-3 code (e.g., United States -> USA, Germany -> DEU, United Kingdom -> GBR).
#    - Determine `source_of_country` using these strict classifications:
#      * Use 1 (Specified country) if the text explicitly states the data location (e.g., "conducted at University of X", "sampled from Y lab").
#      * Use 2 (Multiple countries) if it mentions a blend of international participants but specifies a primary majority country.
#      * Use 3 (All authors) if the location is never specified, but ALL authors share affiliations in that country (including single-author papers).
#      * Use 4 (Most authors) if the location is never specified, but the majority of authors share affiliations in that country.
#
# 3. SAMPLE SIZE:
#    - Isolate the FINAL total sample size used in the actual statistical analyses *after* all participant exclusions (attrition, failed attention checks, incomplete data).
#    - If a single study split its participants evenly across two different games/conditions, divide the total sample size by 2.
#    - Guardrail: Do not simply pull the first "N=" you encounter in the text. Read the "Participants" or "Results" section to verify if any subjects were dropped before calculation.
#
# Be incredibly meticulous. Do not make up information. If a field cannot be computed via the rules above, output a sensible default or fail gracefully.
# """


class SampleDemographicsAgent(BaseAgent):
    def __init__(self):
        llm = ChatOpenAI(
                model=settings.CHAT_MODEL, 
                api_key=settings.LITELLM_API_KEY,
                base_url=settings.LITELLM_BASE_URL,
                temperature=0.2)

        super().__init__(
            llm=llm,
            system_prompt=SAMPLE_DEMOGRAPHICS_PROMPT,
            output_schema=SampleDemographicsSchema,
            query_intent="participants, subjects, sample size, age range, gender distribution, university student sample, recruitment methods, attrition, excluded data"
        )

# Instantiate the node function to be imported directly by your LangGraph workflow
sample_demographics_node = SampleDemographicsAgent()
