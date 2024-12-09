# CoinGecko API Service

## Features
- Real-time cryptocurrency data fetching from CoinGecko API
- Data transformation using Polars
- PostgreSQL database storage
- RESTful API with CRUD operations
- Structured logging
- Request tracking with unique IDs
- Docker containerization
- Development environment with VS Code Dev Containers

## Development Setup

### Prerequisites
- Docker Desktop
- Visual Studio Code
- Dev Containers extension

### Getting Started
1. Clone the repository
2. Open in VS Code with Dev Containers
3. Run `poetry install` in the terminal
4. Start the services: `docker-compose up`

### API Documentation
Access the Swagger UI at `http://localhost:8000/docs`

### Testing
Run tests with: `poetry run pytest`

## API Endpoints
- GET /health - Health check
- GET /coingecko/markets - Fetch market data
- GET /coingecko/ping - Check CoinGecko API status
- GET /coingecko/stored-data - Get stored data
- POST /db/coins - Create coin record
- GET /db/coins/{coin_id} - Get specific coin
- PUT /db/coins/{coin_id} - Update coin record
- DELETE /db/coins/{coin_id} - Delete coin record

## Documentation
- API Reference: https://szymon0f.github.io/coingecko-api-service/api/endpoints
- Development Guide: https://szymon0f.github.io/coingecko-api-service/development/setup

## Code Quality
- Black for formatting
- Ruff for linting
- MyPy for type checking
- Pre-commit hooks for consistency

## CI/CD
- Automated tests on push/PR
- Code quality checks
- Documentation deployment