from typing import Dict, Any

# Official codebook sequence for variables 1 through 60
CODEBOOK_FIELD_ORDER = [
    "study_ID", "authors_and_year", "title", "study_num", "overlaps_with", "published_status",
    "data_collection_year", "source_of_year", "country", "source_of_country", 
    "sample_size", "prop_male", "m_age", "age_range_lower", "age_range_upper", 
    "students", "discipline", "recr_meth", "if_other_recr_meth",
    "exp_setting", "dilemma_type", "if_other_dilemma_type", "if_pgd_continuous_step", 
    "symmetry", "one_shot", "matching", "if_one_shot_repeated", "iterated_num_per_block", 
    "block_num", "end_game_effect", "payment_show_up", "payment_game", "group_size", 
    "if_pd_k_index", "if_pgd_mpcr", "if_step_level_provision_point", "if_rd_replenishment_rate",
    "discussion", "simultaneous", "choice_range_lower", "choice_range_upper", 
    "num_choice_options", "feedback", "deception", "real_part", "periods", 
    "overall_p_c", "overall_m_withdrawal", "overall_m_cooperation", "overall_sd_cooperation", 
    "p_e_contributed", "ivs", "other_variables_measured", "comments", 
    # "var_1", "rel_coeff_1", "rel_statistics_1",
    "sanction", "acquaintance", "n_obs"
]

# Maps internal snake_case keys strictly to clean codebook labels
CODEBOOK_TRANSLATION_MAP = {
    "study_ID": "study_ID",
    "authors_and_year": "Author(s)+year",
    "title": "Title",
    "study_num": "Study #",
    "overlaps_with": "Overlaps with...",
    "published_status": "Published/Not published",
    "data_collection_year": "Year of data collection",
    "source_of_year": "Source of year",
    "country": "Country",
    "source_of_country": "Source of country",
    "sample_size": "N",
    "prop_male": "Prop. Male",
    "m_age": "M_age",
    "age_range_lower": "age range lower",
    "age_range_upper": "age range upper",
    "students": "Students",
    "discipline": "Discipline",
    "recr_meth": "Recr_Meth",
    "if_other_recr_meth": "If other Recr_Meth: Specify",
    "exp_setting": "Exp_Setting",
    "dilemma_type": "Dilemma type(s)",
    "if_other_dilemma_type": "If other Dilemma type: Specify",
    "if_pgd_continuous_step": "If PGD: Continuous/step-level",
    "symmetry": "Symm.",
    "one_shot": "One-shot",
    "matching": "Matching",
    "if_one_shot_repeated": "If one-shot: Repeated",
    "iterated_num_per_block": "Iterated # per block",
    "block_num": "Block #",
    "end_game_effect": "End game effect",
    "payment_show_up": "Payment (show up fee)",
    "payment_game": "Payment (game)",
    "group_size": "Group size(s)",
    "if_pd_k_index": "If PD: K index",
    "if_pgd_mpcr": "If PGD: MPCR",
    "if_step_level_provision_point": "If step-level: provision point",
    "if_rd_replenishment_rate": "If RD: replenishment rate",
    "discussion": "Discussion",
    "simultaneous": "Simultaneous",
    "choice_range_lower": "Choice range lower",
    "choice_range_upper": "Choice range upper",
    "num_choice_options": "# of choice options",
    "feedback": "Feedback",
    "deception": "Deception",
    "real_part": "Real_Part.",
    "periods": "Periods",
    "overall_p_c": "Overall P(C)",
    "overall_m_withdrawal": "Overall M withdrawal",
    "overall_m_cooperation": "Overall M cooperation",
    "overall_sd_cooperation": "Overall SD cooperation",
    "p_e_contributed": "P(E) contributed",
    "ivs": "IVs",
    "other_variables_measured": "Other variables measured",
    "comments": "Comments",
    # "var_1": "VAR_1",
    # "rel_coeff_1": "Rel. Coeff_1",
    # "rel_statistics_1": "Rel. Statistics_1",
    "sanction": "Sanction",
    "acquaintance": "Acquaintance",
    "n_obs": "N.obs"
}



def sort_record_by_codebook(raw_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sorts a flat extraction dictionary according to the official codebook field order.
    Any extracted keys not explicitly found in the standard list are appended gracefully at the end.
    """
    sorted_record = {}

    # 1. Pull keys in official codebook sequence
    for field in CODEBOOK_FIELD_ORDER:
        if field in raw_record:
            sorted_record[field] = raw_record[field]

    # 2. Append unexpected metadata fields (if any exist) so no data is dropped
    for key, value in raw_record.items():
        if key not in sorted_record:
            sorted_record[key] = value

    return sorted_record


def translate_to_codebook_headers(data_record: dict) -> dict:
    """
    Translates a record's pythonic keys into clean, un-numbered Codebook labels.
    Leaves any unmapped keys unchanged.
    """
    return {CODEBOOK_TRANSLATION_MAP.get(k, k): v for k, v in data_record.items()}
