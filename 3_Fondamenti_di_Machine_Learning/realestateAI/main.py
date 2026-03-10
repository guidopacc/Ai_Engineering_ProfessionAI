#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# realestateAI/main.py

# Questo script è il punto di partenza del progetto Real Estate AI.
# Serve per caricare i dati, prepararli e avviare il workflow di ricerca del modello migliore.

# ==============================
# 1. IMPORT DELLE LIBRERIE BASE
# ==============================

import pandas as pd
import numpy as np

# Librerie per grafici di supporto (anche se la maggior parte delle funzioni di plot è nel pacchetto)
import matplotlib.pyplot as plt

# Strumenti di scikit-learn per split e scaling
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Importo le funzioni dal mio pacchetto locale `reg_models`
# (Assumo di essere nella cartella realestateAI/ quando eseguo questo file)
from reg_models import (
    riempi_valori_mancanti,
    workflow_semplice
)

# ==============================
# 2. PARAMETRI GLOBALI DELLO SCRIPT
# ==============================
# Qui imposto i parametri che mi servono in tutto lo script, come il seed per la riproducibilità e l'URL del dataset.
RANDOM_SEED = 0

# URL del dataset
DATA_URL = "https://proai-datasets.s3.eu-west-3.amazonaws.com/housing.csv"

# Nome della colonna target da prevedere (nel dataset è 'price')
TARGET_COL = 'price'

# Lista delle colonne categoriche da trasformare con one-hot encoding
CAT_COLS = ['furnishingstatus']


# ==============================
# 3. FUNZIONE MAIN
# ==============================
# Questa funzione racchiude tutto il flusso principale: dal caricamento dati alla valutazione dei modelli.
def main():
    """
    Funzione principale che esegue il workflow completo.
    """
    # 3.1 Carico il dataset da CSV
    print("\n[1] Carico il dataset...")
    df = pd.read_csv(DATA_URL)  # Qui scarico direttamente il file CSV da internet

    # 3.2 Controllo rapido info per capire la struttura
    # Mi assicuro che il dataset sia stato caricato correttamente e ne visualizzo le prime righe.
    print("Prime 5 righe:")
    print(df.head())
    print("\nInfo dataset:")
    print(df.info())

    # 3.3 Verifico se ci sono valori mancanti
    print("\n[2] Controllo valori mancanti...")
    missing_total = df.isnull().sum().sum()
    if missing_total == 0:
        print("Non ci sono valori mancanti.")
    else:
        print("Valori mancanti per colonna:")
        print(df.isnull().sum())
        print("\nRiempio i valori mancanti (media per numerici, moda per categorici)...")
        # Uso la funzione riempi_valori_mancanti per riempire i NaN in modo semplice e automatico.
        for col in df.columns:
            if df[col].isnull().any():  # se la colonna ha almeno un NaN
                riempi_valori_mancanti(df, col)
        print("Ricontrollo:")
        print(df.isnull().sum())

    # 3.4 One-hot encoding delle categorie
    # Devo trasformare le colonne categoriche in numeriche (dummy variables) per i modelli lineari.
    # Uso pd.get_dummies che crea una colonna per ogni categoria (tranne la prima, per evitare collinearità).
    print("\n[3] One-hot encoding delle colonne categoriche:", CAT_COLS)
    df = pd.get_dummies(df, columns=CAT_COLS, drop_first=True)

    # 3.5 Separazione feature/target
    # Divido il DataFrame in X (feature) e y (target) per preparare i dati al modello.
    print("\n[4] Separazione feature (X) e target (y)...")
    X = df.drop(TARGET_COL, axis=1)
    y = df[TARGET_COL]
    print(f"X shape: {X.shape} | y shape: {y.shape}")

    # 3.6 Standardizzazione delle feature
    # Standardizzo le feature per avere media 0 e deviazione standard 1 (per migliorare la convergenza dei modelli).
    print("\n[5] Standardizzo le feature con StandardScaler (media=0, std=1)...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3.7 Train/Test split
    # Divido i dati in train e test (70%/30%) per poter valutare i modelli su dati non visti.
    # Uso un seed fisso per avere risultati riproducibili.
    print("\n[6] Train/Test split dei dati (70% train, 30% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.3, random_state=RANDOM_SEED
    )
    print(f"Training set: {X_train.shape[0]} righe")
    print(f"Test set    : {X_test.shape[0]} righe")

    # 3.8 Avvio workflow completo (ricerca parametri + report + grafici + tabella)
    # Qui chiamo la funzione che: ricerca il miglior modello, stampa report, mostra grafici e salva i risultati.
    print("\n[7] Avvio il workflow per cercare il modello migliore e valutarlo nel dettaglio...")
    risultati = workflow_semplice(
        X_train, X_test, y_train, y_test,
        r2_minimo=0.70,          # soglia minima per R² sul test
        max_overfit=0.15,        # massimo overfitting relativo accettato
        criterio='r2_test',      # criterio di selezione del modello
        feature_names=X.columns, # nomi delle feature per i plot dei coefficienti
        mostra_grafici=True,     # se False non mostra i grafici a schermo
        save_dir="outputs"       # directory dove salvo CSV/JSON/figure
    )

    # 3.9 Salvo opzionalmente i risultati in CSV
    print("\n[8] Salvo i risultati del confronto modelli in un CSV (tabella_modelli.csv)...")
    risultati['tabella_modelli'].to_csv('tabella_modelli.csv', index=False)
    print("CSV salvato nella cartella corrente.")

    print("\nWorkflow completato correttamente.\n")


# ==============================
# 4. ESECUZIONE SCRIPT
# ==============================
# Qui faccio partire la funzione main solo se eseguo direttamente questo file.
if __name__ == "__main__":
    main()
