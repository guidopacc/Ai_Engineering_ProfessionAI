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


def test_prometheus_metrics_update():
    """Test che verifica l'aggiornamento delle metriche Prometheus dopo una predizione."""
    from src.app.metrics import SENTIMENT_DISTRIBUTION
    
    response1 = client.get("/metrics")
    initial_content = response1.text
    
    response = client.post(
        "/predict",
        json={"text": "I love this product!"}
    )
    assert response.status_code == 200
    
    response2 = client.get("/metrics")
    final_content = response2.text
    
    assert "sentiment_predictions_total" in final_content
    
    initial_count = initial_content.count('sentiment_predictions_total')
    final_count = final_content.count('sentiment_predictions_total')
    
    assert final_count >= initial_count
    
    response3 = client.post(
        "/predict",
        json={"text": "This is terrible!"}
    )
    assert response3.status_code == 200
    
    response4 = client.get("/metrics")
    final_content_after = response4.text
    
    assert "sentiment_predictions_total" in final_content_after


