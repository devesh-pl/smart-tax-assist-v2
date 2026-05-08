"""MongoDB connection and database utilities."""
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from typing import Optional

# Global database instance
_db_client: Optional[MongoClient] = None
_database = None

def init_db(mongodb_url: str) -> None:
    """Initialize MongoDB connection.
    
    Args:
        mongodb_url: MongoDB connection string
    """
    global _db_client, _database
    try:
        _db_client = MongoClient(
            mongodb_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
        )
        # Test connection
        _db_client.admin.command('ping')
        _database = _db_client['smart_tax_assist']
        print("✓ MongoDB connection established")
    except ServerSelectionTimeoutError:
        print("✗ Failed to connect to MongoDB")
        raise

def get_database():
    """Get the database instance."""
    if _database is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _database

def close_db() -> None:
    """Close MongoDB connection."""
    global _db_client
    if _db_client:
        _db_client.close()
        print("✓ MongoDB connection closed")

def get_collection(collection_name: str):
    """Get a collection from the database.
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        MongoDB collection instance
    """
    db = get_database()
    return db[collection_name]

# Collection references
def get_users_collection():
    """Get users collection."""
    return get_collection('users')

def get_expenses_collection():
    """Get expenses collection."""
    return get_collection('expenses')

def get_categories_collection():
    """Get categories collection."""
    return get_collection('categories')
