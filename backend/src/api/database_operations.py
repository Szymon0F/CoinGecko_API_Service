from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from src.database.session import get_db
from src.database.models import CoinPrice
from src.schemas import CoinPriceCreate, CoinPriceUpdate

database_route = APIRouter(
    prefix="/db",
    tags=["Database Operations"]
)

@database_route.post("/coins")
def create_coin_price(
    coin_data: CoinPriceCreate,
    db: Session = Depends(get_db)
):
    db_coin = CoinPrice(
        coin_id=coin_data.coin_id,
        symbol=coin_data.symbol,
        name=coin_data.name,
        current_price=coin_data.current_price,
        market_cap=coin_data.market_cap,
        market_cap_rank=coin_data.market_cap_rank,
        total_volume=coin_data.total_volume,
        price_change_24h=coin_data.price_change_24h,
        price_change_percentage_24h=coin_data.price_change_percentage_24h,
        market_dominance=coin_data.market_dominance,
        volume_to_market_cap_ratio=coin_data.volume_to_market_cap_ratio,
        last_updated=coin_data.last_updated
    )
    db.add(db_coin)
    db.commit()
    db.refresh(db_coin)
    return {"message": "Record created successfully", "data": db_coin.to_dict()}

@database_route.get("/coins/{coin_id}")
def read_coin_price(coin_id: str, db: Session = Depends(get_db)):
    db_coin = db.query(CoinPrice).filter(CoinPrice.coin_id == coin_id).first()
    if db_coin is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    return db_coin.to_dict()

@database_route.put("/coins/{coin_id}")
def update_coin_price(
    coin_id: str,
    coin_data: CoinPriceUpdate,
    db: Session = Depends(get_db)
):
    db_coin = db.query(CoinPrice).filter(CoinPrice.coin_id == coin_id).first()
    if db_coin is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    
    update_data = coin_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_coin, key, value)
    
    db.commit()
    db.refresh(db_coin)
    return {"message": "Record updated successfully", "data": db_coin.to_dict()}

@database_route.delete("/coins/{coin_id}")
def delete_coin_price(coin_id: str, db: Session = Depends(get_db)):
    db_coin = db.query(CoinPrice).filter(CoinPrice.coin_id == coin_id).first()
    if db_coin is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    
    db.delete(db_coin)
    db.commit()
    return {"message": "Record deleted successfully"}
