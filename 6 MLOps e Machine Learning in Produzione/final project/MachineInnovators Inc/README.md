# MachineInnovators Inc. — Sentiment Reputation Monitoring
## Pipeline MLOps per l'analisi del sentiment su testi social

---

## Descrizione

MachineInnovators Inc. è un progetto MLOps end-to-end per il monitoraggio della reputazione online di un'azienda manifatturiera attraverso l'analisi del sentiment su testi provenienti da piattaforme social. Il sistema classifica i testi in tre categorie — *positive*, *neutral*, *negative* — e li espone tramite un'API REST, con monitoraggio continuo in produzione.

Il progetto copre l'intero ciclo di vita di un modello ML in produzione:
- Servizio di inferenza con API REST (FastAPI)
- Containerizzazione con Docker e Docker Compose
- Monitoring con Prometheus e Grafana
- Pipeline CI/CD automatizzata con GitHub Actions
- Rilevamento di concept drift con KL Divergence
- Test automatici con pytest

---

## Autore e contesto

**Autore:** Guido Pacciani  
Sviluppato come progetto finale del modulo *"MLOps e Machine Learning in Produzione"* del **Master Professionale in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

---

## Struttura del progetto

```
MachineInnovators Inc/
├── src/
│   ├── app/
│   │   ├── main.py       # Applicazione FastAPI con endpoint REST
│   │   ├── infer.py      # Inferenza singola e batch
│   │   ├── schemas.py    # Modelli Pydantic per validazione input/output
│   │   ├── health.py     # Endpoint di health check
│   │   └── metrics.py    # Metriche Prometheus (contatori, latenza, distribuzione sentiment)
│   ├── data/             # Dati di riferimento per drift detection
│   └── utils/            # Utility condivise
├── notebooks/
│   ├── consegna_finale.ipynb       # Notebook di presentazione del progetto
│   └── exploration_and_report.ipynb
├── tests/                # Suite di test con pytest
├── docker/               # Dockerfile e configurazioni container
├── workflows/            # Configurazioni GitHub Actions e Grafana
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Tecnologie utilizzate

- **Python 3.10+**
- **FastAPI + Uvicorn** — API REST asincrona ad alte performance
- **Transformers (Hugging Face) + PyTorch** — modello NLP pre-addestrato
- **Pydantic** — validazione automatica degli schemi di input/output
- **Prometheus + prometheus-client** — raccolta e esposizione metriche
- **Grafana** — dashboard per visualizzazione metriche operative
- **Docker + Docker Compose** — containerizzazione e orchestrazione
- **GitHub Actions** — pipeline CI/CD
- **pytest + pytest-cov** — testing e coverage

---

## Modello ML

Il modello utilizzato è [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest) disponibile su Hugging Face. È un modello RoBERTa fine-tunato su testi social/Twitter per la classificazione del sentiment in tre classi (negative, neutral, positive). Non richiede training: viene scaricato automaticamente da Hugging Face al primo avvio.

---

## Come eseguire

### Con Docker Compose (consigliato)

```bash
cd "MachineInnovators Inc/"
docker compose up --build
```

I servizi avviati:
- **API**: `http://localhost:8000` (FastAPI + Swagger UI su `/docs`)
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000`

### In locale senza Docker

```bash
pip install -r requirements.txt
uvicorn src.app.main:app --reload --port 8000
```

### Eseguire i test

```bash
pytest tests/ -v --cov=src
```

---

## API Endpoints

| Metodo | Endpoint         | Descrizione                        |
|--------|------------------|------------------------------------|
| GET    | `/health`        | Health check del servizio          |
| POST   | `/predict`       | Predizione sentiment su un testo   |
| POST   | `/predict/batch` | Predizione su lista di testi       |
| GET    | `/metrics`       | Metriche in formato Prometheus     |

Esempio di richiesta:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Il prodotto è ottimo, consigliato!"}'
```

Risposta:
```json
{"label": "positive", "score": 0.97}
```

---

## Approfondimento tecnico

### Architettura del servizio

L'applicazione FastAPI gestisce richieste HTTP asincrone tramite `async/await`. Un middleware custom intercetta ogni richiesta per aggiornare i contatori Prometheus (`REQUEST_COUNT`, `REQUEST_LATENCY`) e loggare i dati strutturati in formato JSON. I modelli Pydantic garantiscono la validazione automatica degli schemi prima di invocare il modello ML.

### Monitoring e metriche

Prometheus raccoglie tre categorie di metriche:
- **Operative**: numero di richieste per endpoint e codice HTTP, latenza percentile
- **ML**: distribuzione del sentiment predetto nel tempo (utile per rilevare cambiamenti nel comportamento del modello)
- **System**: memoria e CPU del container

Le metriche vengono visualizzate in Grafana con dashboard configurabili.

### Drift detection

Il sistema monitora la distribuzione del sentiment sulle ultime N predizioni e la confronta con la distribuzione di riferimento usando la **KL Divergence** (Kullback-Leibler). Se la divergenza supera una soglia configurabile, il sistema emette un alert, segnalando un potenziale concept drift che potrebbe richiedere il retraining del modello.

### CI/CD con GitHub Actions

La pipeline si attiva su ogni push e pull request:
1. Esecuzione dei test con pytest
2. Build dell'immagine Docker
3. Controllo della copertura del codice

---

## Licenza

Rilasciato con licenza **MIT** — libero per uso personale, studio o sviluppo. Clona e modifica liberamente.
