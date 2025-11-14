"""
Schemi Pydantic per validazione input/output API.
"""
from typing import List
from pydantic import BaseModel, Field


class TextItem(BaseModel):
    """Schema per richiesta di predizione singola."""
    text: str = Field(..., min_length=1, max_length=1000, description="Testo da analizzare per sentiment")


class Prediction(BaseModel):
    """Schema per predizione singola."""
    label: str = Field(..., description="Label di sentiment: negative, neutral, positive")
    score: float = Field(..., ge=0.0, le=1.0, description="Score di confidenza della predizione")


class BatchRequest(BaseModel):
    """Schema per richiesta batch."""
    texts: List[str] = Field(..., min_items=1, max_items=100, description="Lista di testi da analizzare")


class BatchResponse(BaseModel):
    """Schema per risposta batch."""
    predictions: List[Prediction] = Field(..., description="Lista di predizioni per ogni testo")

