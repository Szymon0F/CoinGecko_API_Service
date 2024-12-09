from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.database.models import CoinPrice
from src.database.services import CoinPriceService
from typing import List
from datetime import datetime
from pydantic import BaseModel

# Create router for database operations
database_route = APIRouter(
    prefix="/db",
    tags=["Database Operations"],
)


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
    last_updated: datetime


class CoinPriceUpdate(BaseModel):
    current_price: float | None = None
    market_cap: float | None = None
    market_cap_rank: int | None = None
    total_volume: float | None = None
    price_change_24h: float | None = None
    price_change_percentage_24h: float | None = None


@database_route.post("/coins", response_model=dict)
async def create_coin_price(coin_data: CoinPriceCreate, db: Session = Depends(get_db)):
    """Create a new coin price record"""
    try:
        coin_price = await CoinPriceService.create_coin_prices(db, [coin_data.model_dump()])
        return {"message": "Record created successfully", "data": coin_price[0].to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@database_route.get("/coins/{coin_id}", response_model=dict)
async def read_coin_price(coin_id: str, db: Session = Depends(get_db)):
    """Read a specific coin price record"""
    coin = db.query(CoinPrice).filter(CoinPrice.coin_id == coin_id).first()
    if not coin:
        raise HTTPException(status_code=404, detail="Coin not found")
    return coin.to_dict()


@database_route.put("/coins/{coin_id}", response_model=dict)
async def update_coin_price(
    coin_id: str,
    coin_data: CoinPriceUpdate,
    db: Session = Depends(get_db)
):
    """Update a coin price record"""
    coin = db.query(CoinPrice).filter(CoinPrice.coin_id == coin_id).first()
    if not coin:
        raise HTTPException(status_code=404, detail="Coin not found")

    update_data = coin_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(coin, key, value)

    try:
        db.commit()
        db.refresh(coin)
        return {"message": "Record updated successfully", "data": coin.to_dict()}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@database_route.delete("/coins/{coin_id}")
async def delete_coin_price(coin_id: str, db: Session = Depends(get_db)):
    """Delete a coin price record"""
    coin = db.query(CoinPrice).filter(CoinPrice.coin_id == coin_id).first()
    if not coin:
        raise HTTPException(status_code=404, detail="Coin not found")

    try:
        db.delete(coin)
        db.commit()
        return {"message": "Record deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
