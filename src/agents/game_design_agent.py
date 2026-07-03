from langchain_openai import ChatOpenAI
from src.agents.base_agent import BaseAgent
from src.agents.schemas import GameDesignSchema
from config.settings import settings

GAME_DESIGN_SYSTEM_PROMPT = """
You are a specialized Meta-Analysis Game Design Extraction Agent. Your task is to extract experimental parameters and structural environment details of a social dilemma game from the provided paper context, following the Meta-Analysis Codebook rules.

CRITICAL FIELD ENCODING GUIDELINES:
1. **exp_setting (Var 20)**: 1=Online, 2=Lab, 3=Class, 4=Field, 5=Lab in the field, 6=Natural, 7=Other.
2. **dilemma_type (Var 21)**: 1=Prisoner's Dilemma (PD/nPD), 2=Public Goods Dilemma (PGD), 3=Resource Dilemma (RD), 4=Other. 
3. **if_other_dilemma_type (Var 22)**: Detail name if Var 21=4; else "N/A".
4. **if_pgd_continuous_step (Var 23)**: If PGD: 1=Continuous (any amount up to endowment), 2=Step-level (provision point threshold). Else "N/A".
5. **symmetry (Var 24)**: 1=Yes (identical endowments/payoffs for all players), 0=No.
6. **one_shot (Var 25)**: 1=Yes (played with same player exactly once), 0=No.
7. **matching (Var 26)**: 1=Stranger, 2=Partner (ID unknown), 3=Partner (random ID), 4=Partner (static ID). 
8. **if_one_shot_repeated (Var 27)**: 1=Yes (paired with different partner after each trial across multiple trials); 0=No.
9. **iterated_num_per_block & block_num (Var 28 & 29)**: Numerical round count inside a block, and total session blocks. Default missing to 999; default non-applicable to "N/A".
10. **end_game_effect (Var 30)**: 1=Yes (subjects explicitly know total rounds in advance), 0=No.
11. **payment_show_up & payment_game (Var 31 & 32)**:
    - Show up: 0=None, 1=Paid cash/money, 2=Course credit, 3=Non-monetary.
    - Game: 0=Hypothetical, 1=Paid cash, 2=Monetary lottery, 3=Non-monetary token, 4=Non-monetary lottery.
12. **group_size (Var 33)**: Active decision group size. If manipulated within-subject or varying, format strictly with square brackets, e.g., "[3,7]".
13. **discussion (Var 38)**: 0=No communication, 1=Yes (two-way), 2=Yes (one-way presentation/message).
14. **simultaneous (Var 39)**: 1=Simultaneous actions, 2=Sequential / sequential move choices.
15. **choice_range_lower & choice_range_upper (Var 40 & 41)**: Quantifiable bounds of play (e.g., lower=0, upper=endowment value).
16. **num_choice_options (Var 42)**: Integer count of legal strategies (2 for dichotomous/binary game; upper+1 for discrete integer continuous choices).
17. **feedback (Var 43)**: 0=None, 1=Individual action history, 2=Group aggregate total choices.
18. **deception (Var 44)**: 1=Yes (false teammate feedback or computer bot disguised as human), 0=No.
19. **real_part (Var 45)**: 0=Imagined/computer interaction, 1=Yes (real humans, no deception), 2=Yes (real humans, with deception).
20. **periods (Var 46)**: 1=All rounds analyzed, 2=First round only, 3=Last round only, 4=First & Last only, 5=Others.
21. **sanction (Var 58)**: Punishment/Reward active: 0=No, 1=Yes. If manipulated within-subjects, format with a semicolon: "0 ; 1".
22. **acquaintance (Var 59)**: 0=No (strangers), 1=Yes (friends/classmates), 2=Small bound community.

If information is absent or not mentioned in the text context, output '999' or 'N/A' matching the Pydantic field typing description. Do not extrapolate outside the context text.
"""

class GameDesignAgent(BaseAgent):
    def __init__(self):
        llm = ChatOpenAI(
            model=settings.CHAT_MODEL,
            api_key=settings.LITELLM_API_KEY,
            base_url=settings.LITELLM_BASE_URL,
            temperature=0.2
        )
        super().__init__(
            llm=llm,
            system_prompt=GAME_DESIGN_SYSTEM_PROMPT,
            output_schema=GameDesignSchema,
            query_intent=(
                "methodology, experimental design, game setup, prisoner's dilemma, public goods game, "
                "resource dilemma, rounds, trials, group size, feedback, communication, payment, "
                "endowment, choice range, matching rule, stranger partner, deception, punishment reward"
            )
        )

game_design_node = GameDesignAgent()
