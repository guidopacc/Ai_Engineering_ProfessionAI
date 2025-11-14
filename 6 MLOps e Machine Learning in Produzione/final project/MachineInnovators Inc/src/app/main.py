"""
Applicazione FastAPI principale per sentiment analysis.
"""
import json
import os
import time
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import TextItem, Prediction, BatchRequest, BatchResponse
from .infer import predict_one, predict_batch
from .health import app_health
from .metrics import (
    update_sentiment_metric,
    get_metrics,
    REQUEST_COUNT,
    REQUEST_LATENCY
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sentiment Reputation Monitoring API",
    description="API per analisi del sentiment su testi social",
    version="1.0.0",
    tags=["sentiment", "health", "metrics"]
)

DEBUG = os.getenv("DEBUG", "False").lower() == "true"
if DEBUG:
    cors_origins = ["*"]
else:
    cors_origins = [
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    """Middleware per metriche Prometheus e logging JSON delle richieste."""
    start_time = time.time()
    method = request.method
    path = request.url.path
    
    response = await call_next(request)
    
    latency = time.time() - start_time
    latency_ms = latency * 1000
    status_code = response.status_code
    
    REQUEST_LATENCY.labels(method=method, endpoint=path).observe(latency)
    REQUEST_COUNT.labels(method=method, endpoint=path, status=str(status_code)).inc()
    
    log_data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "route": path,
        "method": method,
        "latency_ms": round(latency_ms, 2),
        "status_code": status_code
    }
    
    logger.info(json.dumps(log_data))
    
    return response


@app.get("/health", tags=["health"], summary="Health check")
async def health():
    """Endpoint di health check."""
    return app_health()


@app.post("/predict", response_model=Prediction, tags=["sentiment"], summary="Predizione singola")
async def predict(item: TextItem):
    """Predice il sentiment per un singolo testo."""
    try:
        start_time = time.time()
        prediction = predict_one(item.text)
        latency = (time.time() - start_time) * 1000
        
        update_sentiment_metric(prediction.label)
        
        logger.info(
            json.dumps({
                "event": "prediction",
                "label": prediction.label,
                "score": prediction.score,
                "latency_ms": round(latency, 2)
            })
        )
        
        return prediction
    except Exception as e:
        logger.error(f"Errore durante predizione: {e}")
        raise HTTPException(status_code=500, detail=f"Errore durante predizione: {str(e)}")


@app.post("/predict/batch", response_model=BatchResponse, tags=["sentiment"], summary="Predizione batch")
async def predict_batch_endpoint(request: BatchRequest):
    """Predice il sentiment per una lista di testi."""
    try:
        start_time = time.time()
        predictions = predict_batch(request.texts)
        latency = (time.time() - start_time) * 1000
        
        for pred in predictions:
            update_sentiment_metric(pred.label)
        
        logger.info(
            json.dumps({
                "event": "batch_prediction",
                "batch_size": len(predictions),
                "latency_ms": round(latency, 2)
            })
        )
        
        return BatchResponse(predictions=predictions)
    except Exception as e:
        logger.error(f"Errore durante predizione batch: {e}")
        raise HTTPException(status_code=500, detail=f"Errore durante predizione batch: {str(e)}")


@app.get("/metrics", tags=["metrics"], summary="Metriche Prometheus")
async def metrics():
    """Endpoint per esporre metriche Prometheus."""
    return get_metrics()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

