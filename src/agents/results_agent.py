from config.settings import settings

from src.agents.base_agent import BaseAgent
from src.agents.schemas import ResultsSchema

from langchain_openai import ChatOpenAI


RESULTS_SYSTEM_PROMPT = """
You are an expert Scientific Results Data Auditor. Your mission is to extract final aggregated behavioral metrics, statistical variances, reliability metrics, and experimental variables from a research paper's findings, following the Codebook.

CRITICAL STATISTICAL EXTRACTION GUIDELINES:
1. **overall_p_c (Var 47)**: Total proportion of cooperative decisions made across the entire analytical pool (strictly between 0.0 and 1.0). For dichotomous choice setups. Code "N/A" if continuous game.
2. **overall_m_withdrawal (Var 48)**: Mean total resource points extracted/withdrawn by participants from a shared pool (Resource Dilemma only). Else "N/A".
3. **overall_m_cooperation (Var 49)**: Total mathematical mean contribution score observed in continuous setups. Else "N/A".
4. **overall_sd_cooperation (Var 50)**: Standard deviation associated with the game contributions or resource pool withdrawals. Code "999" if omitted.
5. **p_e_contributed (Var 51)**: Standardized proportion of endowment contributed. Formula: (Mean Contribution - choice_range_lower) / (choice_range_upper - choice_range_lower). Must be between 0.0 and 1.0. Code "N/A" if not calculable.
6. **ivs (Var 52)**: Provide a clear summary description detailing the primary Independent Variables (IVs) and manipulated design conditions.
7. **other_variables_measured (Var 53)**: List individual individual-difference indicators, psychological scales, or metrics measured (e.g., SVO, Big Five, Trust inventory); else "N/A".
8. **comments (Var 54)**: Document inconsistencies, data anomalies, strange participant drops, or questionable design deviations noted by the authors; else "N/A".
9. **n_obs (Var 60)**: Enter "N/A" for standard studies where individuals make single choices. Only provide an integer value when a unified collective group serves as the absolute singular decision unit making a single choice.

Read statistical tables, text descriptions, and footnotes with extreme care. Do not mistake pre-treatment variables or baseline stats for final game interaction metrics.
"""

class ResultsAgent(BaseAgent):
    def __init__(self):
        llm = ChatOpenAI(
            model=settings.CHAT_MODEL,
            api_key=settings.LITELLM_API_KEY,
            base_url=settings.LITELLM_BASE_URL,
            temperature=settings.TEMPERATURE
        )

        super().__init__(
            llm=llm,
            system_prompt=RESULTS_SYSTEM_PROMPT,
            output_schema=ResultsSchema,
            query_intent=(
                "results, statistical analysis, descriptive statistics, mean contribution, proportion of cooperation, "
                "standard deviation, independent variables, tables, reliability, cronbach's alpha, coefficient, observations"
            )
        )

results_node = ResultsAgent()
