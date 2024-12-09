from typing import List, Optional
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    status: str = Field(..., description="Status of the API response")


class CoinMarketData(BaseModel):
    id: str = Field(..., description="Coin identifier (e.g., 'bitcoin')")
    symbol: str = Field(..., description="Coin symbol (e.g., 'btc')")
    name: str = Field(..., description="Coin name (e.g., 'Bitcoin')")
    current_price: float = Field(...,
                                 description="Current price in specified currency")
    market_cap: float = Field(..., description="Market capitalization")
    market_cap_rank: int = Field(..., description="Market cap rank")
    total_volume: float = Field(..., description="24h trading volume")
    price_change_24h: Optional[float] = Field(
        None, description="24h price change")
    price_change_percentage_24h: Optional[float] = Field(
        None, description="24h price change percentage")
    last_updated: str = Field(..., description="Last update timestamp")


class MarketDataRequest(BaseModel):
    vs_currency: str = Field(
        default="usd",
        description="Target currency (e.g., usd, eur)"
    )
    per_page: int = Field(
        default=100,
        ge=1,
        le=250,
        description="Results per page"
    )
    page: int = Field(
        default=1,
        ge=1,
        description="Page number"
    )
    sparkline: bool = Field(
        default=False,
        description="Include sparkline data"
    )


class MarketDataResponse(BaseModel):
    data: List[CoinMarketData]
    total_count: int
    page: int
    per_page: int


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Optional[dict] = None
