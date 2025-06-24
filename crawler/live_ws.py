import asyncio
from typing import Set

import websockets


class LiveWebSocket:
    """Simple WebSocket broadcaster for crawler events."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8765) -> None:
        self._host = host
        self._port = port
        self._clients: Set[websockets.WebSocketServerProtocol] = set()
        self._server: websockets.server.Serve | None = None

    async def _handler(self, websocket: websockets.WebSocketServerProtocol, path: str) -> None:
        self._clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self._clients.discard(websocket)

    async def broadcast(self, message: str) -> None:
        if not self._clients:
            return
        await asyncio.gather(*(ws.send(message) for ws in self._clients), return_exceptions=True)

    async def start(self) -> None:
        self._server = await websockets.serve(self._handler, self._host, self._port)

    async def stop(self) -> None:
        if self._server:
            self._server.close()
            await self._server.wait_closed()
