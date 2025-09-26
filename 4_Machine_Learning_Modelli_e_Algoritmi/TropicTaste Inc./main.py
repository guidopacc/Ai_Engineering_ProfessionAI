from __future__ import annotations

"""
main.py
-------

Punto di ingresso per classificazione KNN frutti.
Carica dati → allena KNN → valuta → salva (opzionale).
"""

from typing import Any, Dict
import pandas as pd
import numpy as np

# Import dei moduli del progetto
import data_io
import train
import eda


# ==================================================================================
# PARAMETRI DI CONFIGURAZIONE (VARIABILI DA MODIFICARE PER TWEAKING DEL MODELLO)
# ==================================================================================

# Dataset
DATA_PATH: str = "https://proai-datasets.s3.eu-west-3.amazonaws.com/fruits.csv"
TARGET_COL: str = "Frutto"  # Nome della colonna target nel dataset

# Training/Tuning - VARIABILI PRINCIPALI PER TWEAKING
DO_TUNE: bool = True  # True=GridSearchCV, False=addestramento semplice
TEST_SIZE: float = 0.2  # Frazione per test (0.1-0.3)
RANDOM_STATE: int = 42  # Numero che fissa la sequenza casuale, così eseguendo il codice più volte si ottengono sempre gli stessi risultati.
SCORING: str = "f1_macro"  # Metrica da ottimizzare: "f1_macro" di default, altrimenti "accuracy", "precision_macro"
CV_FOLDS: int = 5  # Fold per CV (3-10, più alto=più lento ma più robusto)

# Valutazione
AVERAGE: str = "macro"  # Media metriche: "macro" (bilanciato), "micro" (globale), "weighted" (per frequenza)
SHOW_CONFUSION: bool = True  # Mostra matrice confusione
SHOW_ROC: bool = True  # Mostra curve ROC (solo se modello supporta predict_proba)

# Salvataggio
SAVE_ARTIFACTS: bool = True  # Salva modello e metriche
MODEL_PATH: str = "artifacts/knn_model.pkl"  # Percorso modello
METRICS_PATH: str = "artifacts/metrics.json"  # Percorso metriche


# ============================================================
# FUNZIONE PRINCIPALE
# ============================================================

