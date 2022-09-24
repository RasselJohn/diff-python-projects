import logging
import sys

import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.get('/sessions')
async def get_sessions():
    return (' '.join((k, v)) for k, v in manager.sessions.items())


@app.websocket('/')
async def websocket_endpoint(ws: WebSocket, client_id: str):
    await manager.connect(ws, client_id)
    await manager.set_session(ws, client_id)

    try:
        while True:
            data = await ws.receive_text()
            print(f'Server received from {client_id=} message:{data=}')
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        print(f'Session for {client_id=} finished...')


if __name__ == "__main__":
    uvicorn.run("server:app", port=8880, ws_ping_interval=5, ws_ping_timeout=5)
