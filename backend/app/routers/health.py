from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import text

from app.database import SessionLocal


router = APIRouter(
    prefix="/api/health",
    tags=["Health"]
)


@router.get("/")
def health_check():

    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
            "time": datetime.utcnow()
        }

    except Exception as e:

        return {
            "status": "error",
            "database": str(e)
        }

    finally:
        db.close()