from fastapi import APIRouter, Query, Depends, HTTPException, BackgroundTasks
import httpx
import asyncio
import websockets
import json
from typing import List
from app.models import models
# from app.db.schema import Call
# from sqlalchemy.orm.session import Session 


# from sqlalchemy.orm import Session
# from app.db.database import get_db, SessionLocal
import ssl, certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())


router = APIRouter()



sample_countries = models.Countries(countries=[
    models.Country(name="Nigeria", capital="Abuja"),
    models.Country(name="USA", capital="Washington, D.C."),
])

# GET endpoint
@router.get("/countries", response_model=models.Countries)
def get_countries():
    return sample_countries


#######################################
 

# VAPI_API_KEY
# "assistantId":
# "customer phone":
# "phoneNumberId":


VAPI_API_KEY = "e607594b-68fc-4c70-a5da-4424c7125340"
VAPI_URL = "https://api.vapi.ai/call"

# async with websockets.connect(listen_url, ssl=ssl_context, ping_interval=10, ping_timeout=20) as ws:
async def listen_to_vapi(listen_url: str):
    print(f"Connecting to listen stream: {listen_url}")
    for attempt in range(2):  # x2
        try:
            async with websockets.connect(listen_url, ssl=ssl_context, ping_interval=10, ping_timeout=20) as ws:
                print("Connected to Vapi audio stream")
                async for message in ws:
                    if isinstance(message, bytes):
                        print(f"Received binary chunk: {len(message)} bytes")
                    else:
                        try:
                            data = json.loads(message)
                            print("Message:", data)
                        except json.JSONDecodeError:
                            print("Raw text:", message)
                break  # exit loop if connection closed gracefully
        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}")
            await asyncio.sleep(0.5)  # brief pause before retry



@router.post("/start-call")
async def start_call():
    payload = {
        "assistantId": "dad2c117-6f5e-445e-ab1e-47dcc4f81719",
        "customer": {"number": "+966544332616"},
        "phoneNumberId": "8bfa8f0b-c80c-4863-91d9-26f3748dcb25",
    }

    headers = {
        "authorization": f"Bearer {VAPI_API_KEY}",
        "content-type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(VAPI_URL, headers=headers, json=payload)

    if 200 <= response.status_code < 300:
        data = response.json()
        listen_url = data.get("monitor", {}).get("listenUrl")
        if listen_url:
            print("Got listenUrl, connecting immediately...")
            asyncio.create_task(listen_to_vapi(listen_url))  # connect instantly
            return {"status": "connected", "listen_url": listen_url}
        else:
            print("No listenUrl found in response.")
            return {"status": "error", "message": "No listenUrl found in response."}
    else:
        print("Failed to start call:", response.text)
        return {"status": "error", "message": response.text}

