import os
from fastapi import APIRouter
import httpx
import asyncio
import websockets
import json
from pydub import AudioSegment
from app.models import models
# from live_audio_stream.audio_stream_realtime_classify import classify_emotion
# from live_audio_stream_transcription_diarization.audio_diarize import audio_diarize
from live_audio_stream_transcription_diarization.test import DeepgramLiveTranscriber
# from live_audio_stream_transcription_diarization.sentiment_analysis import get_emotions

import ssl, certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

from dotenv import load_dotenv
load_dotenv(".env")


router = APIRouter()


CHUNKS_PER_FILE = 200
OUTPUT_DIR = "/data" 
SAMPLE_WIDTH = 2 
FRAME_RATE = 30000
CHANNELS = 1

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Buffer to collect audio chunks
buffer = bytearray()  



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


VAPI_API_KEY = os.getenv("VAPI_API_KEY")
CUSTOMER_PHONE_NUMBER = os.getenv("CUSTOMER_PHONE_NUMBER")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
# VAPI_API_KEY = VAPI_API_KEY[0]

VAPI_URL = "https://api.vapi.ai/call"



async def listen_to_vapi(listen_url: str):
    print(f"Connecting to Vapi stream: {listen_url}")

    deepgram = DeepgramLiveTranscriber()
    await deepgram.connect()  # Connect to Deepgram WebSocket

    ssl_context = ssl.create_default_context()

    buffer = bytearray()
    chunk_count = 0

    for attempt in range(4):
        try:
            async with websockets.connect(
                listen_url,
                ssl=ssl_context,
                ping_interval=5,
                ping_timeout=10
            ) as ws:
                print("Connected to Vapi audio stream")

                async for msg in ws:
                    if isinstance(msg, bytes):
                        # Send live audio to Deepgram
                        await deepgram.send_audio(msg)

                        # Buffer & optionally save locally
                        buffer.extend(msg)
                        if len(buffer) >= CHUNKS_PER_FILE * len(msg):
                            audio_segment = AudioSegment(
                                data=bytes(buffer),
                                sample_width=SAMPLE_WIDTH,
                                frame_rate=FRAME_RATE,
                                channels=CHANNELS,
                            )
                            filename = f"{OUTPUT_DIR}/chunk_{chunk_count:04d}.wav"
                            audio_segment.export(filename, format="wav")
                            print(f"Saved {filename} ({len(buffer)} bytes)")
                            buffer.clear()
                            chunk_count += 1

                        # 💤 Optional throttle — slow the sending loop
                        # await asyncio.sleep(0.02)

                    else:
                        try:
                            data = json.loads(msg)
                            print("Vapi message:", data)
                        except json.JSONDecodeError:
                            print("Raw text:", msg)

                print("Vapi connection ended.")
                break

        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}")
            await asyncio.sleep(0.5)

    # Wrap up Deepgram connection
    await deepgram.finish()
    await asyncio.sleep(2)
    await deepgram.close()
    print("Deepgram connection closed.")



@router.post("/start-call")
async def start_call():
    payload = {
        "assistantId": ASSISTANT_ID,
        "customer": {"number": CUSTOMER_PHONE_NUMBER},
        "phoneNumberId": PHONE_NUMBER_ID
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
            asyncio.create_task(listen_to_vapi(listen_url))
            # asyncio.create_task(listen_to_vapi(listen_url))  # connect instantly
            return {"status": "connected", "listen_url": listen_url}
        else:
            print("No listenUrl found in response.")
            return {"status": "error", "message": "No listenUrl found in response."}
    else:
        print("Failed to start call:", response.text)
        return {"status": "error", "message": response.text}


