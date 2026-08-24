from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

from app.realtime.hub import hub
from app.utils.jwt import decode_access

router = APIRouter(tags=["Realtime"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str | None = Query(None),
):
    if not token:
        await websocket.close(code=4001, reason="Authentication token required")
        return

    try:
        payload = decode_access(token)
        org_id = payload.get("org")
        if not org_id:
            await websocket.close(code=4001, reason="Invalid token claims")
            return
    except Exception:
        await websocket.close(code=4001, reason="Invalid or expired token")
        return

    await hub.connect(str(org_id), websocket)
    try:
        while True:
            # Keep connection open; receive client pings/messages if any
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        hub.disconnect(str(org_id), websocket)
    except Exception:
        hub.disconnect(str(org_id), websocket)
