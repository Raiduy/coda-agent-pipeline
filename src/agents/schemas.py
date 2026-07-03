from pydantic import BaseModel, Field
from typing import Union

# CODEBOOK Fields 2 -> 4, 6
class StudyMetadataSchema(BaseModel):
    # authors_and_year: str = Field(description="The names of the authors and the publication year in parenthesis. Example: Author A, Author B, Author C (YYY)")
    # title: str = Field(description="The title of the research paper.")
    # study_number: str = Field(description="")
    # # overlaps_with: str = Field(description="In case the data from one study overlaps with the data from another study, mention here (code doi if available; otherwise code paper_ID/study_ID) ")
    # published_status: int = Field(description="1=Published, 2=Raw data, 3=Doctoral Dissertation, 4=Working paper, 5=Master’s thesis")

    authors_and_year: str = Field(description="Variable 2: Author surnames and publication year in parentheses, e.g., Smith (2020).")
    title: str = Field(description="Variable 3: Title of the paper.")
    # study_num: str = Field(description="Variable 4: Code as 1, 1a, 1b, 2, 3, etc. based on substudies/games/countries.")
    # overlaps_with: Union[str, int] = Field(description="Variable 5: doi or paper_ID/study_ID if data overlaps with another study; else 'N/A' or 999.")
    published_status: int = Field(description="Variable 6: 1=Published, 2=Raw data, 3=Doctoral Dissertation, 4=Working paper, 5=Master's thesis.")



# CODEBOOK Fields 7 -> 19
class SampleDemographicsSchema(BaseModel):
    # data_collection_year: int = Field(description="Year when the data was collected. If not specified, get as precise estimation of the year of data collection as possible. In case of not specified: extract the year from sources in the order of when the paper was accessible as working paper, presented, received/ submitted, accepted, available online after acceptance, published.")
    # source_of_year: int = Field(description="Source of the year when the data was collected 1=Conducted, 2=Presented, 3=Working paper published, 4=Received/Submitted, 5=Published, 6=Accepted, 7=Available online")
    # country: str = Field(description="Country where the data collection took place coded with the 3-letter country code following ISO 3166-1 alpha-3")
    # source_of_country: int = Field(description="Source of the country where the data collection took place. 1=Specified country, 2=Multiple countries, 3=All authors, 4=Most authors. \n(1)  Specified country: The paper explicitly states that data have been collected at a certain location (e.g., University of X, Y lab, using Z participants pool); \n(2) Multiple countries: The paper specifies that most participants come from Country X (that should be indicated under Country), but that a smaller percentage comes from different countries (indicate the percentages and nationalities in a note, if the information is available); \n(3) All authors: The paper does not specify the country, but all authors are affiliated to the same institution in Country X (that should be indicated under Country) (indicate it for single-authored papers), \n(4) Most authors: The majority of the authors are affiliated to the same institution in Country X.")
    # sample_size: int = Field(description="Total sample size in a single study after exclusion of participants. If a single study is coded as two because participants were randomly assigned to two different games, this sample size should be divided by two. Please don’t stop at the first N you see in the text, but be very careful in detecting excluded participants in the study/analyses. Write a note to indicate initial N and reason for exclusion.")
    # prop_male: float = Field(description="Proportion of male participants in the whole sample of a study after exclusion of participants, if possible. If authors do not update this information, code it for initial sample size and write “Information based upon initial sample size” in a note.")
    # mean_age: float = Field(description="Participants’ mean age in years after exclusion of participants, if possible. If authors do not update this information, code it for initial sample size and write “Information based upon initial sample size” in a note")
    # age_range_lower: int = Field(description="Minimum age of all sampled participants")
    # age_range_higher: int = Field(description="Maximum age of all sampled participants")
    # students: int = Field(description="Whether participants were student samples: 0=No, 1=Yes")
    # discipline: int = Field(description="Specific discipline the students are from 1=Economics, 2=Psychology, 3=Sociology, 4=Mixed, 5=Other.\nCode N/A only for non-students samples, otherwise 999 if not mentioned; code as 5 for students from another single discipline (e.g., MBA students)")
    # recr_meth: int = Field(description="The way participants were recruited 1 = Participant pool, 2 =  Mturk, 3 = Advertisement, 4 = Other, 5 = ORSEE, 6 =  Prolific.")
    # other_recr: str = Field(description="If participants were recruited in other ways, specify here.")

    data_collection_year: int = Field(description="Variable 7: Year when data was collected. If not specified, estimate from lifecycle order: presented, working paper, submitted, accepted, online, published. Code 999 if missing.")
    source_of_year: Union[int, str] = Field(description="Variable 8: Source of the collection year. 1=Conducted, 2=Presented, 3=Working paper published, 4=Received/Submitted, 5=Published, 6=Accepted, 7=Available online. Code 999 if missing.")
    country: str = Field(description="Variable 9: 3-letter country code following ISO 3166-1 alpha-3 where data collection took place.")
    source_of_country: Union[int, str] = Field(description="Variable 10: Source classification: 1=Specified country, 2=Multiple countries, 3=All authors, 4=Most authors.")
    sample_size: int = Field(description="Variable 11: Total sample size (N) in a single study after exclusion of participants. Divide by 2 if split evenly across two games.")
    prop_male: Union[float, str] = Field(description="Variable 12: Proportion of male participants in the whole sample (0.0 to 1.0). Code 999 if missing.")
    m_age: Union[float, str] = Field(description="Variable 13: Participants' mean age in years. Code 999 if missing.")
    age_range_lower: Union[int, str] = Field(description="Variable 14: Minimum age of all sampled participants. Code 999 if missing.")
    age_range_upper: Union[int, str] = Field(description="Variable 15: Maximum age of all sampled participants. Code 999 if missing.")
    students: Union[int, str] = Field(description="Variable 16: Whether participants were student samples: 0=No, 1=Yes.")
    discipline: Union[int, str] = Field(description="Variable 17: Discipline of student samples: 1=Economics, 2=Psychology, 3=Sociology, 4=Mixed, 5=Other. Code 'N/A' for non-students; 999 if not mentioned.")
    recr_meth: Union[int, str] = Field(description="Variable 18: Recruitment method: 1=Participant pool, 2=Mturk, 3=Advertisement, 4=Other, 5=ORSEE, 6=Prolific.")
    if_other_recr_meth: str = Field(description="Variable 19: If recruitment method is 4 (Other), specify here; otherwise 'N/A'.")

