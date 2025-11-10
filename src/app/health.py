"""
Modulo per health check dell'applicazione.
"""
from .infer import is_model_loaded, get_model_name


def app_health() -> dict:
    """Restituisce lo stato di salute dell'applicazione."""
    return {
        "status": "ok",
        "model_loaded": is_model_loaded(),
        "model_name": get_model_name()
    }


