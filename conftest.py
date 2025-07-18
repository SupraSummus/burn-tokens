"""
Test configuration and fixtures for the burn tokens application.
"""

import pytest
import tempfile
import os
from app import app
from models import db


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    # Create a temporary database for testing
    db_fd, temp_db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{temp_db_path}"
    app.config["TESTING"] = True
    app.config["DEBUG"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

    os.close(db_fd)
    os.unlink(temp_db_path)


@pytest.fixture
def sample_burn_data():
    """Sample data for testing burn operations."""
    return {
        "token_address": "0x1234567890123456789012345678901234567890",
        "amount": 100.0,
        "reason": "Test burn operation",
    }
