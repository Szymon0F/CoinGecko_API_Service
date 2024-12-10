# API Endpoints

## Health Check
`GET /health`

Health check endpoint to verify API is running.

**Response**: 200 OK

## CoinGecko Routes

### Get Market Data
`GET /coingecko/markets`

Fetch current cryptocurrency market data from CoinGecko.

**Parameters:**
- `vs_currency` (string): The target currency (e.g., "usd")
- `page` (integer): Page number for pagination
- `per_page` (integer): Number of results per page

### Check CoinGecko Status
`GET /coingecko/ping`

Check if the CoinGecko API is available.

### Get Stored Data
`GET /coingecko/stored-data`

Retrieve cryptocurrency data stored in the local database.

## Database Operations

### Create Coin
`POST /db/coins`

Create a new coin record in the database.

### Get Coin
`GET /db/coins/{coin_id}`

Retrieve a specific coin's data.

**Parameters:**
- `coin_id` (string): The unique identifier of the coin

### Update Coin
`PUT /db/coins/{coin_id}`

Update an existing coin record.

**Parameters:**
- `coin_id` (string): The unique identifier of the coin

### Delete Coin
`DELETE /db/coins/{coin_id}`

Delete a coin record from the database.

**Parameters:**
- `coin_id` (string): The unique identifier of the coin