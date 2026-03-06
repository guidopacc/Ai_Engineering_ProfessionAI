# MachineInnovators Inc – Sentiment Reputation Monitoring

**Autore:** Guido Pacciani  
**Azienda:** MachineInnovators Inc.  
**Corso di riferimento:** MLOps e Machine Learning in Produzione – Master in AI Engineering, ProfessionAI

---

## Descrizione

Questo progetto implementa una **pipeline MLOps end-to-end** per il monitoraggio della reputazione online tramite analisi del sentiment su testi provenienti da piattaforme social.

Il sistema è progettato per essere scalabile, containerizzato e facilmente deployabile in produzione. Include un'API REST per l'integrazione con sistemi esterni, un sistema di monitoring con Prometheus e Grafana, una pipeline CI/CD con GitHub Actions, e rilevamento automatico di concept drift con retraining periodico.

---

## Obiettivi

1. Analisi automatica del sentiment su testi social tramite un modello NLP pre-addestrato
2. Esposizione del modello tramite un servizio API REST (FastAPI)
3. Monitoraggio in produzione con metriche personalizzate (Prometheus + Grafana)
4. Pipeline CI/CD automatizzata con GitHub Actions per testing e deployment
5. Rilevamento del concept drift per garantire la qualità del modello nel tempo
6. Retraining periodico del modello per adattarsi ai cambiamenti nei dati

---

## Modello di Machine Learning

**Modello:** `cardiffnlp/twitter-roberta-base-sentiment-latest` (Hugging Face)

Il modello è pre-addestrato e ottimizzato per testi social e Twitter. Supporta tre classi di sentiment:
- `negative`
- `neutral`
- `positive`

Non richiede training iniziale, permettendo un deployment rapido.

---

## Stack Tecnologico

| Componente        | Tecnologia                             |
|-------------------|----------------------------------------|
| Linguaggio        | Python 3.10+                           |
| Framework Web     | FastAPI + Uvicorn                      |
| Machine Learning  | Transformers (Hugging Face) + PyTorch  |
| Validazione       | Pydantic                               |
| Testing           | Pytest + pytest-cov                    |
| Monitoring        | Prometheus + Grafana                   |
| Container         | Docker + Docker Compose                |
| CI/CD             | GitHub Actions                         |
| Version Control   | Git / GitHub                           |

---

## Struttura del progetto

```
MachineInnovators Inc/
├── .github/workflows/          # Pipeline CI/CD
│   ├── ci.yml                  # Workflow di Continuous Integration
│   └── cd.yml                  # Workflow di Continuous Deployment
├── docker/                     # Configurazioni Docker
│   ├── Dockerfile              # Immagine dell'API
│   ├── compose.yml             # Orchestrazione servizi (API + Prometheus + Grafana)
│   └── prometheus.yml          # Configurazione Prometheus
├── notebooks/                  # Notebook di analisi e dimostrazione
│   ├── consegna_finale.ipynb   # Notebook principale del progetto
│   └── exploration_and_report.ipynb
├── src/
│   ├── app/                    # Applicazione FastAPI
│   │   ├── main.py             # Entry point, middleware, endpoint
│   │   ├── infer.py            # Logica di inferenza del modello
│   │   ├── metrics.py          # Metriche Prometheus personalizzate
│   │   ├── health.py           # Health check
│   │   └── schemas.py          # Schemi Pydantic (input/output)
│   ├── data/                   # Dati di esempio
│   └── utils/                  # Utility
│       ├── drift.py            # Rilevamento concept drift
│       └── retraining.py       # Pipeline di retraining
├── tests/                      # Test suite
├── requirements.txt            # Dipendenze Python
├── pytest.ini                  # Configurazione Pytest
└── README.md                   # Questo file
```

---

## API Endpoints

| Metodo | Endpoint         | Descrizione                               |
|--------|------------------|------------------------------------------|
| GET    | `/health`        | Verifica lo stato dell'applicazione      |
| POST   | `/predict`       | Predizione sentiment per un singolo testo|
| POST   | `/predict/batch` | Predizione sentiment per più testi       |
| GET    | `/metrics`       | Esposizione metriche Prometheus          |

### Esempio di utilizzo

```bash
# Predizione singola
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Great product, very satisfied!"}'

# Risposta
{
  "label": "positive",
  "score": 0.982
}
```

---

## Come eseguire il progetto

### Prerequisiti

- Docker e Docker Compose installati
- Python 3.10+ (per esecuzione locale senza Docker)

### Avvio con Docker Compose

```bash
cd "MachineInnovators Inc"

# Avvia tutti i servizi (API + Prometheus + Grafana)
docker compose -f docker/compose.yml up --build
```

I servizi saranno disponibili a:
- **API**: http://localhost:8000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

### Esecuzione locale (senza Docker)

```bash
# Installa le dipendenze
pip install -r requirements.txt

# Avvia l'API
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```

### Esecuzione dei test

```bash
pytest tests/ -v --cov=src
```

---

## Monitoring

Il sistema espone metriche Prometheus per:
- Conteggio delle richieste per endpoint e status code
- Latenza delle richieste (ms)
- Distribuzione delle predizioni di sentiment (negative/neutral/positive)

Le metriche possono essere visualizzate su Grafana configurando Prometheus come datasource.

---

## CI/CD Pipeline

La pipeline GitHub Actions esegue automaticamente:

1. **CI (`ci.yml`):** linting, esecuzione dei test e calcolo della code coverage ad ogni push/pull request
2. **CD (`cd.yml`):** build e push dell'immagine Docker al registro al merge su `main`

---

## Dipendenze principali

```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
transformers==4.36.2
torch==2.1.2
pytest==7.4.4
pytest-cov==4.1.0
prometheus-client==0.19.0
pandas==2.1.4
numpy==1.26.3
```

---

## Licenza

Questo progetto è stato sviluppato esclusivamente per scopi didattici nell'ambito del **Master in AI Engineering** erogato da **ProfessionAI**.

---

**Sviluppato con ❤️ per il Master in AI Engineering – ProfessionAI**
