import asyncio
import websockets
import json
import ssl
import certifi

DEEPGRAM_API_KEY = "b8919e8cbe5181cfc4e899b9a8c64bae99cf39f3"

ssl_context = ssl.create_default_context(cafile=certifi.where())

class DeepgramLiveTranscriber:
    """
    Maintain a persistent WebSocket connection to Deepgram for real-time
    transcription and diarization. Audio bytes can be streamed continuously.
    """

    def __init__(self, model: str = "nova-2", diarize: bool = True):
        self.uri = f"wss://api.deepgram.com/v1/listen?model={model}&diarize={'true' if diarize else 'false'}"
        self.connection = None
        self.send_queue = asyncio.Queue()
        self.is_running = False

    async def connect(self):
        """
        Establish a single persistent WebSocket connection.
        """
        headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}
        print("🔌 Connecting to Deepgram WebSocket...")
        self.connection = await websockets.connect(self.uri, extra_headers=headers, ssl=ssl_context)
        print("✅ Connected to Deepgram")

        self.is_running = True
        # Start sender and receiver tasks
        asyncio.create_task(self._sender())
        asyncio.create_task(self._receiver())

    async def _sender(self):
        try:
            while self.is_running:
                try:
                    chunk = await asyncio.wait_for(self.send_queue.get(), timeout=5.0)
                    if chunk is None:
                        break
                    await self.connection.send(chunk)
                except asyncio.TimeoutError:
                    # No audio for a few seconds, send keepalive ping
                    await self.connection.send(b'\x00' * 320)  # 10ms of silence
        except Exception as e:
            print(f"❌ Error sending audio to Deepgram: {e}")


    async def _receiver(self):
        """
        Continuously receive and print transcriptions and diarization results.
        """
        try:
            async for message in self.connection:
                data = json.loads(message)
                # Handle different event types
                if "channel" in data:
                    transcript = data["channel"]["alternatives"][0].get("transcript", "")
                    if transcript:
                        print("🗣️ Transcript:", transcript)
                    if "words" in data["channel"]["alternatives"][0]:
                        for word in data["channel"]["alternatives"][0]["words"]:
                            if "speaker" in word:
                                print(f"👤 Speaker {word['speaker']}: {word['word']}")
        except Exception as e:
            print(f"❌ Error receiving Deepgram messages: {e}")

    async def send_audio(self, audio_chunk: bytes):
        """
        Queue an audio chunk for sending.
        """
        if self.is_running:
            await self.send_queue.put(audio_chunk)
        else:
            print("⚠️ Deepgram connection not active. Ignoring audio chunk.")

    async def close(self):
        print("🔒 Closing Deepgram connection...")
        self.is_running = False
        await self.send_queue.put(None)
        if self.connection:
            try:
                await self.connection.send(json.dumps({"type": "CloseStream"}))
            except Exception:
                pass
            await self.connection.close()
        print("✅ Deepgram connection closed.")

