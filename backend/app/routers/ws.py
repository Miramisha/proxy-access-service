from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import VirtualMachine
from app.websocket import manager


router = APIRouter(tags=["WebSocket"])


def _current_status(user_id: int) -> dict:
    db: Session = SessionLocal()
    try:
        vm = (
            db.query(VirtualMachine)
            .filter(VirtualMachine.current_user_id == user_id)
            .first()
        )
        if vm:
            return {
                "status": "connected",
                "vm_id": vm.id,
                "host": vm.host,
                "port": vm.port,
                "protocol": vm.protocol,
            }
        return {"status": "disconnected"}
    finally:
        db.close()


@router.websocket("/ws/connection-status/{user_id}/")
async def connection_status(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        await websocket.send_json(_current_status(user_id))
        while True:
            # Ping/poll-friendly endpoint: any client message receives fresh status.
            await websocket.receive_text()
            await websocket.send_json(_current_status(user_id))
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
