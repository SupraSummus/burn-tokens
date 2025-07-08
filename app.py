"""
Burn Tokens Web Application

A Flask-based web application for managing token burning operations.
"""

import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config["DEBUG"] = os.getenv("DEBUG", "False").lower() == "true"
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)

# In-memory storage for demo purposes (use database in production)
burned_tokens = []
burn_stats = {"total_burned": 0, "burn_count": 0, "last_burn": None}


@app.route("/")
def index():
    """Main page showing burn statistics and interface."""
    return render_template("index.html", stats=burn_stats)


@app.route("/api/health")
def health_check():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
        }
    )


@app.route("/api/burn", methods=["POST"])
def burn_tokens():
    """Burn tokens endpoint."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        token_address = data.get("token_address")
        amount = data.get("amount")
        reason = data.get("reason", "Manual burn")

        if not token_address:
            return jsonify({"error": "token_address is required"}), 400

        if not amount or amount <= 0:
            return jsonify({"error": "Valid amount is required"}), 400

        # Create burn record
        burn_record = {
            "id": len(burned_tokens) + 1,
            "token_address": token_address,
            "amount": float(amount),
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tx_hash": f"0x{''.join(['%02x' % (i % 256) for i in range(32)])}"
        }

        # Store the burn record
        burned_tokens.append(burn_record)

        # Update statistics
        burn_stats["total_burned"] += burn_record["amount"]
        burn_stats["burn_count"] += 1
        burn_stats["last_burn"] = burn_record["timestamp"]

        return (
            jsonify(
                {
                    "success": True,
                    "burn_id": burn_record["id"],
                    "tx_hash": burn_record["tx_hash"],
                    "message": f"Successfully burned {amount} tokens",
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/burns")
def get_burns():
    """Get list of all token burns."""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    # Simple pagination
    start = (page - 1) * limit
    end = start + limit

    paginated_burns = burned_tokens[start:end]

    return jsonify(
        {
            "burns": paginated_burns,
            "total": len(burned_tokens),
            "page": page,
            "limit": limit,
            "has_next": end < len(burned_tokens),
        }
    )


@app.route("/api/burns/<int:burn_id>")
def get_burn(burn_id):
    """Get specific burn record by ID."""
    burn = next((b for b in burned_tokens if b["id"] == burn_id), None)

    if not burn:
        return jsonify({"error": "Burn record not found"}), 404

    return jsonify(burn)


@app.route("/api/stats")
def get_stats():
    """Get burn statistics."""
    return jsonify(burn_stats)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
