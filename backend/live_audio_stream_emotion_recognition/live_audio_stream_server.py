import asyncio, websockets, wave

async def stream_audio(websocket):
    try:
        with wave.open("sample.wav", "rb") as wf:
            chunk = 1024
            data = wf.readframes(chunk)
            while data:
                await websocket.send(data)
                await asyncio.sleep(0.05)
                data = wf.readframes(chunk)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected — stopping stream.")
    except Exception as e:
        print(f"Server error: {e}")

async def main(): # I increase ping_interval, ping_timeout to prevent server crash when client slows
    async with websockets.serve(stream_audio, "localhost", 8765, ping_interval=120, ping_timeout=90, max_size=None):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())

