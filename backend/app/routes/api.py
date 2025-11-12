import os
from fastapi import APIRouter
import httpx
import asyncio
import websockets
import json
from pydub import AudioSegment
from live_audio_stream_transcription_diarization.audio_diarize_deepgram import DeepgramLiveTranscriber
import ssl, certifi
from dotenv import load_dotenv

ssl_context = ssl.create_default_context(cafile=certifi.where())
load_dotenv(".env")
router = APIRouter()

CHUNKS_PER_FILE = 200
OUTPUT_DIR = "/data" 
SAMPLE_WIDTH = 2 
FRAME_RATE = 30000
CHANNELS = 1

os.makedirs(OUTPUT_DIR, exist_ok=True)

buffer = bytearray()  

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
CUSTOMER_PHONE_NUMBER = os.getenv("CUSTOMER_PHONE_NUMBER")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

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
                        print("Task 1", deepgram.get_transcript("customer"))

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

    # print(deepgram.get_transcript("customer"))
    # Wrap up Deepgram connection
    await deepgram.finish()
    await asyncio.sleep(2)
    await deepgram.close()
    print("Deepgram connection closed.")
    # return deepgram.get_transcript("customer")
    



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
            # asyncio.create_task(listen_to_vapi(listen_url))
            asyncio.create_task(listen_to_vapi(listen_url))
            return {"status": "connected", "listen_url": listen_url}
        else:
            print("No listenUrl found in response.")
            return {"status": "error", "message": "No listenUrl found in response."}
    else:
        print("Failed to start call:", response.text)
        return {"status": "error", "message": response.text}


