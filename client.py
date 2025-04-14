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
                import time

                disk_usage = psutil.disk_usage('/')
                boot_time = psutil.boot_time()
                uptime = time.time() - boot_time

                status = {
                    "client_id": CLIENT_ID,
                    "hostname": socket.gethostname(),
                    "ip_address": socket.gethostbyname(socket.gethostname()),
                    "platform": platform.platform(),
                    "cpu_percent": psutil.cpu_percent(interval=1),
                    "ram_percent": psutil.virtual_memory().percent,
                    "disk_percent": disk_usage.percent,
                    "uptime_minutes": round(uptime / 60, 2)
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
