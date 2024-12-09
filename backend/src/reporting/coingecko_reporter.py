from datetime import datetime
from typing import Any, Dict, Optional
import logging
import traceback


class CoinGeckoReporter:
    """Reporter class for CoinGecko API operations."""

    def __init__(self):
        self.logger = logging.getLogger("coingecko_reporter")
        self._configure_logger()

    def _configure_logger(self):
        """Configure the logger with appropriate handlers and formatting."""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Set logging level
        self.logger.setLevel(logging.INFO)

    def on_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        message: str = "API request initiated"
    ):
        """
        Log API request details.

        Args:
            endpoint: The API endpoint being called
            params: Request parameters
            message: Optional custom message
        """
        self.logger.info(
            f"CoinGecko API Request - {message}",
            extra={
                "endpoint": endpoint,
                "parameters": params,
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    def on_response(
        self,
        endpoint: str,
        status_code: int,
        response_time: float,
        message: str = "API request completed"
    ):
        """
        Log API response details.

        Args:
            endpoint: The API endpoint called
            status_code: HTTP status code received
            response_time: Time taken for the request in seconds
            message: Optional custom message
        """
        self.logger.info(
            f"CoinGecko API Response - {message}",
            extra={
                "endpoint": endpoint,
                "status_code": status_code,
                "response_time": f"{response_time:.2f}s",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

    def on_error(
        self,
        message: str,
        cause: Optional[Exception] = None,
        stack: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Log error details.

        Args:
            message: Error message
            cause: Exception that caused the error
            stack: Stack trace
            details: Additional error details
        """
        error_info = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": type(cause).__name__ if cause else None,
            "error_message": str(cause) if cause else None,
            "stack_trace": stack or (traceback.format_exc() if cause else None),
            "details": details or {}
        }

        self.logger.error(
            f"CoinGecko API Error - {message}",
            extra=error_info
        )


class ReporterSingleton:
    """Singleton pattern for the CoinGecko reporter."""

    _instance = None

    @classmethod
    def get_instance(cls) -> CoinGeckoReporter:
        """Get or create the reporter instance."""
        if cls._instance is None:
            cls._instance = CoinGeckoReporter()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset the reporter instance (useful for testing)."""
        cls._instance = None
