#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# realestateAI/reg_models/utils.py

"""
Utility di base per il progetto di regressione regolarizzata.
Qui metto funzioni semplici che mi servono in più punti del codice.
"""

import numpy as np


def riempi_valori_mancanti(df, colonna):
    """
    Riempio i valori mancanti (NaN) di UNA singola colonna del DataFrame `df`.
    - Se la colonna è categorica (dtype == 'object') uso la moda (valore più frequente).
    - Se è numerica, uso la media aritmetica.
    Se la colonna non esiste nel DataFrame, non faccio nulla.
    Se la colonna è già piena (senza NaN), non faccio nulla
    """
    # Capisco il tipo della colonna per decidere come riempire i NaN
    tipo = df[colonna].dtype

    if tipo == 'object':
        # Uso la moda per le categorie
        moda = df[colonna].mode()[0]
        df[colonna].fillna(moda, inplace=True)
    else:
        # Per numerici, scelgo la media aritmetica
        media = df[colonna].mean()
        df[colonna].fillna(media, inplace=True)


def conta_coefficienti_non_nulli(modello, soglia=1e-8):
    """
    Conto quanti coefficienti del modello sono "diversi da zero" (in valore assoluto > soglia).
    Metto una soglia piccola per evitare di contare come zero valori molto piccoli dovuti a rounding.
    Se il modello non ha l'attributo `.coef_`, restituisco None.
    """
    if hasattr(modello, 'coef_'):
        # Uso np.abs per prendere il valore assoluto e confronto con la soglia.
        return int(np.sum(np.abs(modello.coef_) > soglia))
    else:
        return None


# =========================================================================
# Questo modulo raccoglie funzioni piccole e generiche che non appartengono
# direttamente a "modeling" o "plotting". Sono utility riutilizzabili.
# ==========================================================================