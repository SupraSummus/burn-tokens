"""
Database models for the burn tokens application.
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Float, Integer, String, Text

db = SQLAlchemy()


class BurnRecord(db.Model):
    """Model for storing token burn records."""

    __tablename__ = "burn_records"

    id = db.Column(Integer, primary_key=True)
    token_address = db.Column(String(42), nullable=False)
    amount = db.Column(Float, nullable=False)
    reason = db.Column(Text)
    timestamp = db.Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    tx_hash = db.Column(String(66), nullable=False)

    def to_dict(self):
        """Convert the model to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "token_address": self.token_address,
            "amount": self.amount,
            "reason": self.reason,
            "timestamp": self.timestamp.isoformat(),
            "tx_hash": self.tx_hash,
        }
