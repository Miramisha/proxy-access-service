from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import VirtualMachine
from app.schemas import VirtualMachineCreate, VirtualMachineResponse
from app.auth import get_current_user


router = APIRouter(
    prefix="/api/vms",
    tags=["Virtual Machines"]
)


@router.post("/", response_model=VirtualMachineResponse)
def create_vm(
    vm_data: VirtualMachineCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    vm = VirtualMachine(
        name=vm_data.name,
        host=vm_data.host,
        port=vm_data.port,
        protocol=vm_data.protocol,
        is_active=True
    )

    db.add(vm)
    db.commit()
    db.refresh(vm)

    return vm


@router.get("/", response_model=list[VirtualMachineResponse])
def get_vms(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return db.query(VirtualMachine).all()