# CODEBOOK Fields 20 -> 33, 38 -> 46, 58, 59
class GameDesignSchema(BaseModel):
    # exp_setting: int = Field(description="The setting in which the experiment was conducted: (a) Online (e.g., MTurk, Prolific); (b) Lab: laboratory experiment not at a field site; (c) Classroom: experiment conducted during a regular class (e.g., does not apply if classroom is used as a lab room); (d) Field: field experiment that involves a manipulation carried out in the field. Subjects may or may not be aware that they are part of an experiment (e.g., Nikos Nikiforakis’ work on punishment in the field); (e) Lab in the field: A lab experiment carried out at a field site. Work by anthropologists often falls into this category (e.g., Joe Henrich and colleagues’ work in small-scale societies), but this also takes place in Western countries (e.g., John List's experiments at a sport trading card fair). The lab is brought to the participants rather than the other way around; (f) Natural experiment: A quasi-experiment in the field in which randomization is not controlled by the experimenter (e.g., John List’s study on the TV show ‘Friend or Foe’ that has the structure of a prisoner’s dilemma. 1 = Online, 2 = Lab, 3 = Class, 4 = Field, 5 = Lab in the field, 6 = Natural experiment, 7 = Other")
    # dilemma_type: str = Field(description="The social dilemma paradigms used to measure cooperation (Code as 1 for both dichotomous-choice and continuous prisoner’s dilemma, e.g., a give-some dilemma falls into this category) 1 = (n)PD (prisoner’s dilemma), 2 = PGD (public goods dilemma), 3 = RD (resource dilemma), 4 = Other")
    # if_other_dilemma_type: str = Field(description="Description of the type of game if it belongs to “Other” dilemma type")
    # pgd_level: int = Field(description="1= Continuous, 2 = Step-level\n(a) Continuous PGD: Total contribution to the group account is multiplied by a factor and equally divided among all group members, regardless of the amount of contribution; (b) Step-level PGD: the public good is provided only if a minimum threshold of contributions (i.e., provision point) is met")
    # symmetry: int = Field(description="0 = No, 1 = Yes\nWhether participants played the game with the same person only once (this also applies if participants switch partners after each trial)")
    # one_shot: int = Field(description="Whether played with same person only once: 0=No, 1=Yes")
    # matching: int = Field(description="1 = Stranger (one-shot or one-shot repeated), 2 = Partner, ID not specified, 3 = Partner, random ID, 4 = Partner, static ID\nThe way participants are paired with others during interactions:\n(a) stranger matching: participants interact with one person for one trial (i.e., one-shot), or switch partners after each trial across many trials (i.e., one-shot repeated);\n(b) partner matching: if the paper did not specify whether participants are assigned an ID during the experiment, code as 2; if participants play with the same partners, but their IDs change after each trial, code as 3; if participants play with the same partners, and each person has the same ID across the experiment, code as 4.")
    # if_one_shot_repeated: int = Field(description="0 = No, 1 = Yes\nWhether participants are paired with different partner(s) after each trial across many trials (code as 1) within a block")
    # iterated_num_per_block: int = Field(description="The number of trials (rounds) in each block.")


    exp_setting: Union[int, str] = Field(description="Variable 20: 1=Online, 2=Lab, 3=Class, 4=Field, 5=Lab in the field, 6=Natural experiment, 7=Other.")
    dilemma_type: Union[int, str] = Field(description="Variable 21: 1=(n)PD, 2=PGD, 3=RD, 4=Other.")
    if_other_dilemma_type: str = Field(description="Variable 22: Specify if dilemma type is 4 (Other); otherwise 'N/A'.")
    if_pgd_continuous_step: Union[int, str] = Field(description="Variable 23: If PGD: 1=Continuous, 2=Step-level. Code 'N/A' if not a PGD.")
    symmetry: Union[int, str] = Field(description="Variable 24: Payoff/endowment matrix symmetry: 0=No, 1=Yes.")
    one_shot: Union[int, str] = Field(description="Variable 25: Whether played with same person only once: 0=No, 1=Yes.")
    matching: Union[int, str] = Field(description="Variable 26: 1=Stranger (one-shot/repeated), 2=Partner (ID unknown), 3=Partner (random ID), 4=Partner (static ID).")
    if_one_shot_repeated: Union[int, str] = Field(description="Variable 27: Paired with different partner after each trial across many trials: 0=No, 1=Yes.")
    iterated_num_per_block: Union[int, str] = Field(description="Variable 28: Number of trials/rounds in each block. Code 'N/A' or 999 if applicable.")
    block_num: Union[int, str] = Field(description="Variable 29: Total number of blocks across full session. Code 999 if missing.")
    end_game_effect: Union[int, str] = Field(description="Variable 30: Do subjects know real total game trials prior to experiment? 0=No, 1=Yes.")
    payment_show_up: Union[int, str] = Field(description="Variable 31: Show up compensation: 0=None, 1=Paid, 2=Course credit, 3=Non-monetary.")
    payment_game: Union[int, str] = Field(description="Variable 32: Decision payoffs form: 0=Hypothetical, 1=Paid money, 2=Monetary lottery, 3=Non-monetary, 4=Non-monetary lottery.")
    group_size: str = Field(description="Variable 33: Number of people affected by choices. If fluctuating/manipulated, use square brackets, e.g., '[3,7]'.")
    discussion: Union[int, str] = Field(description="Variable 38: Discussion before/during: 0=No, 1=Yes (two-way), 2=Yes (one-way).")
    simultaneous: Union[int, str] = Field(description="Variable 39: Decisions: 1=Simultaneous, 2=Sequential.")
    choice_range_lower: Union[float, str] = Field(description="Variable 40: Minimum allowed contribution/choice (often 0 or m).")
    choice_range_upper: Union[float, str] = Field(description="Variable 41: Maximum allowed contribution/endowment n (or 1 for dichotomous).")
    num_choice_options: Union[int, str] = Field(description="Variable 42: Number of choices: 2 for dichotomous, (n+1) or (n-m+1) for continuous.")
    feedback: Union[int, str] = Field(description="Variable 43: Feedback after round: 0=No feedback, 1=Individual feedback, 2=Group feedback.")
    deception: Union[int, str] = Field(description="Variable 44: Deception used (false feedback/computer strategy disguised): 0=No, 1=Yes.")
    real_part: Union[int, str] = Field(description="Variable 45: Real interactions: 0=No (imagined/computer), 1=Yes (no deception), 2=Yes (deception).")
    periods: Union[int, str] = Field(description="Variable 46: Cooperation measurement level: 1=All, 2=First, 3=Last, 4=First and Last, 5=Others.")
    sanction: str = Field(description="Variable 58: Punishment or reward mechanism in place: 0=No, 1=Yes. If manipulated within, use semicolon '0 ; 1'.")
    acquaintance: Union[int, str] = Field(description="Variable 59: Interacting with acquaintances/friends: 0=No, 1=Yes, 2=Something in between (e.g., small community).")

