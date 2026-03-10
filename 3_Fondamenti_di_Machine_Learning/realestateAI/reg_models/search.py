#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# realestateAI/reg_models/search.py

"""
Ricerca manuale dei parametri (alpha e l1_ratio) per Ridge/Lasso/Elastic Net.
"""

import numpy as np
from .modeling import crea_modello, allena_e_valuta


def ricerca_parametri(X_train, X_test, y_train, y_test,
                      tipi_modello=("ridge", "lasso", "elastic_net"),
                      alpha_values=(0.001, 0.01, 0.1, 1, 10, 100),
                      l1_ratio_values=(0.2, 0.5, 0.8),
                      r2_minimo=0.70, 
                      max_overfit=0.15,
                      criterio='r2_test'):     # Criterio per il modello migliore: 'r2_test', 'rmse_test', 'sparsita', di default 'r2_test'
    """
    Faccio una piccola grid-search manuale:
    - ciclo sui modelli e sugli alpha
    - per Elastic Net ciclo anche sugli l1_ratio
    - per ogni combinazione alleno e valuto un modello
    - filtro i modelli che superano i vincoli su R² e overfitting
    - scelgo il migliore in base al criterio specificato
    """
    tutti = []  # Qui salvo tutti i risultati, anche quelli che non rispettano i vincoli
    validi = [] # Qui salvo solo i modelli che rispettano i vincoli di qualità

    for tipo in tipi_modello:
        for alpha in alpha_values:
            if tipo == 'elastic_net':
                # Elastic Net richiede anche l1_ratio
                for l1 in l1_ratio_values:
                    # Creo il modello con i parametri correnti
                    modello = crea_modello(tipo_modello=tipo, alpha=alpha, l1_ratio=l1)
                    # Alleno e valuto il modello
                    res = allena_e_valuta(modello, X_train, X_test, y_train, y_test, esegui_cv=False)
                    # Aggiungo info sui parametri usati
                    res.update({'tipo_modello': tipo, 'alpha': alpha, 'l1_ratio': l1})
                    tutti.append(res)

                    # Controllo i vincoli: voglio solo modelli con R²_test >= r2_minimo
                    # e differenza di overfitting relativa <= max_overfit
                    if (res['r2_test'] >= r2_minimo) and (res['diff_overfit_rel'] <= max_overfit):
                        validi.append(res)
            else:
                # Ridge e Lasso non hanno l1_ratio
                modello = crea_modello(tipo_modello=tipo, alpha=alpha)
                res = allena_e_valuta(modello, X_train, X_test, y_train, y_test, esegui_cv=False)
                res.update({'tipo_modello': tipo, 'alpha': alpha, 'l1_ratio': None})
                tutti.append(res)

                # Controllo i vincoli: voglio solo modelli con R²_test >= r2_minimo
                # e differenza di overfitting relativa <= max_overfit
                if (res['r2_test'] >= r2_minimo) and (res['diff_overfit_rel'] <= max_overfit):
                    validi.append(res)

    # Se non ho modelli "validi", scelgo comunque il migliore per R²_test
    if len(validi) == 0:
        # Scelgo comunque il miglior modello, anche se nessuno ha superato i vincoli.
        # Uso max() con key=lambda per cercare il dizionario in 'tutti' con il valore massimo di R²_test.
        # La lambda prende ogni dizionario e ne estrae 'r2_test' come criterio di confronto.
        migliore = max(tutti, key=lambda d: d['r2_test']) if len(tutti) > 0 else None
        return {
            'successo': False,
            'migliore': migliore,
            'tutti': tutti,
            'validi': validi,
            'messaggio': 'Nessun modello soddisfa i vincoli. Restituisco il migliore per R².'
        }

    # Definisco la funzione chiave per il criterio di selezione finale
    # Posso scegliere il modello migliore in base a R², RMSE o sparsità.
    if criterio == 'r2_test':
        key_fun = lambda d: d['r2_test']
    elif criterio == 'rmse_test':
        key_fun = lambda d: -d['rmse_test']  # RMSE minore → meglio
    elif criterio == 'sparsita':
        key_fun = lambda d: d['sparsita_percentuale'] if d['sparsita_percentuale'] is not None else -np.inf
    else:
        key_fun = lambda d: d['r2_test']  # default

    migliore = max(validi, key=key_fun)

    return {
        'successo': True,
        'migliore': migliore,
        'tutti': tutti,
        'validi': validi,
        'messaggio': 'Ricerca completata con successo.'
    }


# =============================================================
# Questo modulo contiene la logica per la ricerca manuale
# dei parametri per i modelli di regressione (Ridge, Lasso, Elastic Net).
# Si occupa di:
# - Creare i modelli con i parametri specificati
# - Allenarli e valutarli sui dati di addestramento e test
# - Applicare filtri sui risultati in base a vincoli di R² e overfitting
# - Restituire il modello migliore in base a un criterio specificato
# - Fornire un riepilogo dei risultati della ricerca
# - Gestire casi in cui nessun modello soddisfa i vincoli
# ==============================================================