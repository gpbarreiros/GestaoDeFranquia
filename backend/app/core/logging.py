import logging
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("gestao_franquias")


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        requestId = str(uuid.uuid4())[:8]
        inicio = time.time()

        logger.info(
            f"[{requestId}] {request.method} {request.url.path} "
            f"| IP: {request.client.host if request.client else 'unknown'}"
        )

        response = await call_next(request)

        duracao = round((time.time() - inicio) * 1000, 2)
        logger.info(
            f"[{requestId}] {request.method} {request.url.path} "
            f"| STATUS: {response.status_code} | {duracao}ms"
        )

        return response