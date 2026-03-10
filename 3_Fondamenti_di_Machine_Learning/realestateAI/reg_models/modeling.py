#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: realestateAI/reg_models/modeling.py

"""
Funzioni per costruire (crea_modello), allenare e valutare (allena_e_valuta) modelli di
regressione regolarizzata.
"""

import numpy as np
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score

from .utils import conta_coefficienti_non_nulli


def crea_modello(tipo_modello='ridge', alpha=1.0, l1_ratio=0.5, max_iter=2000):
    """
    Creo e restituisco un modello di regressione regolarizzata scelto tra:
    - 'ridge'
    - 'lasso'
    - 'elastic_net'
    Di default la funzione esegue la regressione con regolarizzazione Ridge.

    Parametri:
    - tipo_modello: stringa che indica il tipo di modello da creare.
    - alpha: parametro di regolarizzazione (più alto = più penalità).
    - l1_ratio: solo per ElasticNet, bilancia tra L1 e L2
      (1.0 = Lasso puro, 0.0 = Ridge puro, valori intermedi combinano le due penalità).
    - max_iter: numero massimo di iterazioni per l'ottimizzazione (utile per
      modelli complessi come Lasso/ElasticNet che possono richiedere più iterazioni
      per convergere).
    """
    tipo_modello = tipo_modello.lower()  # Mi assicuro che il confronto sia case-insensitive

    if tipo_modello == 'ridge':
        # Creo un modello di regressione Ridge.
        # Ridge aggiunge una penalità L2 alla somma dei quadrati dei coefficienti.
        # Questo aiuta a ridurre l'overfitting, soprattutto quando le feature sono molte o collineari.
        # Più alpha è grande, più i coefficienti vengono "spinti" verso zero (ma mai annullati del tutto).
        return Ridge(alpha=alpha)
        # ---
        # Utile quando tutte le feature sono potenzialmente informative.
        # ---
    elif tipo_modello == 'lasso':
        # Creo un modello di regressione Lasso.
        # Lasso aggiunge una penalità L1 (somma dei valori assoluti dei coefficienti).
        # Questo porta molti coefficienti esattamente a zero, selezionando solo le feature più importanti.
        # L'argomento max_iter serve per evitare che l'ottimizzazione si blocchi in caso di dataset complessi.
        return Lasso(alpha=alpha, max_iter=max_iter)
        # ---
        # Utile quando solo alcune variabili sono davvero rilevanti.
        # ---
    elif tipo_modello == 'elastic_net':
        # Creo un modello ElasticNet, che combina le penalità L1 (Lasso) e L2 (Ridge).
        # Il parametro l1_ratio controlla il bilanciamento tra L1 e L2:
        # - l1_ratio=1 equivale a Lasso
        # - l1_ratio=0 equivale a Ridge
        return ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=max_iter)
        # ---
        # Utile quando ho molte feature correlate e voglio sia selezione che stabilità.
        # ---
    else:
        raise ValueError("Tipo modello non riconosciuto. Usa 'ridge', 'lasso' o 'elastic_net'.")


def allena_e_valuta(modello,
                    X_train, X_test, y_train, y_test,               # Dati di addestramento e test
                    esegui_cv=True,
                    cv_folds=5,                                     # Numero di fold per la cross-validation (di default 5)
                    scoring_cv='neg_mean_squared_error'):           # Metrica per la cross-validation (di default MSE negativo)
    """
    Alleno il modello, genero predizioni su train e test e calcolo metriche.
    Posso anche lanciare una cross-validation sul train per stimare meglio le performance.

    Ritorno un dizionario di info, da usare per report e grafici.
    """
    # Alleno il modello con i dati di training
    # fit() trova i coefficienti migliori minimizzando la funzione di costo regolarizzata.
    modello.fit(X_train, y_train)

    # Predizioni su training e test
    # Uso il modello allenato per prevedere sia sui dati di training che di test.
    y_pred_train = modello.predict(X_train)
    y_pred_test = modello.predict(X_test)

    # Metriche principali
    # Calcolo le metriche di errore e di bontà del fit.
    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)

    # Differenza relativa R² per stimare overfitting
    # Se la differenza tra R² train e test è grande, il modello sta overfittando.
    if r2_train != 0:
        diff_relativa = abs((r2_train - r2_test) / r2_train)
    else:
        diff_relativa = np.inf  # se R² train è 0, non ha senso calcolare la differenza relativa

    # Inizializzo le variabili legate ai coefficienti
    n_nonzero = None
    tot_coef = None

    # Se il modello ha l'attributo coef_ (quindi è lineare), posso analizzare i coefficienti
    if hasattr(modello, 'coef_'):
        tot_coef = len(modello.coef_)
        n_nonzero = conta_coefficienti_non_nulli(modello)

    # Cross-validation sul TRAIN (opzionale, di default è True, quindi viene eseguita)
    # Inizializzo le variabili che conterranno i risultati della validazione incrociata.
    # Lo faccio subito per evitare errori nel caso in cui non venga eseguita.
    cv_mean = None
    cv_std = None
    cv_scores = None

    # Se ho attivato la cross-validation (di default è True), procedo a calcolarla.
    if esegui_cv:
        # Eseguo la validazione incrociata sul training set.
        # Il modello viene allenato e testato su diverse suddivisioni (folds) dei dati.
        scores = cross_val_score(
            modello,            
            X_train, y_train,   # i dati di addestramento
            cv=cv_folds,        # numero di fold da usare (es. 5 o 10)
            scoring=scoring_cv  # metrica di valutazione (es. R², MSE, ecc.)
        )

        # Alcune metriche (come MSE o il log loss) vengono restituite come valori negativi da sklearn
        # per uniformare la logica "più è alto meglio è" → inverto il segno se necessario
        if scoring_cv.startswith('neg_'):
            scores = -scores    # così ottengo i veri valori della metrica (positivi)

        # Salvo i risultati completi (uno per ciascun fold)
        cv_scores = scores

        # Calcolo la media dei punteggi ottenuti nei vari fold
        cv_mean = scores.mean()

        # Calcolo anche la deviazione standard, per capire quanto i risultati sono stabili tra i fold
        cv_std = scores.std()

    # Impacchetto tutto in un dict
    # Raccolgo tutte le metriche e le predizioni in un dizionario per analisi successive.
    risultati = {
        'modello': modello,
        'y_pred_train': y_pred_train,
        'y_pred_test': y_pred_test,
        'mse_train': mse_train,
        'mse_test': mse_test,
        'rmse_test': rmse_test,
        'mae_test': mae_test,
        'r2_train': r2_train,
        'r2_test': r2_test,
        'diff_overfit_rel': diff_relativa,
        'n_coef_nonzero': n_nonzero,
        'n_coef_totali': tot_coef,
        'sparsita_percentuale': (1 - n_nonzero / tot_coef) * 100 if (n_nonzero is not None and tot_coef) else None,
        'cv_mean': cv_mean,
        'cv_std': cv_std,
        'cv_scores': cv_scores,
    }

    return risultati

# ===============================================================
# Questo modulo contiene funzioni per creare e valutare modelli di 
# regressione regolarizzata come Ridge, Lasso ed ElasticNet.
# Nota: Non include ricerca iperparametri o grafici, solo creazione e 
# valutazione dei modelli.
# ===============================================================