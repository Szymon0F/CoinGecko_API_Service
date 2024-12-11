from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CoinPriceCreate(BaseModel):
    coin_id: str
    symbol: str
    name: str
    current_price: float
    market_cap: float
    market_cap_rank: int
    total_volume: float
    price_change_24h: float
    price_change_percentage_24h: float
    market_dominance: Optional[float] = None
    volume_to_market_cap_ratio: Optional[float] = None
    last_updated: datetime

class CoinPriceUpdate(BaseModel):
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    market_cap_rank: Optional[int] = None
    total_volume: Optional[float] = None
    price_change_24h: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    market_dominance: Optional[float] = None
    volume_to_market_cap_ratio: Optional[float] = None
    last_updated: Optional[datetime] = None
