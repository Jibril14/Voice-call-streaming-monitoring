from pydub import AudioSegment
import os

CHUNKS_PER_FILE = 25  # Number of chunks to collect before saving
OUTPUT_DIR = "/data"  # Directory to save audio files
SAMPLE_WIDTH = 2  # Assuming 16-bit audio, 2 bytes per sample
FRAME_RATE = 16000  # Assuming 16kHz sampling rate
CHANNELS = 1  # Mono audio

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Buffer to collect audio chunks
buffer = bytearray()  
chunk_count = 0

async def listen_to_vapi(listen_url: str):
    print(f"Connecting to listen stream: {listen_url}")
    for attempt in range(2):  # Try 2 times
        try:
            async with websockets.connect(listen_url, ssl=ssl_context, ping_interval=10, ping_timeout=20) as ws:
                print("Connected to Vapi audio stream")
                async for msg in ws:
                    if isinstance(msg, bytes):
                        buffer.extend(msg)

                        # Process when enough chunks are collected
                        if len(buffer) >= CHUNKS_PER_FILE * len(msg):
                            # Create AudioSegment from the buffer
                            audio_segment = AudioSegment(
                                data=bytes(buffer),
                                sample_width=SAMPLE_WIDTH,
                                frame_rate=FRAME_RATE,
                                channels=CHANNELS,
                            )

                            # Save the audio segment to a file
                            filename = f"{OUTPUT_DIR}/chunk_{chunk_count:04d}.wav"
                            audio_segment.export(filename, format="wav")

                            print(f"Saved {filename}")
                            # Reset the buffer for the next set of chunks
                            buffer.clear()
                            chunk_count += 1

                    else:
                        try:
                            data = json.loads(msg)
                            print("Message:", data)
                        except json.JSONDecodeError:
                            print("Raw text:", msg)

                break  # Exit loop if connection closed gracefully
        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}")
            await asyncio.sleep(0.5)  # Brief pause before retry


####################################################################################


#######################################
 

# VAPI_API_KEY
# "assistantId":
# "customer phone":
# "phoneNumberId":

chunk_count

VAPI_API_KEY = "e607594b-68fc-4c70-a5da-4424c7125340"
VAPI_URL = "https://api.vapi.ai/call"

# async with websockets.connect(listen_url, ssl=ssl_context, ping_interval=10, ping_timeout=20) as ws:
async def listen_to_vapi(listen_url: str):
    print(f"Connecting to listen stream: {listen_url}")
    for attempt in range(4):  # Try 2 times
        try:
            async with websockets.connect(listen_url, ssl=ssl_context, ping_interval=10, ping_timeout=20) as ws:
                print("Connected to Vapi audio stream")
                async for msg in ws:
                    if isinstance(msg, bytes):
                        buffer.extend(msg)

                        # Process when few chunks 25 collected
                        if len(buffer) >= CHUNKS_PER_FILE * len(msg):
                            # Create AudioSegment from the buffer
                            audio_segment = AudioSegment(
                                data=bytes(buffer),
                                sample_width=SAMPLE_WIDTH,
                                frame_rate=FRAME_RATE,
                                channels=CHANNELS,
                            )

                            # Save the audio segment to a file
                            filename = f"{OUTPUT_DIR}/chunk_{chunk_count:04d}.wav"
                            audio_segment.export(filename, format="wav")

                            print(f"Saved {filename}")
                            # Reset the buffer for the next set of chunks
                            buffer.clear()
                            chunk_count += 1

                    else:
                        try:
                            data = json.loads(msg)
                            print("Message:", data)
                        except json.JSONDecodeError:
                            print("Raw text:", msg)

                break
        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}")
            await asyncio.sleep(0.5)


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





################################################# 3rd

from fastapi import APIRouter, Query, Depends, HTTPException, BackgroundTasks
import httpx
import asyncio
import websockets
import json
from typing import List
from app.models import models
from live_audio_stream.audio_stream_realtime_classify import classify_emotion

import ssl, certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

router = APIRouter()



from pydub import AudioSegment
import os

CHUNKS_PER_FILE = 250 
OUTPUT_DIR = "/data" 
SAMPLE_WIDTH = 2 
FRAME_RATE = 16000
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


