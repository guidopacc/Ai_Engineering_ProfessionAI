#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# realestateAI/reg_models/plots.py

"""
Funzioni di plotting: grafici di valutazione del singolo modello e confronto tra modelli.
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_valutazione(ris, 
                     y_test, 
                     feature_names=None, # Lista dei nomi delle feature, se disponibili
                     top_n=10,           # Numero di coefficienti da mostrare
                     mostra=True):
    """
    Creo 4 grafici per analizzare un modello:
    1) Valori reali vs predetti
    2) Residui vs predizioni
    3) Istogramma dei residui
    4) Top N coefficienti (se disponibili)
    """
    y_pred = ris['y_pred_test']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Valutazione modello', fontsize=16)

    # 1. Reale vs Predetto
    # Qui confronto i valori reali con quelli predetti: se il modello è buono, i punti stanno vicino alla diagonale.
    axes[0, 0].scatter(y_test, y_pred, alpha=0.6)
    minimo = min(y_test.min(), y_pred.min())
    massimo = max(y_test.max(), y_pred.max())
    axes[0, 0].plot([minimo, massimo], [minimo, massimo], 'r--')
    axes[0, 0].set_xlabel('Valori reali')
    axes[0, 0].set_ylabel('Valori predetti')
    axes[0, 0].set_title('Reale vs Predetto')

    # 2. Residui vs Predizioni
    # Analizzo la distribuzione degli errori (residui) rispetto alle predizioni: cerco pattern o outlier.
    residui = y_test - y_pred
    axes[0, 1].scatter(y_pred, residui, alpha=0.6, color='green')
    axes[0, 1].axhline(0, color='red', linestyle='--')
    axes[0, 1].set_xlabel('Predizioni')
    axes[0, 1].set_ylabel('Residui (reale - predetto)')
    axes[0, 1].set_title('Residui vs Predizioni')

    # 3. Istogramma dei residui
    # Un buon modello ha residui distribuiti simmetricamente attorno a zero.
    axes[1, 0].hist(residui, bins=25, edgecolor='black', alpha=0.7)
    axes[1, 0].axvline(0, color='red', linestyle='--')
    axes[1, 0].set_xlabel('Residui')
    axes[1, 0].set_ylabel('Frequenza')
    axes[1, 0].set_title('Distribuzione residui')

    # 4. Coefficienti principali
    # Visualizzo i coefficienti più "importanti" (in valore assoluto) se disponibili.
    if ris['n_coef_nonzero'] is not None and feature_names is not None:
        coef = ris['modello'].coef_
        indici = np.argsort(np.abs(coef))[-top_n:]
        axes[1, 1].barh(range(len(indici)), coef[indici])
        axes[1, 1].set_yticks(range(len(indici)))
        axes[1, 1].set_yticklabels([feature_names[i] for i in indici])
        axes[1, 1].set_xlabel('Valore coefficiente')
        axes[1, 1].set_title(f'Top {top_n} coefficienti')
    else:
        axes[1, 1].text(0.5, 0.5, 'Coefficienti non disponibili', ha='center')
        axes[1, 1].set_axis_off()

    plt.tight_layout()
    if mostra:
        plt.show()
    return fig, axes


def plot_confronto_modelli(df_ris, metrica='r2_test', mostra=True):
    """
    Creo un bar plot per confrontare visivamente i modelli in base a una metrica scelta (default: R² sul test).
    Il DataFrame `df_ris` deve essere stato generato con la funzione risultati_in_dataframe().
    
    Parametri:
    - metrica: il nome della colonna del DataFrame da usare come altezza delle barre (es. 'r2_test', 'rmse').
    - mostra: se True, mostro subito il grafico; se False, ritorno solo l’oggetto Axes per personalizzazioni esterne.

    Ritorna:
    - Axes matplotlib dell’ultimo grafico creato.
    """

    # Se il DataFrame è vuoto, interrompo tutto e avverto l'utente
    if df_ris.empty:
        print("DataFrame vuoto. Impossibile creare il grafico.")
        return None

    # Definisco una funzione interna che prende una riga del DataFrame e costruisce una stringa leggibile
    def formatta_etichetta(riga):
        # Converto il modello in stringa (es. Ridge(), Lasso(), ElasticNet())
        nome_modello = str(riga['modello'])

        # Formatto il valore di alpha con 2 decimali
        alpha = f"{riga['alpha']:.2f}"

        # Se l1_ratio è NaN (cioè non esiste: tipico per Ridge o Lasso), costruisco etichetta senza l1
        if pd.isna(riga['l1_ratio']):
            return f"{nome_modello}\nα={alpha}"
        else:
            # Altrimenti aggiungo anche l1_ratio, anch'esso con 2 decimali
            l1_ratio = f"{riga['l1_ratio']:.2f}"
            return f"{nome_modello}\nα={alpha}, l1={l1_ratio}"

    # Applico la funzione a ogni riga del DataFrame per creare tutte le etichette
    etichette = df_ris.apply(formatta_etichetta, axis=1)

    # Costruisco il grafico a barre

    # Imposto dimensione del grafico
    plt.figure(figsize=(12, 5))

    # Creo il bar plot usando le etichette come ascisse e i valori metrici come altezze
    plt.bar(etichette, df_ris[metrica])

    # Ruoto le etichette sull'asse x per migliorare la leggibilità
    plt.xticks(rotation=45, ha='right')

    # Aggiungo etichette e titolo
    plt.ylabel(metrica)
    plt.title(f'Confronto modelli - {metrica}')
    plt.tight_layout()  # Ottimizza la disposizione degli elementi grafici

    # Mostro il grafico solo se richiesto
    if mostra:
        plt.show()

    # Ritorno l'oggetto Axes per eventuali modifiche o salvataggi successivi
    return plt.gca()

# =======================================================================
# Questo modulo contiene tutte le funzioni che creano grafici.
# In questo modo riduco la modifica dello stile dei plot ad un unico file.
# =======================================================================