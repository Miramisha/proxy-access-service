from fastapi import FastAPI

from app.database import Base, engine
from app.models import User, VirtualMachine
from app.routers import auth, users, vms, keys


app = FastAPI(
    title="Proxy Access Service",
    version="1.0"
)


@app.on_event("startup")
def startup():

    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(vms.router)
app.include_router(keys.router)

@app.get("/")
def root():

    return {"message": "Backend works"}