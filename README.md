# Sentiment Reputation Monitoring

Sistema completo end-to-end per il monitoraggio della reputazione online tramite analisi del sentiment su testi social. Il progetto include serving via API FastAPI, test automatici, containerizzazione Docker, CI/CD con GitHub Actions, e monitoraggio in produzione con Prometheus e Grafana.

## Indice

- [Panoramica](#panoramica)
- [Stack Tecnologico](#stack-tecnologico)
- [Struttura Progetto](#struttura-progetto)
- [Installazione e Setup](#installazione-e-setup)
- [Esecuzione](#esecuzione)
- [API Contract](#api-contract)
- [Monitoring e Grafana](#monitoring-e-grafana)
- [CI/CD](#cicd)
- [Testing](#testing)
- [Sviluppo e Contributi](#sviluppo-e-contributi)

## Panoramica

Questo progetto implementa una pipeline completa per:

- **Sentiment Analysis**: Utilizza il modello Hugging Face `cardiffnlp/twitter-roberta-base-sentiment-latest` per analizzare il sentiment di testi (negative, neutral, positive)
- **API REST**: FastAPI con endpoint per predizioni singole e batch
- **Monitoring**: Metriche Prometheus esposte e visualizzate in Grafana
- **Drift Detection**: Implementazione didattica di KL divergence per rilevare concept drift
- **CI/CD**: GitHub Actions per test automatici e build/push Docker
- **Containerizzazione**: Docker e Docker Compose per deployment facile

## Stack Tecnologico

- **Python**: 3.10+
- **Framework**: FastAPI, Uvicorn
- **ML**: Transformers (Hugging Face), PyTorch (CPU)
- **Validation**: Pydantic
- **Testing**: Pytest, pytest-cov
- **Monitoring**: Prometheus, Grafana
- **Container**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Gestione Dipendenze**: pip, venv

## Struttura Progetto

```
sentiment-reputation/
├── README.md                       # Questo file
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Dipendenze Python
├── pytest.ini                      # Configurazione pytest
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app principale
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── infer.py                # Logica inferenza modello
│   │   ├── health.py               # Health check
│   │   └── metrics.py              # Metriche Prometheus
│   ├── data/
│   │   └── samples.jsonl           # Campioni etichettati per test
│   └── utils/
│       └── drift.py                # Utility per drift detection
├── tests/
│   ├── __init__.py
│   ├── test_health.py              # Test health endpoint
│   ├── test_infer_unit.py          # Test unitari inferenza
│   └── test_api_integration.py     # Test integrazione API
├── docker/
│   ├── Dockerfile                  # Immagine Docker API
│   ├── compose.yml                 # Docker Compose setup
│   └── prometheus.yml              # Config Prometheus
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Continuous Integration
│       └── cd.yml                  # Continuous Deployment
└── notebooks/
    └── exploration_and_report.ipynb  # Notebook esplorazione
```

## Installazione e Setup

### Prerequisiti

- Python 3.10 o superiore
- pip
- Docker e Docker Compose (per deployment containerizzato)
- Git

### Setup Locale (venv)

1. **Clona il repository**:
```bash
git clone <repository-url>
cd sentiment-reputation
```

2. **Crea virtual environment**:
```bash
python -m venv .venv
```

3. **Attiva virtual environment**:
   - **Linux/macOS**:
   ```bash
   source .venv/bin/activate
   ```
   - **Windows**:
   ```cmd
   .venv\Scripts\activate
   ```

4. **Installa dipendenze**:
```bash
pip install -r requirements.txt
```

**Nota**: Il primo avvio potrebbe richiedere tempo per scaricare il modello Hugging Face (~500MB) e le dipendenze PyTorch.

## Esecuzione

### Locale (Sviluppo)

1. **Avvia l'API FastAPI**:
```bash
uvicorn src.app.main:app --reload
```

L'API sarà disponibile su `http://localhost:8000`

2. **Verifica health check**:
```bash
curl http://localhost:8000/health
```

3. **Testa predizione**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

4. **Testa predizione batch**:
```bash
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great!", "Terrible.", "Okay."]}'
```

5. **Visualizza metriche Prometheus**:
```bash
curl http://localhost:8000/metrics
```

6. **Documentazione interattiva Swagger**:
   - Apri `http://localhost:8000/docs` nel browser

### Docker Compose (Produzione)

1. **Avvia tutti i servizi**:
```bash
docker compose -f docker/compose.yml up --build
```

Questo avvierà:
- **API**: `http://localhost:8000`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000`

2. **Accesso Grafana**:
   - URL: `http://localhost:3000`
   - Username: `admin`
   - Password: `admin`
   - Alla prima login verrà chiesto di cambiare la password

3. **Configura Prometheus come datasource in Grafana**:
   - Vai su Configuration → Data Sources → Add data source
   - Seleziona Prometheus
   - URL: `http://prometheus:9090`
   - Salva & Test

4. **Ferma i servizi**:
```bash
docker compose -f docker/compose.yml down
```

## API Contract

### GET /health

Health check endpoint.

**Response**:
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_name": "cardiffnlp/twitter-roberta-base-sentiment-latest"
}
```

### POST /predict

Predizione sentiment per un singolo testo.

**Request Body**:
```json
{
  "text": "I love this product!"
}
```

**Response**:
```json
{
  "label": "positive",
  "score": 0.95
}
```

**Errori**:
- `422`: Validazione fallita (testo vuoto, troppo lungo, etc.)
- `500`: Errore interno durante predizione

### POST /predict/batch

Predizione sentiment per una lista di testi (max 100).

**Request Body**:
```json
{
  "texts": ["Great!", "Terrible.", "Okay."]
}
```

**Response**:
```json
{
  "predictions": [
    {"label": "positive", "score": 0.92},
    {"label": "negative", "score": 0.88},
    {"label": "neutral", "score": 0.75}
  ]
}
```

**Errori**:
- `422`: Validazione fallita (lista vuota, troppi testi, etc.)
- `500`: Errore interno durante predizione

### GET /metrics

Endpoint per esporre metriche Prometheus.

**Response**: Testo in formato Prometheus exposition format.

**Metriche disponibili**:
- `fastapi_requests_total`: Contatore richieste totali (per metodo, endpoint, status)
- `fastapi_request_latency_seconds`: Istogramma latenza richieste
- `sentiment_predictions_total`: Contatore predizioni per label
- `sentiment_label_drift_kl`: Gauge per KL divergence (drift)

### GET /docs

Documentazione interattiva Swagger UI.

## Monitoring e Grafana

### Metriche Prometheus

Il sistema espone metriche operative:

- **Request Metrics**: `fastapi_requests_total` (richieste totali), `fastapi_request_latency_seconds` (latenza)
- **Business Metrics**: `sentiment_predictions_total` (distribuzione sentiment), `sentiment_label_drift_kl` (drift detection)

### Dashboard Grafana

Configura una dashboard Grafana con i seguenti pannelli:

#### 1. Request Rate
```
Query: rate(fastapi_requests_total[5m])
Visualizzazione: Graph
```

#### 2. Latenza P50/P95
```
Query P50: histogram_quantile(0.5, rate(fastapi_request_latency_seconds_bucket[5m]))
Query P95: histogram_quantile(0.95, rate(fastapi_request_latency_seconds_bucket[5m]))
Visualizzazione: Graph
```

#### 3. Distribuzione Sentiment
```
Query: rate(sentiment_predictions_total[5m]) by (label)
Visualizzazione: Pie Chart o Bar Chart
```

#### 4. Drift (KL Divergence)
```
Query: sentiment_label_drift_kl
Visualizzazione: SingleStat o Gauge
Alerts: Alert quando valore > 0.1
```

### Esempio Query Prometheus

**Request rate per endpoint**:
```promql
rate(fastapi_requests_total[5m]) by (endpoint)
```

**Error rate**:
```promql
rate(fastapi_requests_total{status=~"5.."}[5m]) / rate(fastapi_requests_total[5m])
```

**Distribuzione sentiment (percentuale)**:
```promql
rate(sentiment_predictions_total[5m]) by (label) / sum(rate(sentiment_predictions_total[5m])) * 100
```

## CI/CD

### Continuous Integration (CI)

Workflow `ci.yml` viene eseguito su:
- Pull request su `main`/`master`
- Push su `main`/`master`

**Step**:
1. Checkout codice
2. Setup Python 3.10
3. Cache pip packages
4. Installa dipendenze
5. Esegue pytest con coverage
6. Build Docker image (validazione)

### Continuous Deployment (CD)

Workflow `cd.yml` viene eseguito su:
- Release pubblicate
- Push tag `v*`

**Step**:
1. Build e push immagine Docker su GitHub Container Registry (GHCR)
2. Tag: `latest`, `sha`, semver
3. (Opzionale) Deploy su Hugging Face Spaces (se configurato `HF_TOKEN`)

### Secrets GitHub

Configura i seguenti secrets nel repository per abilitare il deploy:

- **GITHUB_TOKEN**: Automatico (per GHCR)
- **HF_TOKEN**: (Opzionale) Token Hugging Face per deploy su Spaces

## Testing

### Esegui tutti i test

```bash
pytest
```

### Test con coverage

```bash
pytest --cov=src --cov-report=term-missing
```

### Test specifici

```bash
pytest tests/test_health.py
pytest tests/test_infer_unit.py
pytest tests/test_api_integration.py
```

### Configurazione Pytest

Il file `pytest.ini` configura:
- Output quiet (`-q`)
- Fail fast (`--maxfail=1`)
- Disabilita warning (`--disable-warnings`)

## Sviluppo e Contributi

### Code Quality

Si consiglia l'uso di:

- **Black**: Formattazione codice
  ```bash
  pip install black
  black src/ tests/
  ```

- **Flake8**: Linting
  ```bash
  pip install flake8
  flake8 src/ tests/
  ```

### Best Practices

- Logging in formato JSON line (timestamp, route, latency)
- Validazione input con Pydantic
- Limitazioni: testo max 1000 caratteri, batch max 100 testi, token max 512

### Retraining

Il modulo `src/utils/retrain.py` implementa una simulazione di retraining periodico del modello. Lo script simula il processo di retraining (caricamento dati, addestramento, validazione) con un intervallo configurabile.

**Esecuzione**:
```bash
python src/utils/retrain.py
```

Per default, il retraining viene simulato ogni 60 secondi. Per modificare l'intervallo, modifica il parametro `interval_seconds` nella chiamata a `retrain_loop()`.

In produzione, questo script può essere integrato con un orchestratore come Airflow per eseguire retraining programmati su nuovi dati.

### Notebook

Il notebook `notebooks/exploration_and_report.ipynb` include:
- Caricamento e analisi campioni
- Test API locale
- Visualizzazione distribuzione sentiment
- Calcolo KL divergence
- Analisi finestre mobili
- Conclusioni e idee di miglioramento

**Esecuzione**:
1. Avvia l'API localmente (`uvicorn src.app.main:app --reload`)
2. Apri Jupyter: `jupyter notebook notebooks/exploration_and_report.ipynb`
3. Esegui tutte le celle

## Build Docker Manuale

```bash
# Build immagine
docker build -f docker/Dockerfile -t sentiment-reputation:latest .

# Run container
docker run -p 8000:8000 sentiment-reputation:latest
```

## Deploy su Hugging Face Spaces

### Setup Manuale

1. Crea un nuovo Space su Hugging Face (tipo: Docker)
2. Configura `HF_TOKEN` secret nel repository GitHub
3. Push un tag o release per triggerare il workflow CD

### Template FastAPI per HF Spaces

Crea un file `app.py` nella root del Space:

```python
from src.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
```

## Note Importanti

- **Primo avvio**: Il modello Hugging Face viene scaricato automaticamente al primo utilizzo (~500MB)
- **Memoria**: Assicurati di avere almeno 2GB RAM disponibili per il modello
- **Performance**: Il modello è ottimizzato per CPU; per GPU aggiungi `device=0` nella pipeline
- **Monitoring**: Prometheus scrapa metriche ogni 5 secondi (configurabile in `docker/prometheus.yml`)

## Licenza

Nessuna licenza

## Autore

Guido Pacciani

---

**Status**: Project completo e funzionante

**Ultimo aggiornamento**: novembre 2025


