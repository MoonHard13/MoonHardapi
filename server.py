import logging
from logging.handlers import TimedRotatingFileHandler
import os

# === Δημιουργία φακέλου logs ===
os.makedirs("logs", exist_ok=True)

# === Ρύθμιση log handler ===
log_path = os.path.join("logs", "moonhard.log")
log_handler = TimedRotatingFileHandler(log_path, when="midnight", backupCount=7, encoding="utf-8")
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
log_handler.setFormatter(formatter)

logger = logging.getLogger("moonhard")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict
from datetime import datetime
import asyncio
import json

app = FastAPI()
AUTH_TOKEN = "479a263f74007327498f24925a9ce0ae"
connected_clients: Dict[str, Dict] = {}

# === Έλεγχος token ===
def check_token(token: str):
    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/register/{client_id}")
async def register(client_id: str, token: str = Query(...)):
    check_token(token)
    connected_clients[client_id] = {
        "websocket": None,
        "last_seen": datetime.utcnow()
    }
    return {"message": f"{client_id} registered"}

@app.get("/status")
async def get_status():
    results = []
    for cid, info in connected_clients.items():
        result = {
            "client_id": cid,
            "last_seen": info["last_seen"].isoformat(),
            "connected": info["websocket"] is not None,
            "last_message": info.get("last_message", ""),
            "cpu": info.get("cpu"),
            "ram": info.get("ram"),
            "disk": info.get("disk")
        }
        results.append(result)
    return results

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, token: str = Query(...)):
    check_token(token)
    await websocket.accept()
    if client_id not in connected_clients:
        connected_clients[client_id] = {}
        logger.info(f"ℹ️ Auto-registered {client_id} on WebSocket connect.")
    connected_clients[client_id]["websocket"] = websocket
    connected_clients[client_id]["last_seen"] = datetime.utcnow()

    logger.info(f"🟢 WebSocket connected: {client_id}")
    try:
        while True:
            try:
                message = await websocket.receive_text()
                print(f"📨 {client_id} → {message}")
                connected_clients[client_id]["last_message"] = message
                try:
                    data = json.loads(message)
                    if isinstance(data, dict):
                        connected_clients[client_id].update({
                            "cpu": data.get("cpu"),
                            "ram": data.get("ram"),
                            "disk": data.get("disk")
                        })
                except json.JSONDecodeError:
                    pass
            except Exception as e:
                print(f"⚠️ Error receiving from {client_id}: {e}")
                break
    except Exception as outer_e:
        logger.error(f"⚠️ Unexpected error in WebSocket loop for {client_id}: {outer_e}")
    finally:
        logger.info(f"🔴 WebSocket disconnected: {client_id}")
        if client_id in connected_clients:
            connected_clients[client_id]["websocket"] = None

@app.post("/send/{client_id}")
async def send_command(client_id: str, command: str, token: str = Query(...)):
    check_token(token)
    client = connected_clients.get(client_id)
    if not client or not client["websocket"]:
        return JSONResponse(status_code=404, content={"error": "Client not connected"})

    try:
        await client["websocket"].send_text(command)
        return {"message": f"✅ Command sent to {client_id}"}
    except:
        return JSONResponse(status_code=500, content={"error": "Failed to send command"})

@app.post("/broadcast")
async def broadcast_command(command: str, token: str = Query(...)):
    check_token(token)
    sent = 0
    for cid, client in connected_clients.items():
        if client["websocket"]:
            try:
                await client["websocket"].send_text(command)
                sent += 1
            except:
                continue
    return {"message": f"📡 Sent '{command}' to {sent} clients"}
