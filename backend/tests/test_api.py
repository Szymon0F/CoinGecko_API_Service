import pytest
from fastapi.testclient import TestClient


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_get_market_data(client, mocker):
    # Mock the CoinGecko API response
    mock_response = {
        "data": [
            {
                "id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin",
                "current_price": 50000,
                "market_cap": 1000000000000,
                "market_cap_rank": 1,
                "total_volume": 50000000000,
                "price_change_24h": 1000,
                "price_change_percentage_24h": 2.5,
                "last_updated": "2024-02-20T12:00:00Z"
            }
        ]
    }

    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)

    response = client.get("/coingecko/markets")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0
