from __future__ import annotations

"""
model.py
--------

Pipeline KNN e tuning. Preprocessore fornito dall'esterno.
"""

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from typing import Any
import time


# ------------------------------------------------------------
# Costruzione Pipeline KNN
# ------------------------------------------------------------

def build_knn_pipeline(
    preprocessor,                   # Qui mettiamo un oggetto che prepara i dati (es. StandardScaler)
    *,
    n_neighbors: int = 7,           # Quanti "vicini" usare per il KNN
    weights: str = "distance",      # Se "distance", i punti più vicini pesano di più; se "uniform", pesano tutti uguale
    metric: str = "minkowski",      # Tipo di distanza: "minkowski" con p=2 = distanza Euclidea
    p: int = 2                      # Parametro p: p=2 → Euclidea, p=1 → Manhattan
) -> Pipeline:

    """
    Costruisce una *Pipeline* composta da due fasi:

    1. **Preprocessing (prep)**: definisce come trasformare i dati prima dell'allenamento
       Esempio: StandardScaler → rende ogni colonna con media=0 e std=1

    2. **Modello KNN (knn)**: definisce il classificatore K-Nearest Neighbors
       (non viene ancora addestrato qui: l'allenamento parte quando chiami pipeline.fit)

    Dopo la creazione:
        pipeline.fit(X, y)
            → Esegue il preprocessing su X (solo train)
            → Allena KNN su X trasformato + y

        pipeline.predict(X_test)
            → Applica lo stesso preprocessing a X_test
            → Usa il KNN allenato per predire
    """

    # ----- Step A: Creiamo il modello KNN -----
    # Qui stiamo SOLO creando l'oggetto KNN con i parametri scelti.
    knn = KNeighborsClassifier(
        n_neighbors=n_neighbors,
        weights=weights,
        metric=metric,
        p=p
    )

    # ----- Step B: Costruiamo la Pipeline -----
    # La Pipeline esegue i passi in sequenza:
    #   1. "prep" = preprocessing (es. StandardScaler)
    #   2. "knn"  = modello KNN
    pipeline = Pipeline([
        ("prep", preprocessor),
        ("knn", knn)
    ])

    # La funzione restituisce l'oggetto Pipeline,
    # che ora possiamo addestrare e usare per predire.
    return pipeline


# ------------------------------------------------------------
# Addestramento modello
# ------------------------------------------------------------

def fit_model(pipeline: Pipeline, X_train, y_train) -> Pipeline:
    """
    Esegue l'addestramento della Pipeline sul training set.

    Parametri:
        pipeline: Pipeline KNN da addestrare.
        X_train: Feature di training (DataFrame o array).
        y_train: Target di training (Serie o array).

    Ritorna:
        Pipeline: Pipeline addestrata (modificata in-place).

    Note:
        Equivale al metodo pipeline.fit(X_train, y_train).
        Viene riscritta come fit_model affinchè, in un futuro, si possano aggiungere
        ulteriori funzionalità al metodo senza intaccare il metodo .fit
    """
    start = time.perf_counter()  # ⏱ Inizio cronometro
    pipeline.fit(X_train, y_train)  # Allenamento vero e proprio
    end = time.perf_counter() # ⏱ Fine cronometro

    duration = end - start
    print(f"⏱ Addestramento completato in {duration:.3f} secondi")

    return pipeline

# ------------------------------------------------------------
# Griglia di iperparametri di default
# ------------------------------------------------------------

def default_param_grid() -> dict[str, list[Any]]:
    """
    Restituisce una griglia di iperparametri (param_grid) da usare con GridSearchCV
    per il modello KNN contenuto nella Pipeline.

    Cosa può fare il codice con questa griglia:
    - NON viene usata direttamente dall'utente per allenare il modello.
    - Viene letta da GridSearchCV, che proverà **tutte le combinazioni** dei valori qui elencati.
    - Per ogni combinazione:
        1. Allena la Pipeline (prep + KNN) su un sottoinsieme di dati (train fold)
        2. Valida su un altro sottoinsieme (val fold)
        3. Calcola una metrica standard di valutazione del modello 
    - Alla fine, GridSearchCV sceglie la combinazione di parametri con il punteggio migliore
      e ri-addestra la Pipeline migliore su tutto il training set.

    Chiavi del dizionario:
        - "knn__n_neighbors": numero di vicini K da considerare
        - "knn__weights": come pesare i vicini ("uniform" = tutti uguali, "distance" = vicini più vicini pesano di più)
        - "knn__metric": tipo di distanza ("euclidean", "manhattan", "minkowski")
        - "knn__p": parametro p per Minkowski (p=1 → Manhattan, p=2 → Euclidean)

    Nota:
        Il prefisso "knn__" indica che i parametri appartengono allo step "knn" della Pipeline
        (Pipeline usa la sintassi nome_step__parametro per accedere ai parametri interni).

    Ritorna:
        dict: dizionario con le liste di valori da testare per ogni iperparametro
    """
    return {
        "knn__n_neighbors": [3, 5, 7, 9, 11],
        "knn__weights": ["uniform", "distance"],
        "knn__metric": ["euclidean", "manhattan", "minkowski"],
        "knn__p": [1, 2]  # p=1=manhattan, p=2=euclidean (solo per metric="minkowski")
    }


