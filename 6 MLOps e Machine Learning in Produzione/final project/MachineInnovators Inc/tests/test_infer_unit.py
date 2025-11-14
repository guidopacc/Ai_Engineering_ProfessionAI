"""
Test unitari per funzioni di inferenza.
"""
import pytest
from src.app.infer import predict_one, predict_batch
from src.app.schemas import Prediction


def test_predict_one_positive():
    """Test predizione per testo positivo."""
    text = "I love this product! It's amazing!"
    result = predict_one(text)
    
    assert isinstance(result, Prediction)
    assert result.label in ["negative", "neutral", "positive"]
    assert 0.0 <= result.score <= 1.0


def test_predict_one_negative():
    """Test predizione per testo negativo."""
    text = "This is terrible. I'm very disappointed."
    result = predict_one(text)
    
    assert isinstance(result, Prediction)
    assert result.label in ["negative", "neutral", "positive"]
    assert 0.0 <= result.score <= 1.0


def test_predict_one_neutral():
    """Test predizione per testo neutro."""
    text = "The product arrived on time. It's okay."
    result = predict_one(text)
    
    assert isinstance(result, Prediction)
    assert result.label in ["negative", "neutral", "positive"]
    assert 0.0 <= result.score <= 1.0


def test_predict_one_empty_text():
    """Test che testo vuoto solleva errore."""
    with pytest.raises(ValueError):
        predict_one("")


def test_predict_batch():
    """Test predizione batch."""
    texts = [
        "I love this!",
        "This is terrible.",
        "It's okay, nothing special."
    ]
    
    results = predict_batch(texts)
    
    assert len(results) == 3
    assert all(isinstance(r, Prediction) for r in results)
    assert all(r.label in ["negative", "neutral", "positive"] for r in results)
    assert all(0.0 <= r.score <= 1.0 for r in results)


def test_predict_batch_empty():
    """Test batch vuoto restituisce lista vuota."""
    results = predict_batch([])
    assert results == []