def run() -> Dict[str, Any]:
    """
    Esegue il flusso completo di classificazione KNN: carica dati, allena modello,
    valuta performance e salva risultati opzionalmente.

    Ritorna:
        dict: Risultati completi dell'esperimento con chiavi:
            - "model": Pipeline addestrata
            - "results": Metriche su train/test
            - "cv_results": Risultati GridSearchCV (se tuning)
            - "splits": Dati di split per debug

    Note:
        Stampa metriche chiave (F1 macro, accuracy) e migliori iperparametri.
        Salva modello e metriche se SAVE_ARTIFACTS=True.
    """
    print("=" * 60)
    print("PROGETTO CLASSIFICAZIONE KNN - FRUTTI ESOTICI")
    print("=" * 60)
    
    # 1. Caricamento dataset
    print(f"\n Caricamento dataset da: {DATA_PATH}")
    try:
        df = data_io.load_dataset(DATA_PATH)  # Supporta URL GitHub → raw automatico
        print(f" Dataset caricato: {df.shape[0]} righe, {df.shape[1]} colonne")
        print(f"   Colonne: {list(df.columns)}")
    except Exception as e: 
        print(f" Errore nel caricamento dataset: {e}")
        raise
    
    # 2. Analisi esplorativa (EDA)
    print(f"\n Analisi esplorativa dei dati...")
    try:
        # Auto-rileva colonne numeriche (esclude target)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if TARGET_COL in numeric_cols:
            numeric_cols.remove(TARGET_COL)
        
        eda.run_eda_analysis(df, TARGET_COL, numeric_cols)
    except Exception as e:
        print(f" Errore durante EDA: {e}")
        print(" Continuo con l'addestramento...")
    
    # 3. Addestramento e valutazione
    print(f"\n Addestramento modello KNN...")
    print(f"   Target: {TARGET_COL}")
    print(f"   Tuning: {'Sì' if DO_TUNE else 'No'}")
    print(f"   Test size: {TEST_SIZE}")
    print(f"   Scoring: {SCORING}")
    
    try:
        # Estrai nomi delle classi per la matrice di confusione
        class_names = sorted(df[TARGET_COL].unique().tolist())
        
        results = train.train_and_evaluate(
            df,
            target_col=TARGET_COL,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=True,  # Stratificazione per classificazione
            id_cols=None,  # Nessuna colonna ID da rimuovere
            scale_numeric=True,  # StandardScaler per KNN
            numeric_cols=None,  # Auto-rileva colonne numeriche
            do_tune=DO_TUNE,
            param_grid=None,  # Usa griglia di default
            cv=CV_FOLDS,
            scoring=SCORING,
            n_jobs=-1,  # Usa tutti i core disponibili
            verbose=0,  # Silenzioso
            average=AVERAGE,
            labels=class_names,  # Nomi delle classi per matrice di confusione
            digits=3,
            show_confusion=SHOW_CONFUSION,
            show_roc=SHOW_ROC
        )
        print(" Addestramento completato")
    except Exception as e:
        print(f" Errore durante l'addestramento: {e}")
        raise
    
    # 4. Stampa metriche chiave
    print(f"\n RISULTATI PRINCIPALI")
    print("-" * 40)


    # Metriche su test (valutazione del modello)
    print(f"\n Metriche su test (valutazione del modello):")
    print("-" * 40)
    test_metrics = results["results"]["test"]
    print(f" F1 Macro (Test): {test_metrics['f1']:.3f}")
    print(f" Accuracy (Test): {test_metrics['accuracy']:.3f}")
    print(f" Precision (Test): {test_metrics['precision']:.3f}")
    print(f" Recall (Test): {test_metrics['recall']:.3f}")
    print("-" * 40)
    

    # Metriche su train (controllo overfitting)
    train_metrics = results["results"]["train"]
    print(f"\n Metriche su train (controllo overfitting):")
    print("-" * 40)
    print(f"\n F1 Macro (Train): {train_metrics['f1']:.3f}")
    print(f" Accuracy (Train): {train_metrics['accuracy']:.3f}")
    print("-" * 40)
    
    
    # Differenza train-test (controllo overfitting)
    f1_diff = train_metrics['f1'] - test_metrics['f1']
    acc_diff = train_metrics['accuracy'] - test_metrics['accuracy']

    print("\nControllo Overfitting")
    print("-" * 40)

    # Funzione di supporto per messaggi
    def check_overfit(metric_name: str, diff: float, soglia: float = 0.1) -> None:
        """
        Controlla se la differenza train-test supera la soglia
        e stampa un messaggio chiaro per l'utente.

        Parametri:
            metric_name: Nome della metrica (F1 o Accuracy)
            diff: Differenza tra train e test
            soglia: Soglia per considerare overfit (default: 0.1)
        """
        if abs(diff) < soglia:
            print(f" {metric_name}: {diff:+.3f} → Nessun overfit rilevante)")
        else:
            print(f" {metric_name}: {diff:+.3f} → ATTENZIONE: possibile overfit!")
            print(f"   La differenza tra train e test è {abs(diff):.3f}, sopra la soglia di {soglia}.")
            print(f"   Questo può indicare che il modello ha imparato troppo bene i dati di training,")
            print(f"   ma generalizza peggio sui dati nuovi (test).")

    # Controllo per entrambe le metriche
    check_overfit("F1", f1_diff)
    check_overfit("Accuracy", acc_diff)
    print("-" * 40)
    
    # 5. Stampa migliori iperparametri (se tuning)
    if DO_TUNE and results["cv_results"] is not None:
        print(f"\n MIGLIORI IPERPARAMETRI (Tuning)")
        print("-" * 40)
        
        # Estrae i migliori parametri dal GridSearchCV
        cv_results = results["cv_results"]          # Tutti i risultati
        params_list = cv_results["params"]          # Lista di parametri provati
        rank_list = cv_results["rank_test_score"]   # Classifica dei parametri

        # Trova l'indice del migliore (dove rank = 1)
        best_index = int(np.where(rank_list == 1)[0][0])

        # Parametri migliori
        best_params = params_list[best_index]
        for param, value in best_params.items():
            # Rimuove il prefisso "knn__" per leggibilità
            clean_param = param.replace("knn__", "")
            # Formatta diversamente per numeri e stringhe
            if isinstance(value, (int, float)):
                print(f"   {clean_param}: {value}")
            else:
                print(f"   {clean_param}: {value}")
        
        # Score del miglior modello (già calcolato sopra)
        best_score = results["cv_results"]["mean_test_score"][best_index]
        print(f"   CV Score: {best_score:.3f}")
        print("-" * 40)
    
    # 6. Salvataggio opzionale
    if SAVE_ARTIFACTS:
        print(f"\n Salvataggio risultati...")
        try:
            # Salva modello
            data_io.save_model(results["model"], MODEL_PATH)  # Pipeline completa con scaler
            print(f" Modello salvato: {MODEL_PATH}")
            
            # Salva metriche
            data_io.save_metrics(results["results"], METRICS_PATH)  # JSON con train/test metrics
            print(f" Metriche salvate: {METRICS_PATH}")
            
        except Exception as e:
            print(f"  Errore nel salvataggio: {e}")
    else:
        print(f"\n Salvataggio disabilitato (SAVE_ARTIFACTS=False)")
    
    # 7. Riepilogo finale
    print(f"\n" + "=" * 60)
    print(" PROCEDIMENTO COMPLETATO")
    print("=" * 60)
    
    if DO_TUNE:
        print(f" Miglior F1 Macro: {test_metrics['f1']:.3f}")
        print(f" Miglior Accuracy: {test_metrics['accuracy']:.3f}")
    else:
        print(f" F1 Macro: {test_metrics['f1']:.3f}")
        print(f" Accuracy: {test_metrics['accuracy']:.3f}")
    
    print(f" Dati: {df.shape[0]} campioni, {df.shape[1]} feature")
    print(f" Configurazione: {'Tuning' if DO_TUNE else 'Addestramento semplice'}")
    
    return results


# ============================================================
# ESECUZIONE PRINCIPALE
# ============================================================

if __name__ == "__main__": 
    """
    Punto di ingresso per l'esecuzione come script.
    Eseguito solo se lanci direttamente questo file, non se importato da altro modulo.

    In locale, eseguire con:
        python main.py
    
    In Google Colab, eseguire con:
        !python main.py
    
    Assicurarsi che tutti i moduli del progetto siano nella stessa cartella:
        - data_io.py
        - eda.py
        - preprocessing.py
        - model.py
        - metrics.py
        - train.py
        - main.py
    """
    try:
        results = run()
        print(f"\n Script completato con successo!")
        
    except KeyboardInterrupt:
        print(f"\n  Esecuzione interrotta dall'utente")
        
    except Exception as e:
        print(f"\n Errore critico: {e}")
        print(f"   Tipo: {type(e).__name__}")
        raise
