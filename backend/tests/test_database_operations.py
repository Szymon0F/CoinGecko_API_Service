import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timezone
from src.api.database_operations import CoinPriceCreate, CoinPriceUpdate


def test_create_coin_price(client, db_session):
    test_data = {
        "coin_id": "test-coin",
        "symbol": "TEST",
        "name": "Test Coin",
        "current_price": 100.0,
        "market_cap": 1000000.0,
        "market_cap_rank": 1,
        "total_volume": 50000.0,
        "price_change_24h": 5.0,
        "price_change_percentage_24h": 5.0,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

    response = client.post("/db/coins", json=test_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Record created successfully"


def test_read_coin_price(client, db_session):
    # First create a record
    test_data = {
        "coin_id": "test-coin",
        "symbol": "TEST",
        "name": "Test Coin",
        "current_price": 100.0,
        "market_cap": 1000000.0,
        "market_cap_rank": 1,
        "total_volume": 50000.0,
        "price_change_24h": 5.0,
        "price_change_percentage_24h": 5.0,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    client.post("/db/coins", json=test_data)

    response = client.get("/db/coins/test-coin")
    assert response.status_code == 200
    assert response.json()["coin_id"] == "test-coin"


def test_update_coin_price(client, db_session):
    # First create a record
    test_data = {
        "coin_id": "test-coin",
        "symbol": "TEST",
        "name": "Test Coin",
        "current_price": 100.0,
        "market_cap": 1000000.0,
        "market_cap_rank": 1,
        "total_volume": 50000.0,
        "price_change_24h": 5.0,
        "price_change_percentage_24h": 5.0,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    client.post("/db/coins", json=test_data)

    update_data = {
        "current_price": 150.0,
        "price_change_24h": 50.0
    }
    response = client.put("/db/coins/test-coin", json=update_data)
    assert response.status_code == 200
    assert response.json()["data"]["current_price"] == 150.0


def test_delete_coin_price(client, db_session):
    # First create a record
    test_data = {
        "coin_id": "test-coin",
        "symbol": "TEST",
        "name": "Test Coin",
        "current_price": 100.0,
        "market_cap": 1000000.0,
        "market_cap_rank": 1,
        "total_volume": 50000.0,
        "price_change_24h": 5.0,
        "price_change_percentage_24h": 5.0,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }
    client.post("/db/coins", json=test_data)

    response = client.delete("/db/coins/test-coin")
    assert response.status_code == 200
    assert response.json()["message"] == "Record deleted successfully"

    # Verify deletion
    get_response = client.get("/db/coins/test-coin")
    assert get_response.status_code == 404
