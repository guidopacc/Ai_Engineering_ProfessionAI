"""
Modulo per metriche Prometheus e monitoring.
"""
import logging
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

logger = logging.getLogger(__name__)

REQUEST_COUNT = Counter(
    'fastapi_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'fastapi_request_latency_seconds',
    'Request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)

SENTIMENT_DISTRIBUTION = Counter(
    'sentiment_predictions_total',
    'Total sentiment predictions by label',
    ['label']
)

LABEL_DRIFT = Gauge(
    'sentiment_label_drift_kl',
    'KL divergence for label distribution drift',
)


def update_sentiment_metric(label: str):
    """Incrementa il contatore per la distribuzione dei sentiment."""
    SENTIMENT_DISTRIBUTION.labels(label=label).inc()


def update_drift_metric(kl_value: float):
    """Aggiorna la metrica di drift (KL divergence)."""
    LABEL_DRIFT.set(kl_value)


def get_metrics():
    """Restituisce le metriche Prometheus in formato text."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


