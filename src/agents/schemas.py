from pydantic import BaseModel, Field
from typing import List

# CODEBOOK Fields 2 -> 6
class StudyMetadataSchema(BaseModel):
    authors_and_year: str = Field(description="The names of the authors and the publication year in parenthesis. Example: Author A, Author B, Author C (YYY)")
    title: str = Field(description="The title of the research paper.")
    study_number: str = Field(description="") # TODO: add description
    # overlaps_with: str = Field(description="In case the data from one study overlaps with the data from another study, mention here (code doi if available; otherwise code paper_ID/study_ID) ")
    published_status: int = Field(description="1=Published, 2=Raw data, 3=Doctoral Dissertation, 4=Working paper, 5=Master’s thesis")



# CODEBOOK Fields 7 -> 11
class DataMetadataSchema(BaseModel):
    data_collection_year: int = Field(description="Year when the data was collected. If not specified, get as precise estimation of the year of data collection as possible. In case of not specified: extract the year from sources in the order of when the paper was accessible as working paper, presented, received/ submitted, accepted, available online after acceptance, published.")
    source_of_year: int = Field(description="Source of the year when the data was collected 1=Conducted, 2=Presented, 3=Working paper published, 4=Received/Submitted, 5=Published, 6=Accepted, 7=Available online")
    country: str = Field(description="Country where the data collection took place coded with the 3-letter country code following ISO 3166-1 alpha-3")
    source_of_country: int = Field(description="Source of the country where the data collection took place. 1=Specified country, 2=Multiple countries, 3=All authors, 4=Most authors. \n(1)  Specified country: The paper explicitly states that data have been collected at a certain location (e.g., University of X, Y lab, using Z participants pool); \n(2) Multiple countries: The paper specifies that most participants come from Country X (that should be indicated under Country), but that a smaller percentage comes from different countries (indicate the percentages and nationalities in a note, if the information is available); \n(3) All authors: The paper does not specify the country, but all authors are affiliated to the same institution in Country X (that should be indicated under Country) (indicate it for single-authored papers), \n(4) Most authors: The majority of the authors are affiliated to the same institution in Country X.")
    sample_size: int = Field(description="Total sample size in a single study after exclusion of participants. If a single study is coded as two because participants were randomly assigned to two different games, this sample size should be divided by two. Please don’t stop at the first N you see in the text, but be very careful in detecting excluded participants in the study/analyses. Write a note to indicate initial N and reason for exclusion.")


# CODEBOOK Fields 12 -> 17
class ParticipantsSchema(BaseModel):
    prop_male: float = Field(description="Proportion of male participants in the whole sample of a study after exclusion of participants, if possible. If authors do not update this information, code it for initial sample size and write “Information based upon initial sample size” in a note.")
    mean_age: float = Field(description="Participants’ mean age in years after exclusion of participants, if possible. If authors do not update this information, code it for initial sample size and write “Information based upon initial sample size” in a note")
    age_range_lower: int = Field(description="Minimum age of all sampled participants")
    age_range_higher: int = Field(description="Maximum age of all sampled participants")
    students: int = Field(description="Whether participants were student samples: 0=No, 1=Yes")
    discipline: int = Field(description="Specific discipline the students are from 1=Economics, 2=Psychology, 3=Sociology, 4=Mixed, 5=Other.\nCode N/A only for non-students samples, otherwise 999 if not mentioned; code as 5 for students from another single discipline (e.g., MBA students)")

class ExperimentSchema(BaseModel):
    recr_meth: int = Field(description="The way participants were recruited 1 = Participant pool, 2 =  Mturk, 3 = Advertisement, 4 = Other, 5 = ORSEE, 6 =  Prolific.")
    other_recr: str = Field(description="If participants were recruited in other ways, specify here.")
    # TODO: Complete
