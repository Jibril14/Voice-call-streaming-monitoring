from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class Country(BaseModel):
    name: str
    capital: str

class CountryDisplay(BaseModel):
    name: str
    capital: str
    class Config():
        orm_mode = True

class Countries(BaseModel):
    countries: List[Country]

###################################################

class Word(BaseModel):
    word: str
    start: float
    end: float


class TranscriptItem(BaseModel):
    role: str
    content: str
    words: List[Word]
    sentiment_score: Optional[float] = Field(alias="sentiment score")

    model_config = ConfigDict(extra="ignore")


class CallAnalysis(BaseModel):
    call_summary: str
    Overall_sentiment: str

    model_config = ConfigDict(extra="ignore")


class RetellLLMVariables(BaseModel):
    customer_name: Optional[str]

    model_config = ConfigDict(extra="ignore")


class CallData(BaseModel):
    call_id: str
    agent_id: str
    retell_llm_dynamic_variables: RetellLLMVariables
    start_timestamp: int
    end_timestamp: int
    duration_ms: int
    transcript_object: List[TranscriptItem]
    call_analysis: CallAnalysis
    model_config = ConfigDict(extra="ignore")
