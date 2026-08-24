from collections import defaultdict

from fastapi import WebSocket


class ConnectionHub:
    def __init__(self) -> None:
        self._rooms: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, organization_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self._rooms[organization_id].add(ws)

    def disconnect(self, organization_id: str, ws: WebSocket) -> None:
        self._rooms[organization_id].discard(ws)

    async def broadcast(self, organization_id: str, payload: dict) -> None:
        dead: list[WebSocket] = []
        for ws in list(self._rooms.get(organization_id, ())):
            try:
                await ws.send_json(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self._rooms[organization_id].discard(ws)


hub = ConnectionHub()
