from fastapi import Request
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
from typing import Callable
from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add request ID to each request."""

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Add request_id to logging context
        logger_adapter = logging.LoggerAdapter(
            logger, {"request_id": request_id}
        )

        # Log request
        logger_adapter.info(
            f"Incoming {request.method} request to {request.url.path}",
            extra={"path": request.url.path, "method": request.method}
        )

        # Track request timing
        start_time = time.time()

        response = await call_next(request)

        # Calculate request duration
        duration = time.time() - start_time

        # Log response
        logger_adapter.info(
            f"Request completed in {duration:.3f}s",
            extra={
                "duration": duration,
                "status_code": response.status_code
            }
        )

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        return response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle and log errors."""

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            return await call_next(request)
        except Exception as e:
            logger.exception(
                "Unhandled exception",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "error": str(e)
                }
            )
            raise
