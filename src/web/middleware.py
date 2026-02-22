import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars

from src.share.core.logger import get_logger


logger = get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        bind_contextvars(request_id = request_id)
        
        try:
            response = await call_next(request)
        finally:
            clear_contextvars()
        
        return response
    