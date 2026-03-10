"""
Test per health check endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test che /health restituisce 200 e informazioni del modello."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
    assert "model_loaded" in data
    assert "model_name" in data
    assert data["model_name"] != "" and data["model_name"] is not None
    assert isinstance(data["model_loaded"], bool)