# COOKBOOK Fields 34 -> 37
class GameParametersSchema(BaseModel):
    if_pd_k_index: Union[float, str] = Field(description="Variable 34: K Index for symmetric PD: K=(R-P)/(T-S). Range: 0~1. Code 'N/A' if not applicable.")
    if_pgd_mpcr: Union[float, str] = Field(description="Variable 35: Marginal per capita return for continuous PGD (multiplier / group size). Range: 0~1. Code 'N/A' if not continuous PGD.")
    if_step_level_provision_point: Union[float, str] = Field(description="Variable 36: Threshold for step-level PGD. Code 'N/A' if not step-level.")
    if_rd_replenishment_rate: Union[float, str] = Field(description="Variable 37: Replenishment rate in resource dilemma (>= 1.0). Code 'N/A' if not RD.")

# COOKBOOK Fields 47 -> 54, 60
class ResultsSchema(BaseModel):
    overall_p_c: Union[float, str] = Field(description="Variable 47: Overall proportion of cooperative choices across trials (dichotomous games). Else 'N/A' or 999.")
    overall_m_withdrawal: Union[float, str] = Field(description="Variable 48: Mean amount of resource withdrawn from common pool (Resource Dilemma). Else 'N/A'.")
    overall_m_cooperation: Union[float, str] = Field(description="Variable 49: Overall mean of contribution (continuous games). Else 'N/A'.")
    overall_sd_cooperation: Union[float, str] = Field(description="Variable 50: Overall standard deviation of contributions/withdrawals. Else 'N/A'.")
    p_e_contributed: Union[float, str] = Field(description="Variable 51: Proportion of endowment contributed: (M - lower)/(upper - lower). Else 'N/A'.")
    ivs: str = Field(description="Variable 52: Clear description of independent variables and design conditions.")
    other_variables_measured: str = Field(description="Variable 53: Other measured variables/scales in the study.")
    comments: str = Field(description="Variable 54: Sample inconsistencies, notes, or questionable practices; else 'N/A'.")
    n_obs: str = Field(description="Variable 60: Code 'N/A' except when decision maker is a group making a single decision; then code number of group decision makers.")

# COOKBOOOK Fields 55, 56, 57 -> N
class VariablesSchema(BaseModel):
    var_1: str = Field(description="Variable 55: Name of the variable if a reliability test is provided; else 'N/A'.")
    rel_coeff_1: str = Field(description="Variable 56: Reliability coefficient used (e.g., a, rho, k, r, rho'); else 'N/A'.")
    rel_statistics_1: Union[float, str] = Field(description="Variable 57: Value of reliability coefficient; else 'N/A'.")

