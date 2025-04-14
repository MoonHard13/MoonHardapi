from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Dict
from datetime import datetime
from fastapi import Body
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
    return [
        {
            "client_id": cid,
            "last_seen": info["last_seen"].isoformat(),
            "connected": info["websocket"] is not None
        }
        for cid, info in connected_clients.items()
    ]

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, token: str = Query(...)):
    check_token(token)
    await websocket.accept()
    connected_clients[client_id]["websocket"] = websocket
    connected_clients[client_id]["last_seen"] = datetime.utcnow()

    print(f"🟢 WebSocket connected: {client_id}")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 {client_id}: {data}")
            connected_clients[client_id]["last_seen"] = datetime.utcnow()
    except WebSocketDisconnect:
        print(f"🔴 {client_id} disconnected")
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
async def broadcast_command(
    token: str = Query(...),
    command: str = Query(None),
    body: dict = Body(None)
):
    check_token(token)
    cmd = command or (body.get("command") if body else None)
    if not cmd:
        raise HTTPException(status_code=400, detail="Command is required")

    sent = 0
    for cid, client in connected_clients.items():
        if client["websocket"]:
            try:
                await client["websocket"].send_text(cmd)
                sent += 1
            except:
                continue
    return {"message": f"📡 Sent '{cmd}' to {sent} clients"}

