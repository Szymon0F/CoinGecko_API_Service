import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_get_market_data(client):
    # Create a mock response
    mock_data = [
        {
            "coin_id": "test-coin",
            "symbol": "TEST",
            "name": "Test Coin",
            "current_price": 100.0,
            "market_cap": 1000000.0,
            "market_cap_rank": 1,
            "total_volume": 50000.0,
            "price_change_24h": 5.0,
            "price_change_percentage_24h": 5.0,
            "market_dominance": 0.0,
            "volume_to_market_cap_ratio": 0.0,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
    ]

    with pytest.MonkeyPatch().context() as m:
        # Mock the external API call
        m.setattr("src.api.coingecko.coingecko_route", lambda: mock_data)
        
        # Make request to your endpoint
        response = client.get("/coingecko/markets")
        
        # Assert response
        assert response.status_code == 200
        assert "data" in response.json()