# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import httpx
from fastapi import APIRouter, HTTPException, Depends
from src.models import BaseResponse
from src.models import (
    CoinMarketData,
    MarketDataRequest,
    MarketDataResponse,
    ErrorResponse
)
from src.reporting.coingecko_reporter import ReporterSingleton
from src.transformers.market_data import MarketDataTransformer
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.database.services import CoinPriceService
from datetime import datetime
import time

# Create router with prefix and tags
coingecko_route = APIRouter(
    prefix="/coingecko",
    tags=["CoinGecko Operations"],
)

# Constants
COINGECKO_API_URL = os.getenv("COINGECKO_API_URL")


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
    sparkline: bool = False,
    db: Session = Depends(get_db)
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
    start_time = time.time()

    try:
        # Log the request
        reporter.on_request(
            endpoint="/coins/markets",
            params={"vs_currency": vs_currency,
                    "page": page, "per_page": per_page}
        )

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
            raw_data = response.json()

            # Transform data using Polars
            transformer = MarketDataTransformer()
            df = transformer.transform_market_data(raw_data)

            market_data = [
                CoinMarketData(**record)
                for record in df.to_dicts()
            ]
            
            # store the data
            try:
                await CoinPriceService.create_coin_prices(db, raw_data)
            except Exception as e:
                reporter.on_error(
                    "Error storing market data in database",
                    cause=e,
                    stack=None
                )
            
            # Log the response
            reporter.on_response(
                endpoint="/coins/markets",
                status_code=response.status_code,
                response_time=time.time() - start_time
            )

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


@coingecko_route.get("/stored-data")
async def get_stored_data(db: Session = Depends(get_db)):
    """Get the latest stored cryptocurrency data"""
    latest_prices = await CoinPriceService.get_latest_prices(db, limit=10)
    return {
        "count": len(latest_prices),
        "latest_update": latest_prices[0].created_at if latest_prices else None,
        "data": [price.to_dict() for price in latest_prices]
    }
