from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import User, VirtualMachine
from app.routers import auth, users, vms, keys
from app.routers import health
from app.middleware import log_requests
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.routers import websocket
from app.limiter import limiter

from fastapi import HTTPException

from app.exceptions import (
    http_exception_handler,
    generic_exception_handler
)

app = FastAPI(
    title="Proxy Access Service",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.middleware("http")(log_requests)

@app.on_event("startup")
def startup():

    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(vms.router)
app.include_router(keys.router)
app.include_router(health.router)

@app.get("/")
def root():

    return {"message": "Backend works"}