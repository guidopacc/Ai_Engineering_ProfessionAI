#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# realestateAI/reg_models/report.py

"""
Funzioni per creare report testuali e tabelle riassuntive dei risultati
(dei modelli testati o del modello scelto).
"""

import pandas as pd

def stampa_report(ris, nome_modello="Modello"):
    """
    Stampo su console (stdout) un report del dizionario `ris`.
    """
    # Uso print per mostrare tutte le metriche principali in modo ordinato.
    print("=" * 60)
    print(f"VALUTAZIONE: {nome_modello}")
    print("=" * 60)

    print("Metriche principali (test set):")
    print(f"  - MSE  : {ris['mse_test']:.3f}")
    print(f"  - RMSE : {ris['rmse_test']:.3f}")
    print(f"  - MAE  : {ris['mae_test']:.3f}")
    print(f"  - R²   : {ris['r2_test']:.4f}")

    print("\nConfronto train/test (per capire l'overfitting):")
    print(f"  - R² train: {ris['r2_train']:.4f}")
    print(f"  - R² test : {ris['r2_test']:.4f}")
    print(f"  - Differenza relativa: {ris['diff_overfit_rel']*100:.1f}%")

    if ris['n_coef_nonzero'] is not None:
        # Se il modello è lineare, mostro anche info sui coefficienti.
        print("\nAnalisi coefficienti (solo modelli lineari):")
        print(f"  - Totali     : {ris['n_coef_totali']}")
        print(f"  - Non nulli  : {ris['n_coef_nonzero']}")
        print(f"  - Sparsità % : {ris['sparsita_percentuale']:.1f}%")

    if ris['cv_mean'] is not None:
        # Se ho fatto cross-validation, mostro anche media e deviazione standard.
        print("\nCross Validation (sul TRAIN):")
        print(f"  - Media : {ris['cv_mean']:.3f}")
        print(f"  - Std   : {ris['cv_std']:.3f}")

    print("\nReport terminato.\n")


def risultati_in_dataframe(lista_risultati):
    """
    Converto una lista di dizionari (quelli prodotti da `ricerca_parametri`) in un DataFrame
    ordinato per confronto rapido.
    """
    rows = []
    for r in lista_risultati:
        # Estraggo solo le metriche e i parametri principali per ogni modello testato.
        rows.append({
            'modello': r.get('tipo_modello'),
            'alpha': r.get('alpha'),
            'l1_ratio': r.get('l1_ratio'),
            'r2_test': r['r2_test'],
            'rmse_test': r['rmse_test'],
            'mse_test': r['mse_test'],
            'coef_nonzero': r['n_coef_nonzero'],
            'sparsita_%': r['sparsita_percentuale'],
            'overfit_%': r['diff_overfit_rel'] * 100
        })

    df = pd.DataFrame(rows)
    # Ordino per modello e alpha per leggibilità
    df = df.sort_values(by=['modello', 'alpha']).reset_index(drop=True)
    return df

# ==========================================================================
# Il modulo permette di stampare e formattare i risultati in report 
# e tabelle riassuntive
# ==========================================================================