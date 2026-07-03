from config.settings import settings

from src.agents.base_agent import BaseAgent
from src.agents.schemas import GameParametersSchema

from langchain_openai import ChatOpenAI


GAME_PARAMETERS_SYSTEM_PROMPT = """
You are a specialized Meta-Analysis Game Parameters Agent. Your mission is to extract or calculate strict mathematical payoff values and indices from an experimental game description, following the Cooperation Database Codebook.

CRITICAL MATHEMATICAL MATRIX RULES:
1. **if_pd_k_index (Variable 34)**: Applies *only* to symmetric Prisoner's Dilemmas. 
   - Formula: K = (R - P) / (T - S)
   - T = Temptation to defect (Payoff for Defecting when partner Cooperates)
   - R = Reward for mutual cooperation (Payoff for both Cooperating)
   - P = Punishment for mutual defection (Payoff for both Defecting)
   - S = Sucker's payoff (Payoff for Cooperating when partner Defects)
   - Ensure the calculated float index falls strictly between 0 and 1. Code "N/A" if the game is not a symmetric PD.
2. **if_pgd_mpcr (Variable 35)**: Applies *only* to continuous Public Goods Dilemmas.
   - Formula: MPCR = Marginal Per Capita Return = (Total Marginal Efficiency Multiplier / Group Size).
   - Example: If a public pool multiplies contributions by 2, and group size is 4, MPCR = 2 / 4 = 0.50. 
   - Must be a float between 0 and 1. Code "N/A" if not a continuous PGD.
3. **if_step_level_provision_point (Variable 36)**: Applies *only* to step-level Public Goods Dilemmas.
   - Extract the specified provision point threshold required for the group to unlock the public good. Code "N/A" if not step-level.
4. **if_rd_replenishment_rate (Variable 37)**: Applies *only* to Resource Dilemmas.
   - Extract the renewal or replenishment pool multiplier factor (must be >= 1.0). Code "N/A" if not a resource dilemma.

If parameters are not applicable to the current game structure, strictly fill with "N/A". If the target game type matches but values are completely omitted or unmentioned in the text, code "999".
"""

class GameParametersAgent(BaseAgent):
    def __init__(self):
        llm = ChatOpenAI(
                model=settings.CHAT_MODEL, 
                api_key=settings.LITELLM_API_KEY,
                base_url=settings.LITELLM_BASE_URL,
                temperature=0.2)
        super().__init__(
            llm=llm,
            system_prompt=GAME_PARAMETERS_SYSTEM_PROMPT,
            output_schema=GameParametersSchema,
            query_intent=(
                "payoff matrix, payoffs, temptation T, reward R, punishment P, sucker S, multiplier, "
                "marginal per capita return, MPCR, provision point, threshold, replenishment rate, renewal rate"
            )
        )

game_parameters_node = GameParametersAgent()
