# Sentiment Reputation Monitoring – MachineInnovators Inc.

API REST per l'analisi del sentiment su testi social, con monitoraggio in tempo reale, rilevamento del data drift e pipeline CI/CD.

**Autore:** Guido Pacciani  
**Contesto:** Progetto finale del corso *"MLOps e Machine Learning in Produzione"* – Master in AI Engineering, ProfessionAI

---

## Descrizione

Il progetto implementa un sistema MLOps completo per il monitoraggio della reputazione online di un'azienda attraverso l'analisi automatica del sentiment su testi social. Il sistema è composto da:

- **API FastAPI** che espone endpoint di inferenza (singola e batch) e health check
- **Modello NLP** pre-addestrato (`cardiffnlp/twitter-roberta-base-sentiment-latest`) caricato tramite Hugging Face Transformers
- **Monitoraggio** con Prometheus e Grafana per metriche di latenza, conteggio richieste e distribuzione dei label
- **Rilevamento del data drift** tramite divergenza di Kullback-Leibler su distribuzioni di label
- **Simulazione retraining** periodico del modello
- **Pipeline CI/CD** con GitHub Actions (test + build Docker)
- **Containerizzazione** completa con Docker e Docker Compose

---

## Struttura del progetto

```
MachineInnovators Inc/
│
├── src/
│   ├── app/
│   │   ├── main.py        # Applicazione FastAPI con middleware e route
│   │   ├── infer.py       # Caricamento modello e logica di inferenza
│   │   ├── health.py      # Endpoint di health check
│   │   ├── metrics.py     # Metriche Prometheus
│   │   └── schemas.py     # Schemi Pydantic per request/response
│   ├── utils/
│   │   ├── drift.py       # Calcolo KL divergence e distribuzione label
│   │   └── retrain.py     # Simulazione loop di retraining
│   └── data/
│       └── samples.jsonl  # Dati di esempio per test
│
├── tests/
│   ├── test_api_integration.py  # Test di integrazione API
│   ├── test_health.py           # Test endpoint health
│   └── test_infer_unit.py       # Test unitari inferenza
│
├── notebooks/
│   ├── consegna_finale.ipynb        # Notebook di consegna
│   └── exploration_and_report.ipynb # Analisi e report
│
├── docker/
│   ├── Dockerfile        # Immagine Docker per l'API
│   ├── compose.yml       # Orchestrazione API + Prometheus + Grafana
│   └── prometheus.yml    # Configurazione scraping Prometheus
│
├── workflows/
│   ├── ci.yml            # Pipeline CI: test e build Docker
│   └── cd.yml            # Pipeline CD: deploy
│
├── requirements.txt      # Dipendenze Python
├── pytest.ini            # Configurazione pytest
└── README.md             # Questo file
```

---

## Endpoint API

| Metodo | Endpoint         | Descrizione                         |
|--------|------------------|-------------------------------------|
| GET    | `/health`        | Health check dell'applicazione      |
| POST   | `/predict`       | Analisi del sentiment su un testo   |
| POST   | `/predict/batch` | Analisi del sentiment su più testi  |
| GET    | `/metrics`       | Metriche in formato Prometheus      |

### Esempi di utilizzo

```bash
# Predizione singola
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'

# Predizione batch
curl -X POST http://localhost:8000/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great service!", "Terrible experience.", "It was okay."]}'
```

### Formato risposta `/predict`

```json
{
  "label": "positive",
  "score": 0.9876
}
```

I label restituiti sono: `positive`, `neutral`, `negative`.

---

## Requisiti

- Python 3.10+
- Docker e Docker Compose (per esecuzione containerizzata)

### Dipendenze Python principali

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
transformers==4.36.2
torch==2.1.2
prometheus-client==0.19.0
pydantic==2.5.3
```

Installa tutte le dipendenze con:

```bash
pip install -r requirements.txt
```

---

## Avvio locale (senza Docker)

```bash
# Dalla cartella del progetto
uvicorn src.app.main:app --host 0.0.0.0 --port 8000
```

L'API sarà disponibile su `http://localhost:8000`.  
La documentazione interattiva (Swagger UI) è accessibile su `http://localhost:8000/docs`.

---

## Avvio con Docker Compose

```bash
# Dalla cartella docker/
docker compose -f docker/compose.yml up --build
```

Questo avvia tre servizi:

| Servizio    | Porta | Descrizione                    |
|-------------|-------|--------------------------------|
| API         | 8000  | Applicazione FastAPI           |
| Prometheus  | 9090  | Raccolta metriche              |
| Grafana     | 3000  | Dashboard di monitoraggio      |

Grafana è accessibile su `http://localhost:3000` (credenziali: `admin` / `admin`).

---

## Test

```bash
pytest --cov=src --cov-report=term-missing
```

I test coprono:
- **Unit test** (`test_infer_unit.py`): logica di normalizzazione dei label, validazione input
- **Test di integrazione** (`test_api_integration.py`): endpoint `/predict` e `/predict/batch`
- **Test health** (`test_health.py`): endpoint `/health`

---

## Pipeline CI/CD

Il workflow **CI** (`.github/workflows/ci.yml`) viene eseguito ad ogni push o pull request su `main`/`master` e:
1. Installa le dipendenze
2. Esegue i test con coverage
3. Valida la build dell'immagine Docker

---

## Monitoraggio e Data Drift

Il modulo `src/utils/drift.py` implementa:
- **Distribuzione mobile dei label** su finestre temporali (`windowed_label_distribution`)
- **Divergenza KL** (`kl_divergence`) per rilevare variazioni nella distribuzione dei sentiment rispetto alla baseline

Il modulo `src/utils/retrain.py` simula un loop di retraining periodico che in produzione si occuperebbe di ricaricare i dati, riaddestrare il modello e sostituirlo nella pipeline.

---

## Autore e Licenza

**Autore:** Guido Pacciani  
Questo progetto è stato sviluppato per scopi didattici nell'ambito del Master in AI Engineering erogato da **ProfessionAI**.

**Data di realizzazione:** 2025
