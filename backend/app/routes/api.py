import json
import asyncio
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from typing import List
from data.generate_data import generated_data
from app.models import models

router = APIRouter()


starter_data = [
    {'date': "1970-01-01", 'score': 0.000, 'name': ''},
    {'date': "1970-01-01", 'score': 0.000, 'name': ''}
]

@router.get("/sentiment", response_model=List[models.SentimentRecord])
async def get_sentiment(kw1: str = Query(...), kw2: str = Query(...)):
    filtered = []
    names = [kw1.capitalize(), kw2.capitalize()]
    for i, item in enumerate(starter_data):
        item['name'] = names[i]
        filtered.append(item)
    return filtered


async def generate_json_stream(data):
    for item in data:
        yield json.dumps(item) + "\n"
        await asyncio.sleep(6)  # simulate delay, This can be data from kafka

@router.get("/sentiment/stream")
async def get_sentiment(kw1: str = Query(...), kw2: str = Query(...)):
    filtered = [
        entry for entry in generated_data
        if entry["name"].lower() in [kw1.lower(), kw2.lower()]
    ]
    return StreamingResponse(generate_json_stream(filtered), media_type="application/json")