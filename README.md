# 🔥 Burn Tokens

**Note: The name "burn-tokens" is a joke about AI coding this project - referring to the LLM tokens consumed during development, not cryptocurrency tokens!**

A demo Python web application built with Flask. This is a placeholder/demonstration project while the actual functionality is still being decided. The current "token burning" interface is just for demonstration purposes and has no relation to cryptocurrency or blockchain operations.

![Burn Tokens Interface](https://github.com/user-attachments/assets/67fd4007-2e61-452a-89f8-6f1cee1edbf6)

## Features

**This is a demo application with placeholder functionality:**

- **Web Interface**: Beautiful, responsive UI for demonstration purposes
- **REST API**: Full RESTful API for testing and development
- **Statistics Dashboard**: Demo statistics and history tracking
- **Comprehensive Testing**: Full test suite with pytest
- **Code Quality**: Linting with flake8 and formatting with black

- **Documentation**: Comprehensive API documentation

## Quick Start

### Prerequisites

- Python 3.12+
- Poetry

### Installation

```bash
git clone https://github.com/SupraSummus/burn-tokens.git
cd burn-tokens
poetry install
cp .env.example .env
poetry run python app.py
```

The application will be available at `http://localhost:5000`

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-08T19:41:32.489906+00:00",
  "version": "1.0.0"
}
```

#### Burn Tokens
```http
POST /api/burn
```
**Demo endpoint** - simulates burning tokens and records the transaction.

**Request Body:**
```json
{
  "token_address": "0x1234567890123456789012345678901234567890",
  "amount": 100.5,
  "reason": "Manual burn operation"
}
```

**Response:**
```json
{
  "success": true,
  "burn_id": 1,
  "tx_hash": "0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f",
  "message": "Successfully burned 100.5 tokens"
}
```

#### Get Burns
```http
GET /api/burns?page=1&limit=10
```

**Response:**
```json
{
  "burns": [
    {
      "id": 1,
      "token_address": "0x1234567890123456789012345678901234567890",
      "amount": 100.5,
      "reason": "Manual burn operation",
      "timestamp": "2025-07-08T19:41:47.821144+00:00",
      "tx_hash": "0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "has_next": false
}
```

#### Get Burn by ID
```http
GET /api/burns/{burn_id}
```

#### Get Statistics
```http
GET /api/stats
```

**Response:**
```json
{
  "total_burned": 100.5,
  "burn_count": 1,
  "last_burn": "2025-07-08T19:41:47.821144+00:00"
}
```

## Development

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest tests/ -v

# Code linting
poetry run flake8 app.py tests/ conftest.py

# Code formatting
poetry run black app.py tests/ conftest.py

# Run the application
poetry run python app.py
```

## Configuration

- `DEBUG`: Enable debug mode (default: false)
- `SECRET_KEY`: Flask secret key for sessions
- `PORT`: Application port (default: 5000)

### Future Enhancements

**Note: The actual functionality of this project is still being decided. Current "token burning" features are placeholders.**

- Database integration (PostgreSQL/SQLite)
- ~~Blockchain integration for real token burning~~ (Not crypto-related!)
- User authentication and authorization
- Advanced analytics and reporting
- API rate limiting
- WebSocket support for real-time updates

## Contributing

Run tests and linting before submitting changes.

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions and support, please open an issue on GitHub.