from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, VirtualMachine
from app.auth import get_current_user


router = APIRouter(
    prefix="/api/keys",
    tags=["Keys"]
)


@router.post("/activate")
def activate_key(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    vm = (
        db.query(VirtualMachine)
        .filter(VirtualMachine.current_user_id == None)
        .first()
    )

    if not vm:
        raise HTTPException(
            status_code=404,
            detail="No free virtual machines"
        )

    vm.current_user_id = current_user.id

    db.commit()

    return {
        "message": "VM assigned",
        "vm_id": vm.id,
        "host": vm.host,
        "port": vm.port
    }

@router.post("/deactivate")
def deactivate_key(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    vm = (
        db.query(VirtualMachine)
        .filter(VirtualMachine.current_user_id == current_user.id)
        .first()
    )

    if not vm:
        raise HTTPException(
            status_code=404,
            detail="No active VM for this user"
        )

    vm.current_user_id = None
    vm.last_used_at = None

    db.commit()

    return {
        "message": "VM released",
        "vm_id": vm.id
    }