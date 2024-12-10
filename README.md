# Data Processing and API Project

This project implements a data processing pipeline that fetches data from external APIs, processes it using modern data manipulation libraries, and exposes the results through a REST API.

## Features

### Core Features
- ✅ **Poetry Package Management**: Dependencies management and virtual environment using Poetry
- ✅ **External API Integration**: Connects to public APIs for data fetching
- ✅ **Data Processing**: Uses Polars/Pandas for efficient data manipulation
- ✅ **Database Storage**: PostgreSQL database integration using SQLAlchemy ORM
- ✅ **REST API**: CRUD operations for data access and manipulation
- ✅ **Type Safety**: Python type annotations throughout the codebase
- ✅ **Data Validation**: Request/Response validation using Pydantic

### Additional Features
- ✅ **Docker Support**: Containerized application with Docker and Docker Compose
- ✅ **Testing**: Comprehensive test suite using Pytest
- ✅ **Documentation**: Auto-generated documentation using MkDocs with Material theme
- ✅ **Code Quality**: Linting and type checking implementation
- ✅ **CI/CD Pipeline**: Automated testing and deployment workflow

## Installation

### Using Poetry
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

### Getting Started
1. Clone the repository
2. Open in VS Code with Dev Containers
3. Run `poetry install` in the terminal
4. Start the services: `docker-compose up`

### API Documentation
  Swagger UI: http://localhost:8000/docs
  ReDoc: http://localhost:8000/redoc

## API Endpoints
- GET /health - Health check
- GET /coingecko/markets - Fetch market data
- GET /coingecko/ping - Check CoinGecko API status
- GET /coingecko/stored-data - Get stored data
- POST /db/coins - Create coin record
- GET /db/coins/{coin_id} - Get specific coin
- PUT /db/coins/{coin_id} - Update coin record
- DELETE /db/coins/{coin_id} - Delete coin record

### MKDocs
  http://localhost:8080

## Development

### Testing
Run tests with: `docker-compose exec api poetry run pytest`

### Generating Documentation
poetry run mkdocs serve

### Code Quality Checks
  poetry run flake8

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To set up pre-commit:

1. Install pre-commit:
```bash
poetry add pre-commit --dev

2. Install the pre-commit hooks:
pre-commit install

3. Run pre-commit hooks on all files:
pre-commit run --all-files