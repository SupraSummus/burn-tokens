"""
Burn Tokens Demo Web Application

A Flask-based demo web application. The name "burn-tokens" refers to LLM tokens
consumed during AI-assisted development, not cryptocurrency tokens!

This is a placeholder/demonstration application while actual functionality is
being decided. Current "token burning" features are for demo purposes only and
have no relation to cryptocurrency.
"""

import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import func
from models import db, BurnRecord

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config["DEBUG"] = os.getenv("DEBUG", "False").lower() == "true"
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)

# Database configuration
database_url = os.getenv("DATABASE_URL", "sqlite:///burn_tokens.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


def get_burn_stats():
    """Calculate burn statistics from database."""
    total_burned = db.session.query(func.sum(BurnRecord.amount)).scalar() or 0
    burn_count = db.session.query(func.count(BurnRecord.id)).scalar() or 0
    last_burn_record = db.session.query(BurnRecord).order_by(
        BurnRecord.timestamp.desc()
    ).first()
    last_burn = last_burn_record.timestamp.isoformat() if last_burn_record else None

    return {
        "total_burned": float(total_burned),
        "burn_count": burn_count,
        "last_burn": last_burn
    }


@app.route("/")
def index():
    """Main page showing demo burn statistics and interface."""
    stats = get_burn_stats()
    return render_template("index.html", stats=stats)


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
    """Demo burn tokens endpoint - simulates token burning for demonstration."""
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

        # Generate demo transaction hash
        tx_hash = f"0x{''.join(['%02x' % (i % 256) for i in range(32)])}"

        # Create burn record
        burn_record = BurnRecord(
            token_address=token_address,
            amount=float(amount),
            reason=reason,
            tx_hash=tx_hash
        )

        # Save to database
        db.session.add(burn_record)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "burn_id": burn_record.id,
                    "tx_hash": burn_record.tx_hash,
                    "message": f"Successfully burned {amount} tokens",
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/burns")
def get_burns():
    """Get list of all demo token burns."""
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    # Query with pagination
    pagination = db.session.query(BurnRecord).order_by(
        BurnRecord.timestamp.desc()
    ).paginate(page=page, per_page=limit, error_out=False)

    burns = [burn.to_dict() for burn in pagination.items]

    return jsonify(
        {
            "burns": burns,
            "total": pagination.total,
            "page": page,
            "limit": limit,
            "has_next": pagination.has_next,
        }
    )


@app.route("/api/burns/<int:burn_id>")
def get_burn(burn_id):
    """Get specific demo burn record by ID."""
    burn = db.session.query(BurnRecord).filter_by(id=burn_id).first()

    if not burn:
        return jsonify({"error": "Burn record not found"}), 404

    return jsonify(burn.to_dict())


@app.route("/api/stats")
def get_stats():
    """Get demo burn statistics."""
    return jsonify(get_burn_stats())


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
