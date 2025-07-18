"""
Test database migrations and setup.
"""

import tempfile
import os
from sqlalchemy import create_engine, text
from models import db, BurnRecord


def test_database_migration():
    """Test that database schema is created correctly."""
    # Create a temporary database
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    
    try:
        # Create engine and test table creation
        engine = create_engine(database_url)
        
        # Create all tables using our models
        with engine.begin() as conn:
            db.metadata.create_all(bind=conn)
            
            # Verify the table exists and has correct columns
            result = conn.execute(text("PRAGMA table_info(burn_records)"))
            columns = {row[1]: row[2] for row in result.fetchall()}
            
            expected_columns = {
                'id': 'INTEGER',
                'token_address': 'VARCHAR(42)',
                'amount': 'FLOAT',
                'reason': 'TEXT',
                'timestamp': 'DATETIME',
                'tx_hash': 'VARCHAR(66)'
            }
            
            for col_name, col_type in expected_columns.items():
                assert col_name in columns, f"Column {col_name} missing"
                assert col_type in columns[col_name], f"Column {col_name} has wrong type: {columns[col_name]}"
                
    finally:
        os.close(db_fd)
        os.unlink(db_path)


def test_burn_record_model():
    """Test the BurnRecord model directly."""
    # Create a temporary database
    db_fd, db_path = tempfile.mkstemp()
    database_url = f"sqlite:///{db_path}"
    
    try:
        from app import app
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['TESTING'] = True
        
        with app.app_context():
            db.create_all()
            
            # Create a burn record
            burn = BurnRecord(
                token_address="0x1234567890123456789012345678901234567890",
                amount=100.0,
                reason="Test burn",
                tx_hash="0xabcdef1234567890"
            )
            
            db.session.add(burn)
            db.session.commit()
            
            # Query it back
            retrieved = db.session.query(BurnRecord).first()
            assert retrieved.token_address == "0x1234567890123456789012345678901234567890"
            assert retrieved.amount == 100.0
            assert retrieved.reason == "Test burn"
            assert retrieved.tx_hash == "0xabcdef1234567890"
            assert retrieved.timestamp is not None
            
            # Test to_dict method
            data = retrieved.to_dict()
            assert data['id'] == retrieved.id
            assert data['token_address'] == retrieved.token_address
            assert data['amount'] == retrieved.amount
            assert data['reason'] == retrieved.reason
            assert data['tx_hash'] == retrieved.tx_hash
            assert 'timestamp' in data
            
    finally:
        os.close(db_fd)
        os.unlink(db_path)