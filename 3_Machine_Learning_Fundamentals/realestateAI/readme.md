# RealEstateAI
## Previsione dei prezzi immobiliari con regressione regolarizzata

---

## Descrizione

RealEstateAI è un progetto di machine learning per stimare il prezzo di immobili in base alle loro caratteristiche. Il sistema implementa e confronta tre modelli di regressione lineare con regolarizzazione — Ridge, Lasso ed Elastic Net — per ridurre l'overfitting e migliorare la capacità di generalizzazione.

Il progetto:
- Implementa e confronta i tre modelli regolarizzati con ricerca manuale dei parametri (alpha, l1_ratio)
- Valuta le performance con MSE, RMSE, MAE e R², con validazione incrociata sul modello selezionato
- Visualizza i risultati: predizioni vs reali, residui, importanza dei coefficienti, confronto tra modelli
- Salva metriche e grafici su disco per trasparenza e replicabilità

---

## Autore e contesto

**Autore:** Guido Pacciani  
Sviluppato come progetto finale del modulo *"Machine Learning Fundamentals"* del **Master Professionale in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

---

## Struttura del progetto

```
realestateAI/
├── main.py                   # Script principale: carica dati, preprocessa e lancia il workflow
├── requirements.txt          # Dipendenze Python
├── readme.md                 # Questo file
└── reg_models/               # Package Python con funzioni modulari
   ├── __init__.py            # Espone le funzioni principali del package
   ├── utils.py               # Utility generiche (gestione NaN, conteggio coefficienti...)
   ├── modeling.py            # Creazione modelli, training e metriche base
   ├── search.py              # Ricerca manuale dei parametri ottimali
   ├── report.py              # Report testuali e tabella riassuntiva
   ├── plots.py               # Grafici (residui, confronto modelli...)
   └── workflow.py            # Ciclo completo: ricerca → report → grafici → salvataggio
```

**Cartelle di output** (create automaticamente):
- `outputs/tabella_modelli.csv` — tutte le combinazioni testate con le relative metriche
- `outputs/migliore_metrics.json` — metriche del modello selezionato
- `outputs/fig_pred_residui.png`, `outputs/fig_confronto_modelli.png` — grafici

---

## Requisiti e installazione

- Python 3.9 o superiore

Installa le dipendenze con:
```bash
pip install -r requirements.txt
```

Il file `requirements.txt` include:
```
numpy==1.26.4
pandas==2.2.2
scikit-learn==1.4.2
matplotlib==3.8.4
joblib==1.4.2
```

---

## Come eseguire

```bash
cd realestateAI/
python main.py
```

I risultati vengono salvati automaticamente nella cartella `outputs/`.

**Nota per macOS:** se ricevi l'errore `certificate verify failed`, esegui:
```bash
/Applications/Python\ 3.12/Install\ Certificates.command
```

---

## Dataset

- **URL:** [https://proai-datasets.s3.eu-west-3.amazonaws.com/housing.csv](https://proai-datasets.s3.eu-west-3.amazonaws.com/housing.csv)
- **Variabili:** `Price` (target), `Area`, `Bedrooms`, `Bathrooms`, `Stories`, `Mainroad`, `Guestroom`, `Basement`, `Hotwaterheating`, `Airconditioning`, `Parking`, `Prefarea`, `Furnishingstatus`

---

## Output attesi

Esempio di output console:

```
[1] Carico il dataset...
[2] Controllo valori mancanti...
[7] Avvio il workflow per cercare il modello migliore...

VALUTAZIONE: RIDGE (alpha=1.0)
Metriche principali (test set):
  - MSE  : 123456.789
  - RMSE : 351.364
  - MAE  : 210.123
  - R²   : 0.8123
```

---

## Approfondimento tecnico

I tre modelli testati differiscono nel tipo di penalizzazione applicata ai coefficienti:

- **Ridge (L2)**: penalizza i coefficienti al quadrato, li riduce verso zero ma non li azzera. Utile quando tutte le feature contribuiscono, anche marginalmente.
- **Lasso (L1)**: penalizza il valore assoluto dei coefficienti, portandone alcuni esattamente a zero. Ottiene selezione automatica delle feature.
- **Elastic Net (L1+L2)**: combinazione pesata di Ridge e Lasso, controllata da `l1_ratio`. Bilancia riduzione e selezione.

La ricerca degli iperparametri (alpha e l1_ratio) è implementata manualmente in `search.py` con un loop su griglie di valori, senza `GridSearchCV`, per esporre la logica di selezione. La validazione incrociata k-fold viene poi applicata al modello finale selezionato per stimare la varianza delle performance.

---

## Riferimenti

- [scikit-learn — Ridge, Lasso, ElasticNet](https://scikit-learn.org/stable/modules/linear_model.html)
- [Dataset originale](https://www.kaggle.com/datasets/yasserh/housing-prices-dataset)

---

## Licenza

Rilasciato con licenza **MIT** — libero per uso personale, studio o sviluppo. Clona e modifica liberamente.
