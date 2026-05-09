"""
tests/test_health.py - Health check endpoints
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "service" in response.json()


def test_metrics_endpoint():
    """Test metrics endpoint returns 200."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "uptime_seconds" in response.json()
    assert "total_requests" in response.json()


def test_root_endpoint():
    """Test root endpoint returns application info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "SmartTax Assist API"
    assert data["status"] == "running"
