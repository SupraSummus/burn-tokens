"""
Tests for the burn tokens web application.
"""

import json
from app import burned_tokens, burn_stats


class TestBurnTokensApp:
    """Test suite for the burn tokens application."""

    def setup_method(self):
        """Reset state before each test."""
        burned_tokens.clear()
        burn_stats.update({"total_burned": 0, "burn_count": 0, "last_burn": None})

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"

    def test_index_page(self, client):
        """Test the main index page loads."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Burn Tokens" in response.data

    def test_burn_tokens_success(self, client, sample_burn_data):
        """Test successful token burning."""
        response = client.post(
            "/api/burn",
            data=json.dumps(sample_burn_data),
            content_type="application/json",
        )

        assert response.status_code == 201

        data = json.loads(response.data)
        assert data["success"] is True
        assert "burn_id" in data
        assert "tx_hash" in data
        assert "Successfully burned" in data["message"]

        # Check that burn was recorded
        assert len(burned_tokens) == 1
        assert burned_tokens[0]["amount"] == sample_burn_data["amount"]
        assert burned_tokens[0]["token_address"] == sample_burn_data["token_address"]

    def test_burn_tokens_missing_data(self, client):
        """Test burn endpoint with missing data."""
        response = client.post(
            "/api/burn", data=json.dumps({}), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "No data provided" in data["error"]

    def test_burn_tokens_invalid_amount(self, client):
        """Test burn endpoint with invalid amount."""
        burn_data = {
            "token_address": "0x1234567890123456789012345678901234567890",
            "amount": -100,
        }

        response = client.post(
            "/api/burn", data=json.dumps(burn_data), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "Valid amount is required" in data["error"]

    def test_get_burns_empty(self, client):
        """Test getting burns when list is empty."""
        response = client.get("/api/burns")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["burns"] == []
        assert data["total"] == 0
        assert data["page"] == 1

    def test_get_burns_with_data(self, client, sample_burn_data):
        """Test getting burns with existing data."""
        # First create a burn
        client.post(
            "/api/burn",
            data=json.dumps(sample_burn_data),
            content_type="application/json",
        )

        # Then retrieve burns
        response = client.get("/api/burns")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data["burns"]) == 1
        assert data["total"] == 1
        assert data["burns"][0]["amount"] == sample_burn_data["amount"]

    def test_get_burn_by_id(self, client, sample_burn_data):
        """Test getting a specific burn by ID."""
        # Create a burn first
        burn_response = client.post(
            "/api/burn",
            data=json.dumps(sample_burn_data),
            content_type="application/json",
        )
        burn_id = json.loads(burn_response.data)["burn_id"]

        # Get the burn by ID
        response = client.get(f"/api/burns/{burn_id}")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["id"] == burn_id
        assert data["amount"] == sample_burn_data["amount"]
        assert data["token_address"] == sample_burn_data["token_address"]

    def test_get_burn_not_found(self, client):
        """Test getting a non-existent burn."""
        response = client.get("/api/burns/999")
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "Burn record not found" in data["error"]

    def test_get_stats(self, client, sample_burn_data):
        """Test getting burn statistics."""
        # Initially empty stats
        response = client.get("/api/stats")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert data["total_burned"] == 0
        assert data["burn_count"] == 0
        assert data["last_burn"] is None

        # Create a burn
        client.post(
            "/api/burn",
            data=json.dumps(sample_burn_data),
            content_type="application/json",
        )

        # Check updated stats
        response = client.get("/api/stats")
        data = json.loads(response.data)
        assert data["total_burned"] == sample_burn_data["amount"]
        assert data["burn_count"] == 1
        assert data["last_burn"] is not None

    def test_burns_pagination(self, client, sample_burn_data):
        """Test pagination for burns endpoint."""
        # Create multiple burns
        for i in range(5):
            burn_data = sample_burn_data.copy()
            burn_data["amount"] = i + 1
            client.post(
                "/api/burn", data=json.dumps(burn_data), content_type="application/json"
            )

        # Test pagination
        response = client.get("/api/burns?page=1&limit=3")
        assert response.status_code == 200

        data = json.loads(response.data)
        assert len(data["burns"]) == 3
        assert data["total"] == 5
        assert data["has_next"] is True

    def test_404_error_handler(self, client):
        """Test 404 error handler."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

        data = json.loads(response.data)
        assert "Endpoint not found" in data["error"]
