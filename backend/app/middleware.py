import logging
import os
import time

from fastapi import Request


os.makedirs("logs", exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = round(time.time() - start, 3)

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"status={response.status_code} "
        f"time={duration}s"
    )

    return response