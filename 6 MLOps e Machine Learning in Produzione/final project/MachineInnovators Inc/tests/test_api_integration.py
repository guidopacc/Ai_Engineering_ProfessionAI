"""
Test di integrazione per API FastAPI.
"""
import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_predict_endpoint():
    """Test endpoint /predict."""
    response = client.post(
        "/predict",
        json={"text": "I love this product!"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "score" in data
    assert data["label"] in ["negative", "neutral", "positive"]
    assert 0.0 <= data["score"] <= 1.0


def test_predict_endpoint_invalid():
    """Test endpoint /predict con input non valido."""
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422
    
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_batch_endpoint():
    """Test endpoint /predict/batch."""
    response = client.post(
        "/predict/batch",
        json={"texts": ["I love it!", "This is bad.", "It's okay."]}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 3
    
    for pred in data["predictions"]:
        assert "label" in pred
        assert "score" in pred
        assert pred["label"] in ["negative", "neutral", "positive"]
        assert 0.0 <= pred["score"] <= 1.0


def test_predict_batch_endpoint_empty():
    """Test endpoint /predict/batch con lista vuota."""
    response = client.post("/predict/batch", json={"texts": []})
    assert response.status_code == 422


def test_metrics_endpoint():
    """Test endpoint /metrics."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"
    content = response.text
    assert "fastapi_requests_total" in content or len(content) > 0


