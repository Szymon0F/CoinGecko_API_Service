from datetime import datetime, timezone
import polars as pl
from typing import List, Dict, Any


class MarketDataTransformer:
    """Transformer class for CoinGecko market data using Polars."""

    @staticmethod
    def transform_market_data(raw_data: List[Dict[str, Any]]) -> pl.DataFrame:
        """
        Transform raw market data into a Polars DataFrame with necessary calculations.

        Args:
            raw_data: List of dictionaries containing market data from CoinGecko API

        Returns:
            pl.DataFrame: Transformed market data
        """
        # Convert to Polars DataFrame
        df = pl.DataFrame(raw_data)

        # Ensure all required columns are present
        required_columns = [
            "id", "symbol", "name", "current_price", "market_cap",
            "market_cap_rank", "total_volume", "price_change_24h",
            "price_change_percentage_24h", "last_updated"
        ]

        # Add missing columns with null values if they don't exist
        for col in required_columns:
            if col not in df.columns:
                df = df.with_columns(pl.lit(None).alias(col))

        # Convert last_updated to datetime
        df = df.with_columns([
            pl.col("current_price").cast(pl.Float64),
            pl.col("market_cap").cast(pl.Float64),
            pl.col("total_volume").cast(pl.Float64),
            pl.col("price_change_24h").cast(pl.Float64),
            pl.col("price_change_percentage_24h").cast(pl.Float64),
        ])

        if "last_updated" in df.columns:
            df = df.with_columns([
                pl.col("last_updated").cast(pl.Utf8)
            ])

        # Add additional calculated columns
        df = df.with_columns([
            # Calculate market dominance (market cap / total market cap)
            (pl.col("market_cap") / pl.col("market_cap").sum() * 100)
            .alias("market_dominance"),

            # Calculate volume to market cap ratio
            (pl.col("total_volume") / pl.col("market_cap"))
            .alias("volume_to_market_cap_ratio"),

            # Add timestamp for when the transformation occurred
            pl.lit(datetime.now(timezone.utc).isoformat()).alias("processed_at")
        ])

        # Select and order final columns
        final_columns = [
            "id", "symbol", "name", "current_price", "market_cap",
            "market_cap_rank", "total_volume", "price_change_24h",
            "price_change_percentage_24h", "market_dominance",
            "volume_to_market_cap_ratio", "last_updated", "processed_at"
        ]

        return df.select(final_columns)

    @ staticmethod
    def get_market_summary(df: pl.DataFrame) -> Dict[str, Any]:
        """
        Generate market summary statistics from the transformed data.

        Args:
            df: Transformed market data DataFrame

        Returns:
            Dict containing market summary statistics
        """
        return {
            "total_market_cap": df["market_cap"].sum(),
            "total_volume_24h": df["total_volume"].sum(),
            "avg_price_change_24h": df["price_change_percentage_24h"].mean(),
            "num_cryptocurrencies": len(df),
            "top_gainers": df.filter(
                pl.col("price_change_percentage_24h") > 0
            ).sort("price_change_percentage_24h", descending=True)
            .select(["symbol", "price_change_percentage_24h"])
            .head(5).to_dicts(),
            "top_losers": df.filter(
                pl.col("price_change_percentage_24h") < 0
            ).sort("price_change_percentage_24h")
            .select(["symbol", "price_change_percentage_24h"])
            .head(5).to_dicts(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
