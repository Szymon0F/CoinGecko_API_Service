# Data Models

## CoinPrice
Database model for cryptocurrency price data.

Fields:
- id: Integer (primary key)
- coin_id: String
- symbol: String
- name: String
- current_price: Float
[... other fields ...]

## MarketData
API response model for market data.

Fields:
- data: List[CoinMarketData]
- total_count: Integer
- page: Integer
- per_page: Integer