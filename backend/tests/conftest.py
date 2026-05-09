"""
tests/conftest.py - Pytest configuration and fixtures
"""
import pytest
import os
from dotenv import load_dotenv

# Load test environment
load_dotenv()


@pytest.fixture
def test_jwt_secret():
    """Provide test JWT secret."""
    return "test-secret-key-for-testing"


@pytest.fixture
def test_mongodb_url():
    """Provide test MongoDB URL."""
    return os.getenv("MONGODB_URL", "mongodb://localhost:27017/smart_tax_assist_test")
