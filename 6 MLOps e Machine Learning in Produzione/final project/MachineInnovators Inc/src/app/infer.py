"""
Modulo per inferenza sentiment analysis usando il modello Hugging Face.
"""
import logging
from typing import List, Optional
from transformers import pipeline

from .schemas import Prediction

logger = logging.getLogger(__name__)

_pipeline: Optional[object] = None
_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"


def get_pipeline():
    """Carica la pipeline con lazy loading per ridurre tempo di startup."""
    global _pipeline
    if _pipeline is None:
        logger.info(f"Caricamento modello {_model_name}...")
        try:
            _pipeline = pipeline(
                "sentiment-analysis",
                model=_model_name,
                tokenizer=_model_name,
                return_all_scores=False,
                max_length=512,
                truncation=True
            )
            logger.info(f"Modello {_model_name} caricato con successo")
        except Exception as e:
            logger.error(f"Errore durante il caricamento del modello: {e}")
            raise
    return _pipeline


def _normalize_label(label: str) -> str:
    """Normalizza label del modello in formato standardizzato."""
    label_lower = label.lower()
    if "negative" in label_lower or label_lower == "label_0":
        return "negative"
    elif "neutral" in label_lower or label_lower == "label_1":
        return "neutral"
    elif "positive" in label_lower or label_lower == "label_2":
        return "positive"
    else:
        logger.warning(f"Label non riconosciuta: {label}, restituita così com'è")
        return label_lower


def predict_one(text: str) -> Prediction:
    """Predice il sentiment per un singolo testo."""
    if not text or not text.strip():
        raise ValueError("Il testo non può essere vuoto")
    
    pipe = get_pipeline()
    result = pipe(text[:1000])
    
    if isinstance(result, list) and len(result) > 0:
        label_raw = result[0].get("label", "neutral")
        score = result[0].get("score", 0.0)
        label = _normalize_label(label_raw)
    else:
        label = "neutral"
        score = 0.5
        logger.warning(f"Formato risultato inatteso per testo: {text[:50]}")
    
    return Prediction(label=label, score=float(score))


def predict_batch(texts: List[str]) -> List[Prediction]:
    """Predice il sentiment per una lista di testi."""
    if not texts:
        return []
    
    max_batch = 100
    if len(texts) > max_batch:
        logger.warning(f"Batch size {len(texts)} supera il massimo {max_batch}, vengono processati solo i primi {max_batch}")
        texts = texts[:max_batch]
    
    predictions = []
    for text in texts:
        try:
            pred = predict_one(text)
            predictions.append(pred)
        except Exception as e:
            logger.error(f"Errore durante predizione per testo: {text[:50]}, errore: {e}")
            predictions.append(Prediction(label="neutral", score=0.5))
    
    return predictions


def is_model_loaded() -> bool:
    """Verifica se il modello è stato caricato."""
    return _pipeline is not None


def get_model_name() -> str:
    """Restituisce il nome del modello utilizzato."""
    return _model_name


