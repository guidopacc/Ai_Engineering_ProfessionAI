#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# realestateAI/reg_models/workflow.py

"""
Workflow compatto per eseguire la ricerca dei parametri, stampare il report,
mostrare i grafici e restituire tutti i risultati in un unico dizionario.
"""

import os, json
from .search import ricerca_parametri
from .report import stampa_report, risultati_in_dataframe
from .plots import plot_valutazione, plot_confronto_modelli
from .modeling import crea_modello, allena_e_valuta

def workflow_semplice(X_train, X_test, y_train, y_test,
                      r2_minimo=0.70,
                      max_overfit=0.15,
                      criterio='r2_test',
                      feature_names=None,
                      mostra_grafici=True,
                      save_dir="outputs"):
    """
    1) Ricerca parametri (senza CV per velocità)
    2) Seleziono il migliore e rifaccio allena_e_valuta con esegui_cv=True
    3) Stampo report + grafici
    4) Salvo tabella, metriche e figure su disco
    """

    # ------------------ 1. Ricerca parametri ------------------
    # Qui avvio la ricerca manuale degli iperparametri (alpha, l1_ratio) per tutti i modelli.
    risultati_ricerca = ricerca_parametri(
        X_train, X_test, y_train, y_test,
        r2_minimo=r2_minimo,
        max_overfit=max_overfit,
        criterio=criterio
    )
    best_raw = risultati_ricerca['migliore']   # dizionario con modello già allenato (senza CV)

    # ------------------ 2. Rifaccio training con CV sul migliore ------------------
    # Ricreo il modello con gli stessi iperparametri trovati nella ricerca.
    best_type   = best_raw.get('tipo_modello')
    best_alpha  = best_raw.get('alpha')
    best_l1     = best_raw.get('l1_ratio')

    modello_best = crea_modello(tipo_modello=best_type,
                                alpha=best_alpha,
                                l1_ratio=best_l1 if best_l1 is not None else 0.5)

    # Alleno + valuto con cross-validation attiva
    best_full = allena_e_valuta(modello_best,
                                X_train, X_test, y_train, y_test,
                                esegui_cv=True, cv_folds=5,
                                scoring_cv='neg_mean_squared_error')

    # Rimetto metadati utili nel dict finale
    best_full.update({'tipo_modello': best_type,
                      'alpha': best_alpha,
                      'l1_ratio': best_l1})

    # ------------------ 3. Report e grafici ------------------
    # Stampo un report dettagliato e genero i grafici di valutazione.
    nome = f"{best_type.upper()} (alpha={best_alpha}{'' if best_l1 is None else f', l1={best_l1}'} )"
    stampa_report(best_full, nome_modello=nome)

    # Creo cartella output se richiesta
    if save_dir is not None:
        os.makedirs(save_dir, exist_ok=True)

    # Grafico valutazione singolo modello
    fig_val, _ = plot_valutazione(best_full, y_test,
                                  feature_names=feature_names,
                                  mostra=mostra_grafici)

    if save_dir is not None:
        fig_val.savefig(os.path.join(save_dir, "fig_pred_residui.png"),
                        dpi=300, bbox_inches='tight')

    # Tabella di tutti i modelli
    df_ris = risultati_in_dataframe(risultati_ricerca['tutti'])
    if save_dir is not None:
        df_ris.to_csv(os.path.join(save_dir, "tabella_modelli.csv"), index=False)

    # Grafico confronto modelli
    metric_plot = criterio if criterio != 'sparsita' else 'sparsita_%'
    ax = plot_confronto_modelli(df_ris, metrica=metric_plot, mostra=mostra_grafici)
    if save_dir is not None and ax is not None:
        ax.figure.savefig(os.path.join(save_dir, "fig_confronto_modelli.png"),
                          dpi=300, bbox_inches='tight')

    # Salvo metriche del modello migliore in JSON
    if save_dir is not None:
        with open(os.path.join(save_dir, "migliore_metrics.json"), "w") as f:
            json.dump(best_full, f, indent=2, default=float)

    # Ritorno tutti i risultati utili in un dizionario, così posso usarli anche in notebook.
    return {
        'risultati_ricerca': risultati_ricerca,
        'migliore': best_full,
        'tabella_modelli': df_ris,
        'workflow_completato': True,
        'output_dir': save_dir
    }

# =============================================================================
# Questo modulo contiene la funzione "orchestra" che usa tutto il resto per
# fare il giro completo (ricerca → report → grafici → tabella).
# =============================================================================