from fastapi import (
    FastAPI,
    status,
)
from fastapi.responses import Response
from src.api.coingecko import coingecko_route  # fetch and store
from src.api.database_operations import database_route  # CRUD

app = FastAPI(
    title="CoinGecko",
    version="0.1.0",
)

app.include_router(coingecko_route)  # fetch and store
app.include_router(database_route)  # CRUD


@app.get(
    "/health",
    summary="API health check",
)
def health_check():
    """Returns a 200 response to indicate the API is healthy."""
    return Response(status_code=status.HTTP_200_OK)
