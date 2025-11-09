# Classificazione di Frutti Esotici con KNN

**Autore:** Guido Pacciani  
**Azienda:** TropicTaste Inc.  
**Contesto:** Automatizzazione della classificazione di frutti esotici per ottimizzare la gestione dell'inventario e ridurre errori manuali nel processo di distribuzione.

## Descrizione del Progetto

### Obiettivo
Questo progetto sviluppa un sistema di machine learning per classificare automaticamente il tipo di frutto esotico basandosi sulle sue caratteristiche numeriche (peso, diametro, lunghezza, durezza della buccia, dolcezza).

### Dataset
- **Fonte:** [Dataset frutti esotici](https://proai-datasets.s3.eu-west-3.amazonaws.com/fruits.csv)
- **Variabili:**
  - `Frutto`: Tipo di frutto (variabile target da prevedere)
  - `Peso (g)`: Peso del frutto in grammi
  - `Diametro medio (mm)`: Diametro medio in millimetri
  - `Lunghezza media (mm)`: Lunghezza media in millimetri
  - `Durezza buccia (1-10)`: Durezza della buccia su scala 1-10
  - `Dolcezza (1-10)`: Dolcezza del frutto su scala 1-10

### Modello
Utilizziamo l'algoritmo **K-Nearest Neighbors (KNN)** che classifica ogni frutto basandosi sui "vicini" più simili nel dataset di training. KNN è ideale per questo tipo di problema perché:
- Funziona bene con dati numerici
- È interpretabile (è possibile capire perché ha fatto una certa predizione)
- Non richiede assunzioni complesse sui dati

## Come Usare il Progetto (Google Colab)

### Passi per l'esecuzione:

1. **Carica tutti i file** del progetto nella cartella di lavoro di Google Colab
2. **Installa le dipendenze** (se necessario):
   ```bash
   !pip install pandas numpy scikit-learn matplotlib seaborn joblib
   ```
3. **Esegui il progetto**:
   ```bash
   !python main.py
   ```

### Output Attesi
Il sistema mostrerà:
• **Metriche di performance:** F1-score, Accuracy, Precision, Recall
• **Matrice di Confusione:** Visualizzazione degli errori di classificazione
• **Curve ROC** (Receiver Operating Characteristic): Se show_roc=True nel codice
• **Migliori Iperparametri:** Se il tuning è attivato (do_tune=True)
• **Modello Salvato:** File artifacts/knn_model.pkl (se abilitato)

## Struttura del Progetto

```
├── data_io.py       # Caricamento dataset e salvataggio modelli/metriche
├── preprocessing.py # Pulizia dati, split train/test, scalatura feature
├── model.py         # Costruzione Pipeline KNN e tuning iperparametri
├── metrics.py       # Calcolo metriche e creazione grafici di valutazione
├── train.py         # Orchestratore: coordina preprocessing, training e valutazione
├── main.py          # Punto di ingresso: carica dati, allena modello, valuta risultati
└── README.md        # Documentazione del progetto
```

### Descrizione Moduli

- **`data_io.py`**: Gestisce input/output (carica dataset da URL, salva modelli, metriche, grafici)
- **`preprocessing.py`**: Prepara i dati per l'addestramento (rimuove duplicati, fa split stratificato, applica StandardScaler)
- **`model.py`**: Costruisce la Pipeline KNN e gestisce il tuning degli iperparametri con GridSearchCV
- **`metrics.py`**: Calcola metriche di classificazione e crea visualizzazioni (matrice confusione, curve ROC)
- **`train.py`**: Orchestratore principale che coordina tutto il flusso end-to-end
- **`main.py`**: Script principale che lancia l'intero processo con parametri predefiniti

## Ordine di Lettura Consigliato

Per capire come funziona il progetto, leggi i moduli in questo ordine:

1. **`data_io.py`** → Come vengono caricati e salvati i dati
   - Inizia da `load_dataset()` per vedere il caricamento da URL/file
   - Poi `to_github_raw()` per la conversione URL GitHub
   - Infine `save_model()` e `save_metrics()` per il salvataggio

2. **`preprocessing.py`** → Come i dati vengono preparati
   - Inizia da `clean_data()` per vedere la pulizia base
   - Poi `train_test_split_df()` per lo split stratificato
   - Infine `build_preprocessor()` per la scalatura

3. **`model.py`** → Come il modello è costruito e allenato
   - Leggi `build_knn_pipeline()` per la costruzione della Pipeline
   - Poi `tune_model()` per il tuning degli iperparametri
   - Infine `fit_model()` per l'addestramento semplice

4. **`metrics.py`** → Come valutiamo le performance
   - Inizia da `compute_classification_metrics()` per le metriche base
   - Poi `plot_confusion_matrix()` per la visualizzazione
   - Infine `evaluate_classifier()` per la valutazione completa

5. **`train.py`** → Come tutto viene orchestrato
   - Leggi `prepare_data()` per vedere come i dati vengono preparati
   - Poi `train_and_evaluate()` per il flusso completo
   - Nota come coordina tutti i moduli precedenti

6. **`main.py`** → Come si lancia il progetto completo
   - Vedi come vengono configurati i parametri
   - Segui la funzione `run()` per il flusso completo
   - Nota la gestione degli errori e l'output strutturato

## Output e Interpretazione

### Metriche Principali

- **Accuracy**: Percentuale di predizioni corrette sul totale
- **Precision**: Tra i frutti predetti come "tipo X", quanti sono davvero di tipo X?
- **Recall**: Tra tutti i frutti di tipo X, quanti ne abbiamo trovati?
- **F1-Score**: Media armonica tra precision e recall (metrica bilanciata)

### Grafici

- **Matrice di Confusione**: Mostra dove il modello sbaglia (quali tipi di frutto confonde tra loro)
- **Curve ROC** (opzionale): Mostra il compromesso tra tasso di veri positivi e falsi positivi

### File Salvati

Se `SAVE_ARTIFACTS = True` in `main.py`:
- `artifacts/knn_model.pkl`: Modello addestrato (può essere ricaricato per nuove predizioni)
- `artifacts/metrics.json`: Metriche di performance in formato JSON

### Interpretazione dei Risultati

- **F1-Score > 0.8**: Ottimo risultato
- **F1-Score 0.6-0.8**: Buon risultato, ma c'è margine di miglioramento
- **F1-Score < 0.6**: Risultato da migliorare (prova tuning o più dati)

## Personalizzazione

### Modificare i Parametri

In `main.py` puoi cambiare:
- `DO_TUNE`: Attiva/disattiva il tuning degli iperparametri
- `TEST_SIZE`: Frazione di dati per il test (default: 0.2)
- `SCORING`: Metrica da ottimizzare (default: "f1_macro")
- `SHOW_CONFUSION`: Mostra/nasconde la matrice di confusione
- `SAVE_ARTIFACTS`: Salva/non salva il modello e le metriche

### Aggiungere Nuove Feature

1. Modifica il dataset per includere nuove colonne
2. Aggiorna `TARGET_COL` in `main.py` se necessario
3. Il sistema rileverà automaticamente le nuove colonne numeriche

## Autore e Licenza

**Autore:** Guido Pacciani  
**Licenza:** Nessuna licenza specifica

---

*Questo progetto è stato sviluppato per scopi didattici e di ricerca.*
