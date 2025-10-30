import asyncio
import websockets
import json
import ssl, certifi

DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"
DEEPGRAM_URL = "wss://api.deepgram.com/v1/listen?model=nova-2&diarize=true"

ssl_context = ssl.create_default_context(cafile=certifi.where())


async def deepgram_live_transcribe(audio_stream_generator):
    """
    Stream audio to Deepgram WebSocket API for real-time transcription & diarization.

    Args:
        audio_stream_generator: An async generator yielding raw PCM audio bytes (from Vapi stream)
    """
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
    }

    async with websockets.connect(
        DEEPGRAM_URL,
        extra_headers=headers,
        ssl=ssl_context,
        ping_interval=5,
        ping_timeout=20,
        max_size=10 * 1024 * 1024,  # allow large messages
    ) as ws:
        print("Connected to Deepgram WebSocket")

        # Run both sending and receiving tasks concurrently
        async def send_audio():
            try:
                async for chunk in audio_stream_generator:
                    if not isinstance(chunk, (bytes, bytearray)):
                        continue
                    await ws.send(chunk)
                await ws.send(json.dumps({"type": "CloseStream"}))
                print("Finished sending audio stream to Deepgram.")
            except Exception as e:
                print(f"Error sending audio: {e}")

        async def receive_transcripts():
            try:
                async for message in ws:
                    data = json.loads(message)
                    # Deepgram real-time transcripts come as partials or finals
                    if "channel" in data:
                        alt = data["channel"]["alternatives"][0]
                        transcript = alt.get("transcript", "")
                        if transcript.strip():
                            print(f"🗣️ {transcript}")
                            # Speaker diarization info
                            words = alt.get("words", [])
                            if words:
                                speakers = {w["speaker"] for w in words if "speaker" in w}
                                print(f"Speakers detected: {speakers}")
                    elif data.get("type") == "Metadata":
                        print("Metadata:", data)
            except Exception as e:
                print(f"Error receiving transcripts: {e}")

        await asyncio.gather(send_audio(), receive_transcripts())
