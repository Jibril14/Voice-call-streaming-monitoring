# server.py
import asyncio, websockets, wave

async def stream_audio(websocket):
    with wave.open("sample.wav", "rb") as wf:
        chunk = 1024
        data = wf.readframes(chunk)
        while data:
            await websocket.send(data)
            await asyncio.sleep(0.05)
            data = wf.readframes(chunk)

async def main():
    async with websockets.serve(stream_audio, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())


