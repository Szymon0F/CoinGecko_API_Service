# API Overview

The CoinGecko API Service provides a RESTful interface for accessing cryptocurrency data.

## Base URL
http://localhost:8000

## Authentication

Currently, the API does not require authentication.

## Response Format

All responses are returned in JSON format:

```json
{
    "data": {
        // Response data
    },
    "status": "success",
    "timestamp": "2024-02-20T12:00:00Z"
}

{
    "error": {
        "code": "ERROR_CODE",
        "message": "Error description",
        "details": {}
    },
    "status": "error",
    "timestamp": "2024-02-20T12:00:00Z"
}