from pydantic import BaseModel

class SentimentRecord(BaseModel):
    date: str
    score: float
    name: str
