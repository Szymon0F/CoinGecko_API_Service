from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from src.database.models import CoinPrice


class CoinPriceService:
    """Service for handling coin price data in the database."""

    @staticmethod
    async def create_coin_prices(
        db: Session, 
        market_data: List[Dict[str, Any]]
    ) -> List[CoinPrice]:
        """
        Create multiple coin price records in the database.

        Args:
            db: Database session
            market_data: List of market data dictionaries

        Returns:
            List of created CoinPrice records
        """
        coin_prices = []
        for data in market_data:
            coin_price = CoinPrice(
                coin_id=data["id"],
                symbol=data["symbol"],
                name=data["name"],
                current_price=data["current_price"],
                market_cap=data["market_cap"],
                market_cap_rank=data["market_cap_rank"],
                total_volume=data["total_volume"],
                price_change_24h=data["price_change_24h"],
                price_change_percentage_24h=data["price_change_percentage_24h"],
                last_updated=datetime.fromisoformat(
                    data["last_updated"].replace("Z", "+00:00")),
                created_at=datetime.now(timezone.utc)
            )
            coin_prices.append(coin_price)

        db.add_all(coin_prices)
        db.commit()
        return coin_prices

    @staticmethod
    async def get_latest_prices(
        db: Session, 
        limit: int = 100
    ) -> List[CoinPrice]:
        """
        Get the latest coin prices from the database.

        Args:
            db: Database session
            limit: Maximum number of records to return

        Returns:
            List of CoinPrice records
        """
        return (
            db.query(CoinPrice)
            .order_by(CoinPrice.created_at.desc())
            .limit(limit)
            .all()
        )