# ------------------------------------------------------------
# Tuning degli iperparametri
# ------------------------------------------------------------

def tune_model(
    pipeline: Pipeline,
    X_train,
    y_train,
    *,
    param_grid: dict[str, list[Any]] | None = None, 
    cv: int = 5,                        # numero di fold (per classificazione: di norma StratifiedKFold con N fold)
    scoring: str = "f1_macro",          # metrica da ottimizzare (media F1 tra classi, non pesata)
    n_jobs: int = -1,                   # n. processi in parallelo (-1 = usa tutti i core disponibili)
    verbose: int = 0,                   # livello di log di GridSearchCV (0 silenzioso, 1/2 più verboso)
    refit: bool = True                  # se True, ri-addestra la migliore combinazione su TUTTO il training set
) -> tuple[Pipeline, dict[str, Any]]:
    """
    Esegue una ricerca a griglia (GridSearchCV) degli iperparametri della Pipeline.

    Come funziona:
      1) Se la griglia non è fornita, usa default_param_grid() (chiavi tipo "knn__param" per
         riferirsi allo step "knn" della Pipeline).
      2) Per ogni combinazione nella griglia:
           - divide il training in `cv` fold (con classificazione di norma stratificata),
           - allena su (cv-1) fold e valida sull'altro fold,
           - ripete facendo ruotare il fold di validazione,
           - calcola la media della metrica (es. f1_macro) della combinazione testata.
      3) Sceglie la combinazione con la media migliore; se `refit=True`, la ri-addestra
         sull'intero training set.
    
    Note:
      - Se nella griglia `knn__metric` vale "euclidean" o "manhattan", `knn__p` è ignorato
        (il parametro `p` ha effetto solo con `metric="minkowski"`).
      - `cv_results_` contiene i risultati completi (es. 'mean_test_score', 'std_test_score', ecc.).

    Ritorna:
      - pipeline migliore già fittata (best_estimator_)
      - dizionario con TUTTE le metriche della ricerca (cv_results_)
    """
    if param_grid is None:
        param_grid = default_param_grid()

    grid_search = GridSearchCV(
        estimator=pipeline,     
        param_grid=param_grid,  
        cv=cv,                  
        scoring=scoring,        # metrica da massimizzare
        n_jobs=n_jobs,        
        verbose=verbose,
        refit=refit             
    )

    # Per ogni combinazione della griglia, GridSearchCV esegue cv addestramenti/valutazioni
    # (cv-1 fold per il training, 1 fold per la validation), ruotando i fold.
    grid_search.fit(X_train, y_train)

    # best_estimator_ = Pipeline migliore già addestrata (se refit=True)
    # cv_results_ = risultati completi (dict di array) per analisi/sintesi dei punteggi
    return grid_search.best_estimator_, grid_search.cv_results_


# ------------------------------------------------------------
# Utility per introspezione
# ------------------------------------------------------------

def get_knn_step(pipeline: Pipeline, 
                verbose: bool = False) -> KNeighborsClassifier:
    """
    Restituisce lo step KNN dalla Pipeline.
    Se verbose=True, stampa anche i parametri principali del modello.

    Parametri:
        pipeline: Pipeline con step "knn".
        verbose: Se True, stampa i parametri principali del KNN.

    Ritorna:
        KNeighborsClassifier: Istanza del classificatore KNN.
    """
    knn_model = pipeline.named_steps["knn"]

    if verbose:
        print("📌 Parametri principali del KNN:")
        print(f"  - n_neighbors: {knn_model.n_neighbors}")
        print(f"  - weights: {knn_model.weights}")
        print(f"  - metric: {knn_model.metric}")

    return knn_model