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
CLIENT_LOCAL_PATH = os.path.abspath(__file__)

class TrayClient:
    def __init__(self):
        self.running = True
        self.icon = self.create_icon()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.loop.run_until_complete, args=(self.listen_websocket(),))
        self.thread.daemon = True
        self.register()
        from command_handler import CommandHandler
        from program_downloader import ProgramDownloader

        self.downloader = ProgramDownloader()
        self.command_handler = CommandHandler(self.downloader)

        self.thread.start()

    def create_icon(self):
        # Create a simple icon
        image = Image.new("RGB", (64, 64), "black")
        draw = ImageDraw.Draw(image)
        draw.rectangle((8, 8, 56, 56), fill="green")

        menu = pystray.Menu(
            pystray.MenuItem("Exit", self.exit)
        )

        return pystray.Icon("Moonhard Client", image, "Moonhard Tray Client", menu)

    def exit(self, icon=None, item=None):
        self.running = False
        self.icon.stop()

    def run(self):
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
                        self.command_handler.handle(msg)
                        print(f"📩 Received: {msg}")
            except Exception as e:
                print(f"🔁 Connection error: {e}. Retrying in 5 seconds...")
                time.sleep(5)

# === Run ===
if __name__ == "__main__":
    app = TrayClient()
    app.run()
