import uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

from src.manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.get('/sessions')
async def get_sessions() -> list:
    sessions = await manager.get_all_sessions()
    return sessions


@app.websocket('/')
async def websocket_endpoint(ws: WebSocket, client_id: str):
    session: str = await manager.get_session(client_id)
    await ws.accept()
    await ws.send_text(session)

    try:
        while True:
            data: str = await ws.receive_text()
            is_actual_session: bool = await manager.is_active_session(client_id, session)
            if not is_actual_session:
                await ws.close()
                break

            print(f'Server received from {client_id=} message:{data=}')

    except WebSocketDisconnect:
        print(f'Ws connection closed.')

    finally:
        await manager.clean(client_id, session)


# for testing
if __name__ == "__main__":
    uvicorn.run("server:app", port=8880, ws_ping_interval=5, ws_ping_timeout=5)
