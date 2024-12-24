from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ..utils import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(room_id: str, websocket: WebSocket):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Text: {data}", room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast("Human left the chat", room_id)
