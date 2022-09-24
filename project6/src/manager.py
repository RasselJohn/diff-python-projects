from uuid import uuid4

from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.sessions = {}
        self.active_connections: dict[str, WebSocket] = {}  # {client_id: ws}

    async def connect(self, ws: WebSocket, client_id):
        if client_id in self.active_connections:
            print(f'{client_id=} already exists. Old connection will be closed.')
            await self.active_connections[client_id].close()

        await ws.accept()
        self.active_connections[client_id] = ws

    def disconnect(self, client_id):
        del self.active_connections[client_id]

    async def set_session(self, ws: WebSocket, client_id):
        session_id = str(uuid4())
        self.sessions[client_id] = session_id
        await ws.send_text(f'{session_id}')

        print(f'Session {session_id=} started.')
