from __future__ import annotations

"""
train.py
--------

Orchestratore end-to-end: preprocessing → fit/tune → evaluate.
KNN sensibile alla scala → StandardScaler nella Pipeline.
"""

from typing import Any, Dict, Optional, Tuple, Literal
import pandas as pd

# Import dei moduli interni del progetto
import preprocessing
import model
import metrics


# ------------------------------------------------------------
# Preparazione dati
# ------------------------------------------------------------

def prepare_data(
    df: pd.DataFrame,
    *,
    target_col: str,
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True,
    id_cols: list[str] | None = None,
    scale_numeric: bool = True,
    numeric_cols: list[str] | None = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, Any]:
    """
    Esegue la preparazione completa dei dati prima dell'addestramento.

    Parametri:
        df: DataFrame completo con feature e target.
        target_col: Nome della colonna target.
        test_size: Frazione del dataset per il test (0 < test_size < 1).
        random_state: Numero che fissa la sequenza casuale, così eseguendo il codice più volte si ottengono sempre gli stessi risultati.
        stratify: Se True, mantiene proporzioni delle classi in train/test (vedi modulo 'preprocessing.py')
        id_cols: Colonne ID da rimuovere dalle feature.
        scale_numeric: Se True, applica StandardScaler alle colonne numeriche.
        numeric_cols: Lista esplicita di colonne numeriche (se None, auto-rileva).

    Ritorna:
        Tuple: (X_train, X_test, y_train, y_test, preprocessor) dove:
            - X_train, X_test: DataFrame con feature (senza id_cols)
            - y_train, y_test: Serie con target (eventualmente codificato)
            - preprocessor: ColumnTransformer configurato per KNN

    Note:
        Esegue pulizia base (duplicati, ±inf→NaN), split stratificato e costruzione
        del preprocessore con StandardScaler per le feature numeriche.
        Nessuna stampa, nessun I/O.
    """
    # Pulizia base del dataset
    df_clean = preprocessing.clean_data(df)
    
    # Split stratificato con encoding automatico del target
    X_train, X_test, y_train, y_test, _ = preprocessing.train_test_split_df(
        df_clean, 
        target_col=target_col, 
        test_size=test_size, 
        random_state=random_state, 
        stratify=stratify, 
        id_cols=id_cols
    )
    
    # Costruzione preprocessore (StandardScaler per KNN)
    preprocessor = preprocessing.build_preprocessor(
        X_train, 
        scale_numeric=scale_numeric, 
        numeric_cols=numeric_cols
    )
    
    return X_train, X_test, y_train, y_test, preprocessor


# ------------------------------------------------------------
# Addestramento semplice
# ------------------------------------------------------------

def train_pipeline(
    X_train: Any,
    y_train: Any,
    *,
    preprocessor: Any,
    n_neighbors: int = 7,
    weights: Literal["uniform", "distance"] = "distance",
    metric: Literal["euclidean", "manhattan", "minkowski"] = "minkowski",
    p: int = 2
) -> Any:
    """
    Costruisce e addestra una Pipeline KNN con iperparametri fissi.

    Parametri:
        X_train, y_train: Dati di training.
        preprocessor: Preprocessore (ColumnTransformer) da integrare nella Pipeline.
        n_neighbors: Numero di vicini per KNN (>= 1).
        weights: Schema di pesatura ("uniform" | "distance").
        metric: Metrica di distanza ("euclidean" | "manhattan" | "minkowski").
        p: Parametro Minkowski (>= 1, rilevante solo se metric="minkowski").

    Ritorna:
        Pipeline: Pipeline KNN addestrata con iperparametri specificati.

    Note:
        Costruisce la Pipeline con model.build_knn_pipeline e la addestra con model.fit_model.
        Nessun I/O, nessuna stampa.
    """
    # Costruzione Pipeline KNN
    pipe = model.build_knn_pipeline(
        preprocessor,
        n_neighbors=n_neighbors,
        weights=weights,
        metric=metric,
        p=p
    )
    
    # Addestramento
    pipe = model.fit_model(pipe, X_train, y_train)
    
    return pipe


# ------------------------------------------------------------
# Tuning degli iperparametri
# ------------------------------------------------------------

