import os
import asyncio
import websockets
import json
import base64
import ssl
from dotenv import load_dotenv
from live_audio_stream_transcription_diarization.sentiment_analysis import get_emotions

load_dotenv(".env")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("DEEPGRAM_API_KEY:", DEEPGRAM_API_KEY)


# DEEPGRAM_URL = (
#     "wss://api.deepgram.com/v1/listen?"
#     "encoding=linear16&sample_rate=16000&channels=2"
#     "&model=nova-2"
#     "&diarize=true"
#     "&punctuate=true"
# )
DEEPGRAM_URL = (
    "wss://api.deepgram.com/v1/listen?"
    "encoding=linear16&sample_rate=16000&channels=2"
    "&multichannel=true"
    "&model=nova-2"
    "&diarize=true"
    "&punctuate=true"
)

class DeepgramLiveTranscriber:
    def __init__(self):
        self.connection = None

    async def connect(self):
        headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}
        ssl_context = ssl.create_default_context()
        print("Connecting to Deepgram WebSocket...")

        self.connection = await websockets.connect(
            DEEPGRAM_URL,
            extra_headers=headers,
            ssl=ssl_context,
            ping_interval=10,
            ping_timeout=20,
        )
        print("Connected to Deepgram!")

        # Start background listener
        asyncio.create_task(self.receive_messages())

    async def receive_messages(self):
        try:
            async for msg in self.connection:
                # print("Raw:", msg)
                data = json.loads(msg)
                if "channel" in data:
                    if data.get("channel_index") == [0, 2]:
                        alt = data["channel"]["alternatives"][0] if data["channel"].get("alternatives") else {}
                        transcript = alt.get("transcript", "")
                        if transcript:
                            print("Customer Transcript:", transcript)
                            emotion_classify = get_emotions(transcript)
                            print("Customer Emotion:", emotion_classify)

                    elif data.get("channel_index") == [1, 2]:
                        alt = data["channel"]["alternatives"][0] if data["channel"].get("alternatives") else {}
                        transcript = alt.get("transcript", "")
                        if transcript:
                            print("AI agent Transcript:", transcript)


        except Exception as e:
            print(f"Error receiving Deepgram messages: {e}")

    async def send_audio(self, chunk: bytes):
        try:
            await self.connection.send(chunk)
        except Exception as e:
            print(f"Error sending audio: {e}")

    async def finish(self):
        try:
            await self.connection.send(json.dumps({"type": "CloseStream"}))
        except:
            pass

    async def close(self):
        if self.connection:
            await self.connection.close()
            print("Deepgram connection closed.")


async def test_deepgram():
    deepgram = DeepgramLiveTranscriber()
    await deepgram.connect()

    # Send a local sample.wav file
    with open("sample.wav", "rb") as f:
        while chunk := f.read(4096):
            await deepgram.send_audio(chunk)

    
    await deepgram.finish()
    await asyncio.sleep(2)
    await deepgram.close()


if __name__ == "__main__":
    asyncio.run(test_deepgram())
