"""
Test configuration and fixtures for the burn tokens application.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["DEBUG"] = False

    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def sample_burn_data():
    """Sample data for testing burn operations."""
    return {
        "token_address": "0x1234567890123456789012345678901234567890",
        "amount": 100.0,
        "reason": "Test burn operation",
    }
