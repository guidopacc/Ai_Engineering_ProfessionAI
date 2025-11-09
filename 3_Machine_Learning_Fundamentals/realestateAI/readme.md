# RealEstateAI – Modello di previsione per il mercato immobiliare

*Modello di regressione regolarizzata sviluppato per il master in AI Engineering, erogato da ProfessionAI*

**Data creazione:** 12 luglio 2025  
**Autore:** Guido Pacciani


---

## 1. Obiettivo del progetto

RealEstateAI Solutions intende ottimizzare la stima dei prezzi immobiliari sfruttando modelli di regressione lineare con tecniche di **regolarizzazione** (Ridge, Lasso, Elastic Net). L’obiettivo è fornire previsioni più accurate e stabili, riducendo l’overfitting e migliorando la capacità di generalizzazione.

In particolare, il progetto:
- implementa e confronta tre modelli regolarizzati;
- valuta le performance con MSE/RMSE/MAE e R², includendo **validazione incrociata** del modello selezionato;
- analizza la complessità del modello tramite il numero di coefficienti non nulli;
- visualizza i risultati (predizioni vs reali, residui, importanza dei coefficienti, confronto tra modelli);
- salva le metriche e i grafici su disco per garantire trasparenza e replicabilità.

---

## 2. Requisiti di sistema

- **Python**: versione 3.9 o superiore
- **Librerie**:  
  - numpy  
  - pandas  
  - scikit-learn  
  - matplotlib  

Puoi installare tutto con:
```bash
pip install -r requirements.txt
```

Esempio di `requirements.txt`:
```
numpy==1.26.4
pandas==2.2.2
scikit-learn==1.4.2
matplotlib==3.8.4
joblib==1.4.2
```

---

## 3. Dataset

- **URL:** [https://proai-datasets.s3.eu-west-3.amazonaws.com/housing.csv](https://proai-datasets.s3.eu-west-3.amazonaws.com/housing.csv)

**Variabili:**
- `Price` (target), `Area`, `Bedrooms`, `Bathrooms`, `Stories`, `Mainroad`, `Guestroom`, `Basement`, `Hotwaterheating`, `Airconditioning`, `Parking`, `Prefarea`, `Furnishingstatus` (0=non arredato, 1=parzialmente arredato, 2=completamente arredato).

---

## 4. Struttura del progetto

```
realestateAI/
├─ main.py                        # Script principale: carica dati, preprocessa, lancia il workflow
├─ requirements.txt               # Librerie necessarie per l'esecuzione
├─ readme.md                      # Questo file di documentazione
└─ reg_models/                    # Pacchetto Python con funzioni modulari
   ├─ __init__.py                 # Rende la cartella un package ed espone le funzioni principali
   ├─ utils.py                    # Utility generiche (riempimento NaN, conteggio coefficienti, ...)
   ├─ modeling.py                 # Creazione modelli e training + metriche base
   ├─ search.py                   # Ricerca manuale dei parametri (alpha, l1_ratio)
   ├─ report.py                   # Report testuali e tabella riassuntiva dei modelli
   ├─ plots.py                    # Grafici (residui, confronto modelli, ecc.)
   └─ workflow.py                 # Ciclo completo: ricerca → report → grafici → salvataggi
```

**Cartelle di output:**  
La cartella `outputs/` viene creata automaticamente dal workflow e contiene:
- `tabella_modelli.csv` (tutte le combinazioni testate)
- `migliore_metrics.json` (metriche del modello scelto)
- `fig_pred_residui.png`, `fig_confronto_modelli.png` (grafici)
- Il file `tabella_modelli.csv` viene salvato anche nella root per comodità.

---

## 5. Come eseguire il progetto

1. **Clona o copia** la struttura di cartelle sopra.
2. Installa le librerie richieste (vedi sopra).
3. Da terminale, spostati nella cartella `realestateAI/` e lancia:
   ```bash
   python main.py
   ```
4. Alla fine dell’esecuzione troverai i risultati nella cartella `outputs/`.

**Nota per utenti Mac:**
Se durante il caricamento del dataset ricevi un errore simile a `certificate verify failed: unable to get local issuer certificate`,
devi installare i certificati SSL di Python. Esegui questo comando da terminale:
```bash
/Applications/Python\ 3.12/Install\ Certificates.command
```
Poi rilancia il programma.

---

## 6. Esempio di output console

```
[1] Carico il dataset...
Prime 5 righe:
   Price  Area  Bedrooms  ...
0  133000  7420         4  ...
...
[2] Controllo valori mancanti...
Non ci sono valori mancanti.
...
[7] Avvio il workflow per cercare il modello migliore e valutarlo nel dettaglio...
============================================================
VALUTAZIONE: RIDGE (alpha=1.0)
============================================================
Metriche principali (test set):
  - MSE  : 123456.789
  - RMSE : 351.364
  - MAE  : 210.123
  - R²   : 0.8123
...
Report terminato.
```

---

## 7. Output generati

- **Tabella modelli** (CSV): R², MSE, RMSE, #coef non nulli, overfitting % per ogni combinazione provata.
- **Report testuale** in console del modello finale.
- **Grafici**:
  - Reale vs Predetto
  - Residui vs Predizioni
  - Istogramma residui
  - Top coefficienti (per modelli lineari)
  - Confronto bar-chart tra modelli sulla metrica scelta (es. R²)
- **Metriche modello migliore** salvate in JSON per riuso (presentazioni, report, ecc.).

---

## 8. Riferimenti utili

- [scikit-learn: Documentazione ufficiale](https://scikit-learn.org/stable/)
- [pandas: Documentazione ufficiale](https://pandas.pydata.org/docs/)
- [matplotlib: Documentazione ufficiale](https://matplotlib.org/stable/contents.html)
- [Dataset originale](https://www.kaggle.com/datasets/yasserh/housing-prices-dataset)

---




