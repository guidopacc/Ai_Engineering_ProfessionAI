# TropicTaste Inc. — Classificazione di frutti esotici
## Classificazione automatica con K-Nearest Neighbors

---

## Descrizione

Il progetto implementa un sistema di machine learning per classificare automaticamente frutti esotici in base alle loro caratteristiche fisiche (peso, diametro, lunghezza, durezza della buccia, dolcezza). L'obiettivo è automatizzare un processo di classificazione manuale per ottimizzare la gestione dell'inventario e ridurre gli errori in fase di distribuzione.

L'algoritmo scelto è **K-Nearest Neighbors (KNN)**, che assegna a ogni campione la classe più frequente tra i suoi k vicini più simili nello spazio delle feature.

---

## Autore e contesto

**Autore:** Guido Pacciani  
Sviluppato come progetto finale del modulo *"Machine Learning: Modelli e Algoritmi"* del **Master Professionale in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

---

## Dataset

- **Fonte:** [https://proai-datasets.s3.eu-west-3.amazonaws.com/fruits.csv](https://proai-datasets.s3.eu-west-3.amazonaws.com/fruits.csv)
- **Variabili di input:** `Peso (g)`, `Diametro medio (mm)`, `Lunghezza media (mm)`, `Durezza buccia (1-10)`, `Dolcezza (1-10)`
- **Variabile target:** `Frutto` (tipo di frutto esotico)

---

## Struttura del progetto

```
TropicTaste Inc./
├── data_io.py        # Caricamento dataset e salvataggio modelli/metriche
├── preprocessing.py  # Pulizia dati, split train/test stratificato, scalatura feature
├── model.py          # Costruzione Pipeline KNN e tuning iperparametri
├── metrics.py        # Calcolo metriche e visualizzazioni (matrice di confusione, ROC)
├── train.py          # Orchestratore: coordina preprocessing, training e valutazione
├── main.py           # Punto di ingresso con parametri configurabili
└── README.md
```

---

## Requisiti e installazione

```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib
```

---

## Come eseguire

### Su Google Colab

1. Carica tutti i file nella cartella di lavoro
2. Installa le dipendenze: `!pip install pandas numpy scikit-learn matplotlib seaborn joblib`
3. Esegui: `!python main.py`

### In locale

```bash
python main.py
```

---

## Output attesi

- **Metriche di classificazione:** Accuracy, Precision, Recall, F1-score
- **Matrice di confusione:** visualizzazione grafica degli errori di classificazione
- **Curve ROC** (opzionale, se `SHOW_ROC=True` in `main.py`)
- **Modello salvato** in `artifacts/knn_model.pkl` (se `SAVE_ARTIFACTS=True`)

---

## Personalizzazione

I parametri principali sono configurabili in `main.py`:
- `DO_TUNE`: attiva/disattiva il tuning degli iperparametri con GridSearchCV
- `TEST_SIZE`: proporzione dei dati per il test set (default: 0.2)
- `SCORING`: metrica da ottimizzare durante il tuning (default: `f1_macro`)
- `SHOW_CONFUSION`: mostra/nasconde la matrice di confusione
- `SAVE_ARTIFACTS`: salva modello e metriche su disco

---

## Approfondimento tecnico

### Pipeline scikit-learn

Il modello è costruito come una `Pipeline` scikit-learn che incapsula due passi:
1. **`StandardScaler`**: normalizza le feature sottraendo la media e dividendo per la deviazione standard, necessario per KNN che si basa sulle distanze euclidee
2. **`KNeighborsClassifier`**: il classificatore vero e proprio

Usare una Pipeline garantisce che la scalatura venga applicata coerentemente su train e test set, evitando data leakage.

### Tuning degli iperparametri

Con `DO_TUNE=True`, il parametro `k` (numero di vicini) viene ottimizzato tramite **GridSearchCV** con cross-validation stratificata. La stratificazione assicura che ogni fold abbia la stessa distribuzione delle classi del dataset originale.

### Metriche

Il sistema usa `f1_macro` come metrica principale: calcola l'F1-score per ciascuna classe e ne fa la media non pesata, dando lo stesso peso a tutte le classi indipendentemente dalla loro frequenza.

### Struttura modulare

La separazione in moduli (`data_io`, `preprocessing`, `model`, `metrics`, `train`) permette di riutilizzare singoli componenti e facilita i test unitari. `train.py` agisce da orchestratore che conosce solo i contratti tra moduli, non i dettagli implementativi.

---

## Interpretazione dei risultati

- **F1-Score > 0.8**: performance buone
- **F1-Score 0.6–0.8**: margine di miglioramento (prova tuning o più dati)
- **F1-Score < 0.6**: da investigare (verifica la qualità dei dati o il bilanciamento delle classi)

---

## Riferimenti

- [scikit-learn — KNeighborsClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)
- [scikit-learn — Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)

---

## Licenza

Rilasciato con licenza **MIT** — libero per uso personale, studio o sviluppo. Clona e modifica liberamente.
