# audio_stream_client.py
import asyncio
import websockets
from pydub import AudioSegment
# import simpleaudio as sa 
from io import BytesIO

# WAV format params — must match your server audio
SAMPLE_WIDTH = 2
FRAME_RATE = 16000
CHANNELS = 1

# async def play_audio():
#     uri = "ws://localhost:8765"
#     async with websockets.connect(uri) as ws:
#         print("Connected to server, receiving audio...")
#         async for msg in ws:
#             if isinstance(msg, bytes):
#                 # Wrap bytes into a WAV segment
#                 seg = AudioSegment(
#                     data=msg,
#                     sample_width=SAMPLE_WIDTH,
#                     frame_rate=FRAME_RATE,
#                     channels=CHANNELS
#                 )
#                 print("seg.raw_data:", seg.raw_data)
#                 print("seg.channels:", seg.channels)
#                 print("seg.sample_width", seg.sample_width)
#                 print("seg.frame_rate", seg.frame_rate)
#                 # Convert to raw audio and play immediately
#                 # playback = sa.play_buffer( 
#                 #     seg.raw_data,
#                 #     num_channels=seg.channels,
#                 #     bytes_per_sample=seg.sample_width,
#                 #     sample_rate=seg.frame_rate
#                 # )
#                 # playback.wait_done()

# asyncio.run(play_audio())


# async def save_audio_chunks():
#     uri = "ws://localhost:8765"
#     chunk_count = 0

#     async with websockets.connect(uri) as ws:
#         print("Connected to server, receiving audio...")

#         async for msg in ws:
#             if isinstance(msg, bytes):
#                 seg = AudioSegment(
#                     data=msg,
#                     sample_width=SAMPLE_WIDTH,
#                     frame_rate=FRAME_RATE,
#                     channels=CHANNELS
#                 )
#                 # Save each chunk to file
#                 filename = f"chunk_{chunk_count:04d}.wav"
#                 seg.export(filename, format="wav")
#                 print(f"Saved {filename}")
#                 chunk_count += 1

# asyncio.run(save_audio_chunks())





CHUNKS_PER_FILE = 25  # Adjust depending on how fast your server sends chunks

async def save_audio_chunks():
    uri = "ws://localhost:8765"
    chunk_count = 0
    buffer = bytearray()

    async with websockets.connect(uri) as ws:
        print("Connected to server, receiving audio...")

        async for msg in ws:
            if isinstance(msg, bytes):
                buffer.extend(msg)

                # Save after collecting enough data
                if len(buffer) >= CHUNKS_PER_FILE * len(msg):
                    seg = AudioSegment(
                        data=bytes(buffer),
                        sample_width=SAMPLE_WIDTH,
                        frame_rate=FRAME_RATE,
                        channels=CHANNELS
                    )

                    filename = f"data/chunk_{chunk_count:04d}.wav"
                    seg.export(filename, format="wav")
                    print(f"Saved {filename} ({len(buffer)} bytes)")

                    # Reset buffer
                    buffer.clear()
                    chunk_count += 1

asyncio.run(save_audio_chunks())














