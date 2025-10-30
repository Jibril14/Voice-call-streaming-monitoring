import asyncio
import websockets
from pydub import AudioSegment
from io import BytesIO
# from audio_stream_realtime_classify import classify_emotion
from audio_diarize import audio_diarize
from sentiment_analysis import get_emotions
import os

SAMPLE_WIDTH = 2
FRAME_RATE = 16000
CHANNELS = 1

# Number of chunks to accumulate before processing, # high generally dont timeout stream server
CHUNKS_PER_FILE = 100 # change this if you want e.g 50 gave 3sec chunk 

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


async def save_audio_chunks():
    uri = "ws://localhost:8765"
    chunk_count = 0
    buffer = bytearray()

    async with websockets.connect(uri, ping_interval=10, ping_timeout=200) as ws:
        print("Connected to server, receiving audio...")

        async for msg in ws:
            if isinstance(msg, bytes):
                buffer.extend(msg)

                # Process when 25 chunks collected
                if len(buffer) >= CHUNKS_PER_FILE * len(msg):

                    audio_segment = AudioSegment(
                        data=bytes(buffer),
                        sample_width=SAMPLE_WIDTH,
                        frame_rate=FRAME_RATE,
                        channels=CHANNELS,
                    )

                    filename = f"{OUTPUT_DIR}/chunk_{chunk_count:04d}.wav"
                    audio_segment.export(filename, format="wav")

                    print("filename:", filename)
                    try:
                        transcript = audio_diarize(filename)
                        emotion = get_emotions(transcript)
                        print("TTY:", emotion)
                    except Exception as e:
                        print(f"Error classifying {filename}: {e}")
                    # try:
                    #     result = classify_emotion(filename)
                    #     label = result.get("predicted_label", "unknown")
                    #     confidence = result.get("confidence", "unknown")

                    #     print(f"\nSaved {filename} ({len(buffer)} bytes)")
                    #     print(f"Predicted Emotion: {label} (Confidence: {confidence:.3f})")

                    # except Exception as e:
                    #     print(f"Error classifying {filename}: {e}")

                    buffer.clear()
                    chunk_count += 1


if __name__ == "__main__":
    asyncio.run(save_audio_chunks())
