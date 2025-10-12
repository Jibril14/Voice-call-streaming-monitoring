from pydantic import BaseModel
from typing import List

class SentimentRecord(BaseModel):
    date: str
    score: float
    name: str

class Country(BaseModel):
    name: str
    capital: str

class Countries(BaseModel):
    countries: List[Country]
