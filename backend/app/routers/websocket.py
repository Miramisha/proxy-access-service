import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import VirtualMachine


router = APIRouter(
    tags=["WebSocket"]
)


@router.websocket("/ws/status/{user_id}")
async def connection_status(
    websocket: WebSocket,
    user_id: int
):
    await websocket.accept()

    try:
        while True:
            db: Session = SessionLocal()

            try:
                vm = (
                    db.query(VirtualMachine)
                    .filter(
                        VirtualMachine.current_user_id == user_id
                    )
                    .first()
                )

                if vm:
                    status = {
                        "status": "connected",
                        "vm_id": vm.id,
                        "host": vm.host,
                        "port": vm.port,
                        "protocol": vm.protocol
                    }
                else:
                    status = {
                        "status": "disconnected"
                    }

                await websocket.send_json(status)

            finally:
                db.close()

            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print(
            f"WebSocket disconnected for user {user_id}"
        )