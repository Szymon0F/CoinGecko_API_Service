import logging
import sys
from typing import Any, Dict
import json
from .config import get_settings

settings = get_settings()


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_object: Dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "environment": settings.ENVIRONMENT
        }

        if hasattr(record, "request_id"):
            log_object["request_id"] = record.request_id

        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_object)


def setup_logging() -> None:
    """Configure application logging."""
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Remove existing handlers
    logger.handlers = []

    # Console handler with JSON formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)

    # Disable default uvicorn access logger
    logging.getLogger("uvicorn.access").handlers = []

    # Log initial configuration
    logger.info(
        "Logging configured",
        extra={
            "environment": settings.ENVIRONMENT,
            "log_level": settings.LOG_LEVEL
        }
    )
