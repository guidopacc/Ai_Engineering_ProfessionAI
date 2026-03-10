#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# realestateAI/reg_models/__init__.py

# Definisco esplicitamente quali funzioni e moduli voglio esporre quando qualcuno importa il pacchetto.
__all__ = [
    # === utils.py ===
    'riempi_valori_mancanti',
    'conta_coefficienti_non_nulli',

    # === modeling.py ===
    'crea_modello',
    'allena_e_valuta',

    # === search.py ===
    'ricerca_parametri',

    # === report.py ===
    'stampa_report',
    'risultati_in_dataframe',

    # === plots.py ===
    'plot_valutazione',
    'plot_confronto_modelli',

    # === workflow.py ===
    'workflow_semplice'
]

# Importo e rendo accessibili le funzioni definite nei moduli interni
from .utils import riempi_valori_mancanti, conta_coefficienti_non_nulli
from .modeling import crea_modello, allena_e_valuta
from .search import ricerca_parametri
from .report import stampa_report, risultati_in_dataframe
from .plots import plot_valutazione, plot_confronto_modelli
from .workflow import workflow_semplice

# ===========================================================================================================
# Questo file viene eseguito automaticamente da Python quando importo il pacchetto `reg_models`.
# Con esso comunico a Python: "Questa cartella è un pacchetto", quindi può essere usata con `import`.

# - Grazie a questo file posso:
#   ✔ Esportare solo le funzioni che mi interessano (senza doverle importare una per una).
#   ✔ Organizzare i miei moduli interni (`utils.py`, `modeling.py`, ecc.) in modo ordinato.
#   ✔ Importare da fuori con una sintassi comoda:
#         from reg_models import crea_modello, workflow_semplice
#     invece di dover scrivere:
#         from reg_models.modeling import crea_modello
#
# - La variabile `__all__` specifica esattamente cosa viene esposto se qualcuno usa:
#         from reg_models import *
#
# - Le righe con `from .modulo import funzione` servono a portare le funzioni dal modulo interno al livello del pacchetto.
#
# In pratica: questo file è come una “vetrina” che mostra solo le funzioni che voglio far usare al mondo esterno.
# ===========================================================================================================