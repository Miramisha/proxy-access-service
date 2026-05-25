from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token
from app.auth import hash_password
from app.auth import verify_password

from app.database import get_db
from app.models import User

from app.schemas import UserRegister
from app.schemas import UserLogin
from app.schemas import TokenResponse

from app.tasks import send_activation_key_email
from app.utils import generate_activation_key


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register_user(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    if data.password != data.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    activation_key = generate_activation_key()

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        is_active=False,
        activation_key=activation_key,
        activation_key_expires=datetime.utcnow() + timedelta(hours=24)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    send_activation_key_email.delay(
        user.email,
        user.activation_key
    )

    return {
        "message":
            "Registration successful. Activation key sent to email."
    }


@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    data: UserLogin,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not activated"
        )

    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }