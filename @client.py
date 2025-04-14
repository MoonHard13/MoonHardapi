import asyncio
import platform
import psutil
import json
import socket
import websockets
import requests

# === Ρυθμίσεις πελάτη ===
SERVER_URL = "https://moonhardapi.onrender.com"
AUTH_TOKEN = "479a263f74007327498f24925a9ce0ae"
CLIENT_ID = socket.gethostname()  # ή κάτι custom

async def listen_websocket():
    uri = f"{SERVER_URL.replace('https', 'wss')}/ws/{CLIENT_ID}?token={AUTH_TOKEN}"

    async with websockets.connect(uri) as websocket:
        while True:
            msg = await websocket.recv()

            if msg == "get_status":
                status = {
                    "client_id": CLIENT_ID,
                    "platform": platform.system(),
                    "cpu": psutil.cpu_percent(),
                    "ram": psutil.virtual_memory().percent
                }
                await websocket.send(json.dumps(status))

def register_client():
    url = f"{SERVER_URL}/register/{CLIENT_ID}?token={AUTH_TOKEN}"
    try:
        response = requests.post(url)
        print("✅ Registered:", response.json())
    except Exception as e:
        print("❌ Failed to register:", e)

if __name__ == "__main__":
    register_client()
    asyncio.run(listen_websocket())
