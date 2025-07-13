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
- Poetry (for dependency management)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SupraSummus/burn-tokens.git
cd burn-tokens
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
# or using pip
pip install poetry
```

3. Install dependencies:
```bash
poetry install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
poetry run python app.py
# or activate the virtual environment
poetry shell
python app.py
```

The application will be available at `http://localhost:5000`

### Alternative Installation (Legacy)

If you prefer using pip and requirements.txt:
```bash
pip install -r requirements.txt
python app.py
```

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
Returns the health status of the application.

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
Retrieves a paginated list of **demo** burn operations.

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
Retrieves a specific **demo** burn operation by ID.

#### Get Statistics
```http
GET /api/stats
```
Returns **demo** burn statistics.

**Response:**
```json
{
  "total_burned": 100.5,
  "burn_count": 1,
  "last_burn": "2025-07-08T19:41:47.821144+00:00"
}
```

## Development

### Using Poetry (Recommended)

The project now uses Poetry for dependency management. Use these commands:

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

# Activate Poetry shell (alternative)
poetry shell
pytest tests/ -v
```

### Using Make Commands

The project includes a Makefile for common tasks:

```bash
# Install dependencies
make install

# Run tests
make test

# Run linting
make lint

# Format code
make format

# Run application
make run

# Run all CI checks
make ci
```

### Legacy Development (pip)

If you prefer using pip directly:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Code linting
flake8 app.py tests/ conftest.py

# Code formatting
black app.py tests/ conftest.py
```

### Project Structure
```
burn-tokens/
├── app.py                 # Main Flask application
├── conftest.py           # Test configuration
├── pyproject.toml        # Poetry configuration & dependencies
├── poetry.lock           # Locked dependency versions
├── requirements.txt      # Python dependencies (legacy)
├── .env.example         # Environment variables template
├── setup.cfg            # Tool configuration (migrated to pyproject.toml)
├── Makefile             # Development commands
├── .gitignore          # Git ignore rules
├── templates/
│   └── index.html      # Web interface template
└── tests/
    └── test_app.py     # Application tests
```

## Configuration

### Environment Variables

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

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions and support, please open an issue on GitHub.