def tune_pipeline(
    X_train: Any,
    y_train: Any,
    *,
    preprocessor: Any,
    param_grid: dict | None = None,
    cv: int = 5,
    scoring: str = "f1_macro",
    n_jobs: int = -1,
    verbose: int = 0
) -> Tuple[Any, dict]:
    """
    Esegue tuning degli iperparametri tramite GridSearchCV.

    Parametri:
        X_train, y_train: Dati di training.
        preprocessor: Preprocessore da integrare nella Pipeline.
        param_grid: Griglia di iperparametri (usa default se None).
        cv: Numero di fold per cross-validation (>= 2).
        scoring: Metrica da ottimizzare (default: "f1_macro").
        n_jobs: Numero di job paralleli (-1 = tutti i core).
        verbose: Livello di verbosità (0 = silenzioso).

    Ritorna:
        Tuple: (best_estimator, cv_results) dove:
            - best_estimator: Pipeline addestrata con i migliori iperparametri
            - cv_results: Dizionario con risultati dettagliati della grid search

    Note:
        Se param_grid è None, usa model.default_param_grid() per una griglia sensata.
        La Pipeline base usa iperparametri di default, poi GridSearchCV li ottimizza.
        Nessun I/O, nessuna stampa.
    """
    # Costruzione Pipeline base (iperparametri di default)
    pipe = model.build_knn_pipeline(
        preprocessor,
        n_neighbors=7,
        weights="distance",
        metric="minkowski",
        p=2
    )
    
    # Griglia di iperparametri (usa default se non specificata)
    grid = param_grid or model.default_param_grid() # Se param_grid è “truthy” → grid = param_grid, altrimenti → grid = model.default_param_grid()
    
    # Tuning tramite GridSearchCV
    best_pipe, cv_results = model.tune_model(
        pipe, X_train, y_train,
        param_grid=grid,
        cv=cv,
        scoring=scoring,
        n_jobs=n_jobs,
        verbose=verbose
    )
    
    return best_pipe, cv_results


# ------------------------------------------------------------
# Orchestratore end-to-end
# ------------------------------------------------------------

def train_and_evaluate(
    df: pd.DataFrame,
    *,
    # Parametri dati / split
    target_col: str,
    test_size: float = 0.2,
    random_state: int = 42,
    stratify: bool = True,
    id_cols: list[str] | None = None,
    # Parametri preprocess
    scale_numeric: bool = True,
    numeric_cols: list[str] | None = None,
    # Parametri training/tuning
    do_tune: bool = True,
    param_grid: dict | None = None,
    cv: int = 5,
    scoring: str = "f1_macro",
    n_jobs: int = -1,
    verbose: int = 0,
    # Parametri valutazione
    average: Literal["macro", "micro", "weighted"] = "macro",
    labels: list[str] | None = None,
    digits: int = 3,
    show_confusion: bool = True,
    show_roc: bool = True
) -> dict[str, Any]:
    """
    Orchestratore end-to-end per addestramento e valutazione di classificatori KNN.

    Parametri:
        df: DataFrame completo con feature e target.
        target_col: Nome della colonna target.
        test_size: Frazione per il test (0 < test_size < 1).
        random_state: Semina per riproducibilità.
        stratify: Se True, stratifica per il target durante lo split.
        id_cols: Colonne ID da rimuovere dalle feature.
        scale_numeric: Se True, applica StandardScaler alle colonne numeriche.
        numeric_cols: Lista esplicita di colonne numeriche (se None, auto-rileva).
        do_tune: Se True, esegue tuning; altrimenti addestramento con iperparametri fissi.
        param_grid: Griglia per tuning (usa default se None).
        cv: Numero di fold per cross-validation (>= 2).
        scoring: Metrica da ottimizzare per tuning.
        n_jobs: Numero di job paralleli per tuning.
        verbose: Livello di verbosità per tuning.
        average: Tipo di media per le metriche di valutazione.
        labels: Nomi delle classi per report e visualizzazioni.
        digits: Cifre decimali per le metriche.
        show_confusion: Se True, mostra matrice di confusione.
        show_roc: Se True, mostra curve ROC (richiede predict_proba).

    Ritorna:
        dict: Dizionario con chiavi:
            - "model": Pipeline addestrata (con o senza tuning)
            - "results": {"train": {...metriche...}, "test": {...metriche...}}
            - "cv_results": Risultati GridSearchCV (None se do_tune=False)
            - "splits": {"X_train": ..., "X_test": ..., "y_train": ..., "y_test": ...}

    Note:
        Esegue il flusso completo: prepare_data → train/tune → evaluate.
        I plot sono mostrati da metrics solo se richiesti (show_confusion/show_roc).
        Nessuna stampa di testo, nessun I/O.
    """
    # 1. Preparazione dati: pulizia → split → preprocessore
    X_train, X_test, y_train, y_test, preprocessor = prepare_data(
        df,
        target_col=target_col,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
        id_cols=id_cols,
        scale_numeric=scale_numeric,
        numeric_cols=numeric_cols
    )
    
    # 2. Addestramento o tuning
    if do_tune:
        # Tuning con GridSearchCV (output: best_model e cv_results)
        best_model, cv_results = tune_pipeline(
            X_train, y_train,
            preprocessor=preprocessor,
            param_grid=param_grid,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs,
            verbose=verbose
        )
    else:
        # Addestramento semplice con iperparametri fissi (output: solo best_model, unico modello addestrato)
        best_model = train_pipeline(
            X_train, y_train,
            preprocessor=preprocessor
        )
        cv_results = None
    
    # 3. Valutazione con metriche e visualizzazioni
    results = metrics.evaluate_classifier(
        best_model, X_train, y_train, X_test, y_test,
        average=average,
        labels=labels,
        digits=digits,
        show_confusion=show_confusion,
        show_roc=show_roc
    )
    
    # 4. Ritorna dict completo per debug e riuso
    return {
        "model": best_model,
        "results": results,
        "cv_results": cv_results,
        "splits": {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test
        }
    }

