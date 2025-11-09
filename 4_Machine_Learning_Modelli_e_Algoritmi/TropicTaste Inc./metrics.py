from __future__ import annotations

"""
metrics.py
----------

Valutazione e visualizzazione per classificazione multiclasse.
Metriche: accuracy, precision, recall, F1 + grafici (CM, ROC).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Any, Literal, Mapping
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
)


# ------------------------------------------------------------
# Calcolo metriche multiclasse
# ------------------------------------------------------------

def compute_classification_metrics(
    y_true: np.ndarray | pd.Series,
    y_pred: np.ndarray | pd.Series,
    *,
    average: Literal["macro", "micro", "weighted"] = "macro",   # accetta solo questi tre valori
    labels: list[str] | np.ndarray | None = None,               # (opzionale) classi da includere/ordinare
    digits: int = 3                                             # numero di decimali nelle metriche aggregate
) -> dict[str, Any]:
    """
    Calcola metriche principali di classificazione multiclasse.
    Ogni sample (riga) contiene delle feature (colonne) e deve essere associato dal modello
    a una classe (una sola etichetta nella colonna target). Se le etichette sono più di due
    (es. "mela", "pera", "banana", "kiwi"), si parla di classificazione multiclasse.

    Parametri:
        y_true: Etichette vere.
        y_pred: Predizioni del modello.
        average: Tipo di media per precision/recall/f1 ("macro", "micro", "weighted").
        labels: Nomi delle classi per il report dettagliato/ordine.
        digits: Cifre decimali per il report.

    Ritorna:
        dict: Dizionario con metriche:
            - accuracy: quota di predizioni corrette sul totale
            - precision: media (secondo 'average') della precision
            - recall: media (secondo 'average') del recall
            - f1: media (secondo 'average') della F1
            - report_dict: metriche per classe (+ macro_avg se disponibile)

    Note:
        - accuracy: sul totale delle predizioni, quante sono corrette
        - precision: tra i campioni predetti in una classe, quanti sono davvero di quella classe? (↓ falsi positivi)
        - recall: tra i campioni di una classe, quanti vengono trovati? (↓ falsi negativi)
        - f1: media armonica di precision e recall (bassa se una delle due è bassa)
        - macro: media semplice tra classi (ogni classe pesa uguale)
        - weighted: media pesata per frequenza delle classi
        - micro: calcolo globale aggregando TP/FP/FN
    """
    # Metriche globali
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average=average, zero_division=0)
    recall = recall_score(y_true, y_pred, average=average, zero_division=0)
    f1 = f1_score(y_true, y_pred, average=average, zero_division=0)

    # Report dettagliato per classe in formato dizionario
    report_raw = classification_report(
        y_true, y_pred,
        labels=labels,
        digits=digits,
        zero_division=0,
        output_dict=True # se True, output in formato dizionario
    )

    # Crea dizionario finale con solo le classi reali
    report_dict = {}
    for class_name, metrics in report_raw.items():                                  # .items() restituisce coppie (chiave, valore)
        if class_name in ("accuracy", "macro avg", "weighted avg", "micro avg"):
            continue
        report_dict[class_name] = {
            "precision": float(metrics["precision"]),
            "recall": float(metrics["recall"]),
            "f1-score": float(metrics["f1-score"]),
            "support": int(metrics["support"])
        }

    # Aggiunge macro_avg se presente
    if "macro avg" in report_raw:
        m = report_raw["macro avg"]
        report_dict["macro_avg"] = {
            "precision": float(m["precision"]),
            "recall": float(m["recall"]),
            "f1-score": float(m["f1-score"]),
            "support": int(m["support"])
        }

    # Restituisce metriche globali + dettagli per classe
    return {
        "accuracy": round(accuracy, digits),
        "precision": round(precision, digits),
        "recall": round(recall, digits),
        "f1": round(f1, digits),
        "report_dict": report_dict
    }

# ------------------------------------------------------------
# Visualizzazioni
# ------------------------------------------------------------

def plot_confusion_matrix(
    y_true: np.ndarray | pd.Series,
    y_pred: np.ndarray | pd.Series,
    *,
    labels: list[str] | np.ndarray | None = None,   # ordine o sottoinsieme di etichette da mostrare; se None, le ricava automaticamente
    title: str = "Matrice di Confusione (Test)"
) -> None:
    """
    Heatmap matrice confusione: righe=reali, colonne=predette.
    Diagonale=corretti, fuori diagonale=errori.
    """
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    # Se labels è None, usa le classi uniche

    if labels is None:
        unique_labels = sorted(np.unique(np.concatenate([y_true, y_pred]))) # Se l’utente non ha fornito labels, la funzione prende tutte le classi presenti
                                                                            # in y_true e y_pred, le unisce (np.concatenate), elimina duplicati (np.unique) e le ordina (sorted)
    else:
        unique_labels = labels
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm, 
        annot=True, 
        fmt='d', 
        cmap='Blues',
        xticklabels=unique_labels,
        yticklabels=unique_labels,
        cbar_kws={'label': 'Numero di campioni'}
    )
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Predizioni', fontsize=12)
    plt.ylabel('Valori veri', fontsize=12)
    plt.tight_layout()
    plt.show()


def plot_multiclass_roc_ovr(
    y_true: np.ndarray | pd.Series,
    proba: np.ndarray,
    *,
    class_names: list[str] | None = None,
    title: str = "ROC One-vs-Rest (multiclasse)"
) -> None:
    """
    Plotta curve ROC in modalità One-vs-Rest (una classe vs tutte le altre) per classificazione multiclasse.

    Parametri:
        y_true: Etichette vere (interi 0, 1, 2, ...).
        proba: Probabilità predette shape (n_samples, n_classes).
        class_names: Nomi delle classi per la legenda.
        title: Titolo del grafico.

    Note:
        La ROC mostra il compromesso tra TPR (recall) e FPR al variare del valore di soglia.
        L'AUC riassume l'area sotto la curva: più vicino a 1 è migliore.
        In multiclasse è informativa ma meno intuitiva della matrice di confusione.
        One-vs-Rest: per ogni classe, calcola ROC contro tutte le altre classi combinate.
    """
    # Numero di classi = numero di colonne della matrice delle probabilità
    n_classes = proba.shape[1]

    # Se l'utente non passa i nomi delle classi, creiamoli automaticamente
    if class_names is None:
        class_names = []
        for i in range(n_classes):
            class_names.append(f"Classe {i}")

    # Crea una nuova figura su cui disegnare le curve ROC
    plt.figure(figsize=(10, 8))

    # Prepara una palette di colori distinti, uno per ogni classe
    color_values = np.linspace(0, 1, n_classes)      # valori tra 0 e 1 per campionare la colormap
    colors = plt.cm.Set1(color_values)               # Set1 è una colormap con colori ben distinti

    # Scorre ogni classe e vi associa un colore -> (indice, nome_classe, colore)
    class_info = []
    for i in range(n_classes):
        class_info.append((i, class_names[i], colors[i]))

    # Ciclo per disegnare ROC e calcolare AUC per ogni classe
    for i, class_name, color in class_info:
        
        # 1. Binarizza le etichette: la classe 'i' diventa positiva (1), le altre negative (0)
        y_binary = (y_true == i).astype(int)

        # 2. Calcola FPR, TPR e soglie per la ROC di questa classe
        fpr, tpr, thresholds = roc_curve(y_binary, proba[:, i])

        # 3. Calcola AUC = area sotto la curva ROC
        roc_auc = auc(fpr, tpr)

        # 4. Disegna la curva ROC per questa classe
        plt.plot(
            fpr, tpr, 
            color=color,
            lw=2,
            label=f"{class_name} (AUC = {roc_auc:.3f})"
        )
    
    # Linea di riferimento (classificatore casuale)
    plt.plot([0, 1], [0, 1], 'k--', lw=2, alpha=0.5, label='Classificatore casuale (AUC = 0.5)')
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Tasso di Falsi Positivi (FPR)', fontsize=12)
    plt.ylabel('Tasso di Veri Positivi (TPR)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc="lower right", fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


# ------------------------------------------------------------
# Funzione orchestratrice
# ------------------------------------------------------------

def evaluate_classifier(
    model: Any,
    X_train: Any,
    y_train: np.ndarray | pd.Series,
    X_test: Any,
    y_test: np.ndarray | pd.Series,
    *,
    average: Literal["macro", "micro", "weighted"] = "macro",
    labels: list[str] | np.ndarray | None = None,
    digits: int = 3,
    show_confusion: bool = True,
    show_roc: bool = True
) -> dict[str, dict[str, Any]]:
    """
    Valuta un classificatore su train e test con metriche e visualizzazioni.

    Parametri:
        model: Modello addestrato con metodi predict() e (se disponibile) predict_proba().
        X_train, y_train: Dati di training.
        X_test, y_test: Dati di test.
        average: Tipo di media per le metriche ("macro", "micro", "weighted").
        labels: Nomi delle classi.
        digits: Cifre decimali per le metriche.
        show_confusion: Se True, mostra matrice di confusione sul test.
        show_roc: Se True, mostra curve ROC (richiede predict_proba nel modello classificatore).

    Ritorna:
        dict: {"train": {...metriche...}, "test": {...metriche...}}

    Note:
        - Per show_roc=True servono probabilità: se predict_proba non esiste, lo salta in silenzio
        - In multiclasse, average="macro" è spesso una buona scelta perché pesa ogni classe allo stesso modo
        - weighted considera la frequenza delle classi, micro calcola metriche globali
    """
    results = {}
    
    # Predizioni su train e test
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Calcola metriche per train
    results["train"] = compute_classification_metrics(
        y_train, y_train_pred,
        average=average, labels=labels, digits=digits
    )
    
    # Calcola metriche per test
    results["test"] = compute_classification_metrics(
        y_test, y_test_pred,
        average=average, labels=labels, digits=digits
    )
    
    # Matrice di confusione sul test
    if show_confusion:
        plot_confusion_matrix(
            y_test, y_test_pred,
            labels=labels,
            title="Matrice di Confusione (Test)"
        )
    
    # Curve ROC (solo se il modello supporta predict_proba)
    if show_roc:
        try:
            y_test_proba = model.predict_proba(X_test)
            plot_multiclass_roc_ovr(
                y_test, y_test_proba,
                class_names=labels,
                title="ROC One-vs-Rest (Test)"
            )
        except AttributeError:
            pass  # Modello senza predict_proba: salta silenziosamente
    
    return results
