from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    activation_key: str | None = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class VirtualMachineCreate(BaseModel):
    name: str
    host: str
    port: int
    protocol: str


class VirtualMachineResponse(BaseModel):
    id: int
    name: str
    host: str
    port: int
    protocol: str
    is_active: bool
    current_user_id: int | None = None

    class Config:
        from_attributes = True

class ActivationKeyRequest(BaseModel):
    activation_key: str


class ActivationResponse(BaseModel):
    message: str
    vm_id: int
    host: str
    port: int
    protocol: str


class RefreshKeyResponse(BaseModel):
    message: str
    activation_key: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    new_password_confirm: str
