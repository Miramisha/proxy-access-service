from datetime import datetime, timedelta

from celery import Celery
from sqlalchemy.orm import Session

from app.config import settings
from app.database import SessionLocal
from app.models import VirtualMachine
from app.email_service import send_email


celery_app = Celery(
    "proxy_access_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


celery_app.conf.beat_schedule = {
    "release-expired-vms": {
        "task": "app.tasks.release_expired_vms",
        "schedule": 60.0,
    }
}


@celery_app.task
def send_activation_key_email(
    email: str,
    activation_key: str
):
    body = f"""
Здравствуйте!

Спасибо за регистрацию в Proxy Access Service.

Ваш ключ активации:

{activation_key}

Используйте этот ключ для подключения
к прокси через desktop-приложение.

С уважением,
Proxy Access Service
"""

    send_email(
        to_email=email,
        subject="Ваш ключ активации",
        body=body
    )

    print(f"Activation key sent to {email}")

    return True


@celery_app.task
def release_expired_vms():
    db: Session = SessionLocal()

    try:
        timeout_time = datetime.utcnow() - timedelta(
            minutes=settings.VM_TIMEOUT_MINUTES
        )

        expired_vms = (
            db.query(VirtualMachine)
            .filter(
                VirtualMachine.current_user_id.isnot(None),
                VirtualMachine.last_used_at <= timeout_time
            )
            .all()
        )

        released = 0

        for vm in expired_vms:
            vm.current_user_id = None
            vm.last_used_at = None
            released += 1

        db.commit()

        print(f"Released expired VMs: {released}")

        return released

    finally:
        db.close()