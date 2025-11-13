import os
import asyncio
import websockets
import json
import base64
import ssl
from datetime import datetime
from dotenv import load_dotenv
from live_audio_stream_transcription_diarization.sentiment_analysis import get_emotions

load_dotenv(".env")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

timestamp = datetime.now().isoformat(timespec='seconds')

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
        self.customer_transcripts = []
        self.agent_transcripts = []

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
                            start = data["start"]
                            end = data["duration"]
                            emotion_classify = get_emotions(transcript)
                            print("Customer Emotion:", emotion_classify)
                            key, value = next(iter(emotion_classify.items()))
                            if key in ("anger", "disgust", "sadness"):
                                value -= 0.7
                            entry = {"timestamp": timestamp, "speaker": "customer", "text": transcript, "start": start, "end": end, "score": value}
                            self.customer_transcripts.append(entry)

                    elif data.get("channel_index") == [1, 2]:
                        alt = data["channel"]["alternatives"][0] if data["channel"].get("alternatives") else {}
                        transcript = alt.get("transcript", "")
                        if transcript:
                            print("AI agent Transcript:", transcript)
                            start = data["start"]
                            end = data["duration"]
                            emotion_classify = get_emotions(transcript)
                            key, value = next(iter(emotion_classify.items()))
                            if key in ("anger", "disgust", "sadness"):
                                value -= 0.7
                            entry = {"timestamp": timestamp, "speaker": "agent", "text": transcript, "start": start, "end": end, "score": value}
                            self.agent_transcripts.append(entry)
                            

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

    def get_transcript(self, speaker="both"):
        if speaker == "customer":
            # return " ".join(self.customer_transcripts)
            return self.customer_transcripts[-1] if self.customer_transcripts and len(self.customer_transcripts) > 0 else {}
        elif speaker == "agent":
            # return " ".join(self.agent_transcripts)
            return self.agent_transcripts[-1] if self.agent_transcripts and len(self.agent_transcripts) > 0 else {}
        else:
            # Combine both in order of collection (you could timestamp if needed)
            return {
                "customer": self.customer_transcripts[-1] if self.customer_transcripts and len(self.customer_transcripts) > 0 else {},
                "agent": self.agent_transcripts[-1] if self.agent_transcripts and len(self.agent_transcripts) > 0 else {}
            }

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
