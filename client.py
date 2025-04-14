import asyncio
import websockets
import platform
import psutil
import json

async def listen():
    uri = "ws://your-render-url/ws"  # Will change to actual Render address
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            if message == "get_status":
                status = {
                    "platform": platform.system(),
                    "cpu_percent": psutil.cpu_percent(),
                    "memory": psutil.virtual_memory().percent
                }
                await websocket.send(json.dumps(status))

asyncio.run(listen())
