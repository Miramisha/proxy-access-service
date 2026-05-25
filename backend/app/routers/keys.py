from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import generate_activation_key, get_current_user
from app.database import get_db
from app.models import User, VirtualMachine
from app.schemas import ActivationKeyRequest, ActivationResponse, RefreshKeyResponse
from app.tasks import send_activation_key_email

router = APIRouter(
    prefix="/api/keys",
    tags=["Keys"]
)


@router.post("/refresh", response_model=RefreshKeyResponse)
def refresh_key(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.activation_key = generate_activation_key()

    db.commit()
    db.refresh(current_user)

    send_activation_key_email.delay(
        current_user.email,
        current_user.activation_key
)

    return {
        "message": "Activation key refreshed",
        "activation_key": current_user.activation_key
    }


@router.post("/activate", response_model=ActivationResponse)
def activate_key(
    key_data: ActivationKeyRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.activation_key == key_data.activation_key)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid activation key"
        )

    vm = (
        db.query(VirtualMachine)
        .filter(
            VirtualMachine.current_user_id == None,
            VirtualMachine.is_active == True
        )
        .first()
    )

    if not vm:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="All proxy servers are busy"
        )

    vm.current_user_id = user.id
    vm.last_used_at = datetime.utcnow()

    user.is_active = True
    user.activation_key = None

    db.commit()
    db.refresh(vm)

    return {
        "message": "VM assigned",
        "vm_id": vm.id,
        "host": vm.host,
        "port": vm.port,
        "protocol": vm.protocol
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active VM for this user"
        )

    vm.current_user_id = None
    vm.last_used_at = None

    db.commit()

    return {
        "message": "VM released",
        "vm_id": vm.id
    }