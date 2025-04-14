import asyncio
import threading
import socket
import time
import platform
import psutil
import json
import os
import requests
import websockets
from PIL import Image, ImageDraw
import pystray

SERVER_URL = "https://moonhardapi.onrender.com"
AUTH_TOKEN = "479a263f74007327498f24925a9ce0ae"
CLIENT_ID = socket.gethostname()

class TrayClient:
    def __init__(self):
        self.running = True
        self.icon = self.create_icon()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_until_complete, args=(self.listen_websocket(),))
        self.thread.daemon = True

    def create_icon(self):
        # Create a simple icon
        image = Image.new("RGB", (64, 64), "black")
        draw = ImageDraw.Draw(image)
        draw.rectangle((8, 8, 56, 56), fill="green")

        menu = pystray.Menu(
            pystray.MenuItem("Start", self.start),
            pystray.MenuItem("Stop", self.stop),
            pystray.MenuItem("Exit", self.exit)
        )

        return pystray.Icon("Moonhard Client", image, "Moonhard Tray Client", menu)

    def start(self, icon=None, item=None):
        if not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self.loop.run_until_complete, args=(self.listen_websocket(),))
            self.thread.daemon = True
            self.thread.start()

    def stop(self, icon=None, item=None):
        self.running = False

    def exit(self, icon=None, item=None):
        self.running = False
        self.icon.stop()

    def run(self):
        self.register()
        self.icon.run()

    def register(self):
        try:
            url = f"{SERVER_URL}/register/{CLIENT_ID}?token={AUTH_TOKEN}"
            response = requests.post(url)
            print("✅ Registered:", response.json())
        except Exception as e:
            print("❌ Registration failed:", e)

    async def listen_websocket(self):
        uri = f"{SERVER_URL.replace('https', 'wss')}/ws/{CLIENT_ID}?token={AUTH_TOKEN}"
        while self.running:
            try:
                async with websockets.connect(uri) as websocket:
                    print("🔌 Connected to server")
                    while self.running:
                        msg = await websocket.recv()
                        if msg == "get_status":
                            await websocket.send(json.dumps(self.get_status()))
            except Exception as e:
                print(f"🔁 Connection error: {e}. Retrying in 5 seconds...")
                time.sleep(5)

    def get_status(self):
        disk = psutil.disk_usage('/')
        uptime = time.time() - psutil.boot_time()
        return {
            "client_id": CLIENT_ID,
            "hostname": socket.gethostname(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_percent": psutil.virtual_memory().percent,
            "disk_percent": disk.percent,
            "uptime_minutes": round(uptime / 60, 2)
        }

# === Run ===
if __name__ == "__main__":
    app = TrayClient()
    app.run()