VAPI_API_KEY = "e607594b-68fc-4c70-a5da-4424c7125340"
VAPI_URL = "https://api.vapi.ai/call"

# async with websockets.connect(listen_url, ssl=ssl_context, ping_interval=10, ping_timeout=20) as ws:
async def listen_to_vapi(listen_url: str):
    chunk_count = 0
    print(f"Connecting to listen stream: {listen_url}")
    for attempt in range(4):  # Try 2 times
        try:
            async with websockets.connect(listen_url, ssl=ssl_context, ping_interval=10, ping_timeout=20) as ws:
                print("Connected to Vapi audio stream")
                async for msg in ws:
                    if isinstance(msg, bytes):
                        buffer.extend(msg)

                        # Process when few chunks 25 collected
                        if len(buffer) >= CHUNKS_PER_FILE * len(msg):
                            # Create AudioSegment from the buffer
                            audio_segment = AudioSegment(
                                data=bytes(buffer),
                                sample_width=SAMPLE_WIDTH,
                                frame_rate=FRAME_RATE,
                                channels=CHANNELS,
                            )

                            # Save the audio segment to a file
                            filename = f"{OUTPUT_DIR}/chunk_{chunk_count:04d}.wav"
                            audio_segment.export(filename, format="wav")

                            print(f"Saved {filename}")
                            # Reset the buffer for the next set of chunks
                            buffer.clear()
                            chunk_count += 1

                    else:
                        try:
                            data = json.loads(msg)
                            print("Message:", data)
                        except json.JSONDecodeError:
                            print("Raw text:", msg)

                break
        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}")
            await asyncio.sleep(0.5)


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













############################### 4 #####################################################################



from fastapi import APIRouter, Query, Depends, HTTPException, BackgroundTasks
import httpx
import asyncio
import websockets
import json
from typing import List
from app.models import models
from live_audio_stream.audio_stream_realtime_classify import classify_emotion

import ssl, certifi
ssl_context = ssl.create_default_context(cafile=certifi.where())

router = APIRouter()

import wave

from pydub import AudioSegment
import os

CHUNKS_PER_FILE = 250 
OUTPUT_DIR = "/data" 
SAMPLE_WIDTH = 2 
FRAME_RATE = 24,000
CHANNELS = 1
SECONDS_PER_FILE = 5

# FRAME_RATE = 16000

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


VAPI_API_KEY = "e607594b-68fc-4c70-a5da-4424c7125340"
VAPI_URL = "https://api.vapi.ai/call"

# async with websockets.connect(listen_url, ssl=ssl_context, ping_interval=10, ping_timeout=20) as ws:
BYTES_PER_SECOND = FRAME_RATE * SAMPLE_WIDTH * CHANNELS
BUFFER_LIMIT = SECONDS_PER_FILE * BYTES_PER_SECOND  # how many bytes = N seconds

async def listen_to_vapi(listen_url: str):
    ssl_context = ssl.create_default_context()
    print(f"Connecting to listen stream: {listen_url}")
    chunk_count = 0
    buffer = bytearray()

    for attempt in range(4):
        try:
            async with websockets.connect(listen_url, ssl=ssl_context,
                                        ping_interval=10, ping_timeout=20) as ws:
                print("Connected to Vapi audio stream")

                async for msg in ws:
                    if isinstance(msg, bytes):
                        buffer.extend(msg)

                        # when we have enough for N seconds, write to wav
                        if len(buffer) >= BUFFER_LIMIT:
                            audio_segment = AudioSegment(
                                data=bytes(buffer),
                                sample_width=SAMPLE_WIDTH,
                                frame_rate=FRAME_RATE,
                                channels=CHANNELS,
                            )
                            filename = f"{OUTPUT_DIR}/chunk_{chunk_count:04d}.wav"
                            audio_segment.export(filename, format="wav")
                            print(f"Saved {filename} ({len(buffer)} bytes ≈ {SECONDS_PER_FILE}s)")
                            buffer.clear()
                            chunk_count += 1

                    else:
                        print("Text:", msg)

        except Exception as e:
            print(f"Connection attempt {attempt+1} failed: {e}")
            print("Error connecting to Vapi stream:", e)


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

