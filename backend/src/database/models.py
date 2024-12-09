from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CoinPrice(Base):
    """Model for storing cryptocurrency price data."""

    __tablename__ = "coin_prices"

    id = Column(Integer, primary_key=True)
    coin_id = Column(String, nullable=False, index=True)
    symbol = Column(String, nullable=False)
    name = Column(String, nullable=False)
    current_price = Column(Float)
    market_cap = Column(Float)
    market_cap_rank = Column(Integer)
    total_volume = Column(Float)
    price_change_24h = Column(Float)
    price_change_percentage_24h = Column(Float)
    market_dominance = Column(Float)
    volume_to_market_cap_ratio = Column(Float)
    last_updated = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now(
        timezone.utc), nullable=False)

    # Create indexes for common queries
    __table_args__ = (
        Index('idx_coin_price_date', 'coin_id', 'created_at'),
        Index('idx_market_cap_rank', 'market_cap_rank'),
    )

    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": self.id,
            "coin_id": self.coin_id,
            "symbol": self.symbol,
            "name": self.name,
            "current_price": self.current_price,
            "market_cap": self.market_cap,
            "market_cap_rank": self.market_cap_rank,
            "total_volume": self.total_volume,
            "price_change_24h": self.price_change_24h,
            "price_change_percentage_24h": self.price_change_percentage_24h,
            "market_dominance": self.market_dominance,
            "volume_to_market_cap_ratio": self.volume_to_market_cap_ratio,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
