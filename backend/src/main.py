from fastapi import (
    FastAPI,
    status,
)
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from src.api.coingecko import coingecko_route  # fetch and store
from src.api.database_operations import database_route  # CRUD
from src.core.middleware import RequestIDMiddleware, ErrorHandlerMiddleware
from src.core.logging import setup_logging
from src.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="CoinGecko",
    version="0.1.0",
    debug=settings.DEBUG,
    description="""
    A service that integrates with CoinGecko API to fetch, store, and manage cryptocurrency data.
    
    Features:
    - Fetch real-time cryptocurrency market data
    - Store data in PostgreSQL database
    - Perform CRUD operations on stored data
    - Data transformation using Polars
    """,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(ErrorHandlerMiddleware)

app.include_router(coingecko_route)  # fetch and store
app.include_router(database_route)  # CRUD


@app.get(
    "/health",
    summary="API health check",
)
def health_check():
    """Returns a 200 response to indicate the API is healthy."""
    return Response(status_code=status.HTTP_200_OK)
