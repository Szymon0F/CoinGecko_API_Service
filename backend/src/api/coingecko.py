# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import httpx
from fastapi import APIRouter, HTTPException
from src.models import BaseResponse
from src.models import (
    CoinMarketData,
    MarketDataRequest,
    MarketDataResponse,
    ErrorResponse
)
from src.reporting.coingecko_reporter import ReporterSingleton

# Create router with prefix and tags
coingecko_route = APIRouter(
    prefix="/coingecko",
    tags=["CoinGecko Operations"],
)

# Constants
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


@coingecko_route.get(
    "/markets",
    summary="Get cryptocurrency market data",
    response_model=MarketDataResponse,
    responses={
        503: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def get_market_data(
    vs_currency: str = "usd",
    page: int = 1,
    per_page: int = 100,
    sparkline: bool = False
):
    """
    Get current cryptocurrency market data from CoinGecko.

    Args:
        vs_currency: The target currency (e.g., usd, eur)
        page: Page number for pagination
        per_page: Number of results per page
        sparkline: Include sparkline data

    Returns:
        MarketDataResponse: List of cryptocurrency market data
    """
    reporter = ReporterSingleton().get_instance()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{COINGECKO_API_URL}/coins/markets",
                params={
                    "vs_currency": vs_currency,
                    "per_page": per_page,
                    "page": page,
                    "sparkline": sparkline,
                    "order": "market_cap_desc"
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

            market_data = [CoinMarketData(**coin) for coin in data]
            return MarketDataResponse(
                data=market_data,
                total_count=len(market_data),
                page=page,
                per_page=per_page
            )

    except httpx.HTTPError as e:
        reporter.on_error(
            "Error fetching market data from CoinGecko",
            cause=e,
            stack=None,
            details={"vs_currency": vs_currency, "page": page}
        )
        raise HTTPException(
            status_code=503,
            detail=ErrorResponse(
                message="CoinGecko API service unavailable",
                details={"error": str(e)}
            ).model_dump()
        )
    except Exception as e:
        reporter.on_error(
            "Unexpected error fetching market data",
            cause=e,
            stack=None,
            details={"vs_currency": vs_currency, "page": page}
        )
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                message="Internal server error",
                details={"error": str(e)}
            ).model_dump()
        )


@coingecko_route.get(
    "/ping",
    summary="Check CoinGecko API status",
    response_model=BaseResponse,
    responses={503: {"model": ErrorResponse}}
)
async def check_api_status():
    """Check if the CoinGecko API is operational."""
    reporter = ReporterSingleton().get_instance()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{COINGECKO_API_URL}/ping")
            response.raise_for_status()
            return BaseResponse(status="CoinGecko API is operational")

    except Exception as e:
        reporter.on_error(
            "Error checking CoinGecko API status",
            cause=e,
            stack=None
        )
        raise HTTPException(
            status_code=503,
            detail=ErrorResponse(
                message="CoinGecko API is not available",
                details={"error": str(e)}
            ).model_dump()
        )
