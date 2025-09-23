from __future__ import annotations

"""
preprocessing.py
----------------

Preparazione dati per KNN: pulizia, split stratificato, scalatura.
KNN è sensibile alla scala → StandardScaler obbligatorio.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from typing import Any


# ------------------------------------------------------------
# Pulizia di base
# ------------------------------------------------------------

def clean_data(
    df: pd.DataFrame, 
    *,  # '*' indica che tutti i parametri dopo di lui devono essere passati per nome, non come posizionali
    drop_duplicates: bool = True,
    replace_inf_with_nan: bool = True
) -> pd.DataFrame:
    """
    Pulizia base: duplicati e ±inf → NaN.
    """
    df_clean = df.copy()
    
    if drop_duplicates:
        df_clean = df_clean.drop_duplicates()  # Rimuove duplicati (preserva primo)
    
    if replace_inf_with_nan:
        df_clean = df_clean.replace([np.inf, -np.inf], np.nan)  # ±inf → NaN per evitare errori
    
    return df_clean


# ------------------------------------------------------------
# Riepilogo target (generico)
# ------------------------------------------------------------

def summarize_target(df: pd.DataFrame, target_col: str) -> dict[str, Any]:
    """
    Calcola statistiche di riepilogo per la variabile target.

    Parametri:
        df: DataFrame contenente la colonna target.
        target_col: Nome della colonna target.

    Ritorna:
        dict: Dizionario con chiavi:
            - "counts": {classe: count, ...}
            - "perc": {classe: percentuale_float, ...}
            - "n_samples": numero totale di campioni
    """
    if target_col not in df.columns:
        raise ValueError(f"Colonna target '{target_col}' non trovata nel DataFrame")
    
    target_series = df[target_col]
    counts = target_series.value_counts().to_dict() # Dizionario contenente come chiave i nomi e come valori il numero di volte che compare quel nome
    n_samples = len(target_series)
    
    # Calcola percentuali
    for key, value in counts.items():
        perc = {key: (value / n_samples) * 100} # Dizionario contenente come chiave i nomi e come valori la percentuale di ciascun nome sul totale
    
    return {
        "counts": counts,
        "perc": perc,
        "n_samples": n_samples
    }


# ------------------------------------------------------------
# Gestione colonne e target
# ------------------------------------------------------------

def drop_id_columns(df: pd.DataFrame, id_cols: list[str] | None) -> pd.DataFrame:
    """
    Rimuove eventuali colonne ID se presenti.

    Parametri:
        df: DataFrame di input.
        id_cols: Lista di nomi colonne da rimuovere (ignora quelle assenti).

    Ritorna:
        pd.DataFrame: DataFrame senza le colonne ID specificate.

    Note:
        Le colonne non presenti nel DataFrame vengono ignorate.
    """
    # Se non viene passata alcuna lista
    if id_cols is None:
        return df.copy()
    
    # Se viene passata una lista, crea la lista da eliminare
    cols_to_drop = []
    for col in id_cols:
        if col in df.columns:
                cols_to_drop.append(col)
    
    # Se la lista è vuota, non c'è nulla da togliere
    if not cols_to_drop:    # in Python le liste vuote sono valutate come False
        return df.copy()
    
    return df.drop(columns=cols_to_drop)


def encode_target_if_needed(y: pd.Series) -> tuple[pd.Series, dict[str, int] | None]:
    """
    Se necessario, codifica la variabile target usando **LabelEncoder**.

    Parametri:
        y: Serie con i valori target. 
        esempio: y = pd.Series(['Kiwi', 'Mela', 'Banana', 'Pesca'], name='Frutta')

    Ritorna:
        tuple: (y_encoded, mapping_dict) dove:
            - y_encoded: Serie con target codificato numericamente
            - mapping_dict: {label_originale: intero} se codifica applicata, None altrimenti

    Note:
        Se y è già numerico (int, float), viene restituito inalterato.
        Se y è object/string/category, viene applicato LabelEncoder.
    """
    # Verifica se la serie y è già numerica
    if pd.api.types.is_numeric_dtype(y):
        return y, None  # Ritorna la Series originale e nessun mapping
    
    # Altrimenti usa LabelEncoder per trasformare le variabili categoriali in numeri
    le = LabelEncoder()
    y_array = le.fit_transform(y)   # .fit(y) impara le classi presenti e le memorizza (in ordine alfabetico) in le.classes_
                                    # .transform(y) sostituisce ogni classe con un numero intero, seguendo l'ordine di le.classes_
                                    # Quindi, si ottiene y_array come un array Numpy di numeri interi
    
    # Converte l’array NumPy in una Series Pandas, preservando indice e nome originali
    y_encoded = pd.Series(y_array, index=y.index, name=y.name)
    
    # Costruisce il dizionario mapping {etichetta_originale: numero}
    mapping = {}
    for idx, label in enumerate(le.classes_): # Scorre le.classes_ e assegna a ciascuna classe l'indice
        mapping[label] = idx
    
    return y_encoded, mapping


# ------------------------------------------------------------
# Split train/test stratificato
# ------------------------------------------------------------

def train_test_split_df(
    df: pd.DataFrame,
    *,  # tutti i parametri dopo '*' devono essere passati per nome, non come posizionali
    target_col: str,    
    test_size: float = 0.2,  # Percentuale di dati nel test set (20%)
    random_state: int = 42,  # Fissa la casualità per rendere lo split ripetibile
    stratify: bool = True,
    id_cols: list[str] | None = None
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, dict[str, int] | None]:
    """
    Esegue uno split train/test, con eventuale stratificazione e encoding automatico del target.
    Ritorna anche il mapping classi->interi se il target era categoriale.
    """
    if target_col not in df.columns:
        raise ValueError(f"Colonna target '{target_col}' non trovata")
    
    # Rimuove eventuali colonne ID dalle feature
    X = drop_id_columns(df, id_cols)
    # Rimuove la colonna target dalle feature
    if target_col in X.columns:
        X = X.drop(columns=[target_col])
    
    # Target + encoding automatico (LabelEncoder solo se categoriale)
    y = df[target_col]
    y_encoded, target_mapping = encode_target_if_needed(y)
    
    # Stratificazione solo se il target è categoriale
    use_stratify = stratify and (target_mapping is not None)
    # Alternativa esplicita:
    # use_stratify = False
    # if stratify and (target_mapping is not None):
    #     use_stratify = True
    
    # train_test_split divide il dataset in train e test.
    # Se stratify=y_encoded:
    #   - Per ogni classe c in y_encoded, calcola:
    #         n_test_c = round(test_size * n_tot_c)
    #     e assegna n_test_c campioni di classe c al test, i restanti al train.
    #   - In questo modo le proporzioni delle classi si mantengono in entrambi i set.
    # Senza stratify, la divisione è casuale e le proporzioni possono variare.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=test_size,
        random_state=random_state,
        stratify=y_encoded if use_stratify else None
    )
    
    return X_train, X_test, y_train, y_test, target_mapping

# ------------------------------------------------------------
# Costruzione preprocessore per KNN 
# ------------------------------------------------------------

def build_preprocessor(
    X: pd.DataFrame,
    *,
    scale_numeric: bool = True, 
    numeric_cols: list[str] | None = None
) -> ColumnTransformer:
    """
    La funzione build_preprocessor serve per creare un preprocessore che:
    • prende un dataset X
    • individua le colonne numeriche
    • le standardizza (media=0, std=1) se scale_numeric=True
    • lascia inalterate tutte le altre colonne.
    """

    # Se l’utente non passa le colonne numeriche, le trova autonomamente
    if numeric_cols is None:
        numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

    # Se non ci sono colonne numeriche → restituisce tutto invariato
    if not numeric_cols:
        return ColumnTransformer(transformers=[], remainder='passthrough')

    # Nome della trasformazione
    nome_trasf = 'scal'

    # L'oggetto che farà la standardizzazione
    scaler = StandardScaler()

    # Colonne su cui applicare la trasformazione
    colonne = numeric_cols

    # Creo la lista dei transformers e aggiungo il blocco
    transformers = []
    transformers.append((nome_trasf, scaler, colonne))

    # Restituisce il ColumnTransformer finale
    return ColumnTransformer(
        transformers=transformers,
        remainder='passthrough'
    )


# ------------------------------------------------------------
# Utility riepilogo dataset
# ------------------------------------------------------------

def describe_dataset(df: pd.DataFrame, 
                    target_col: str | None = None  # target_col è opzionale: se presente, deve essere una stringa; se non lo passi, è None
                    ) -> dict[str, Any]:
    """
    Genera un riepilogo completo del dataset.

    Parametri:
        df: DataFrame da analizzare.
        target_col: Nome della colonna target (opzionale).

    Ritorna:
        dict: Dizionario con chiavi:
            - "n_rows": numero di righe
            - "n_cols": numero di colonne
            - "numeric_cols": lista colonne numeriche
            - "categorical_cols": lista colonne categoriali
            - "nan_per_column": {col: count_nan}
            - "target_summary": output di summarize_target() se target_col fornito

    Note:
        Nessuna stampa: tutto ritornato come dizionario.
    """
    # Dimensioni base
    n_rows, n_cols = df.shape
    
    # Estrae i nomi delle colonne numeriche e le inserisce in una lista
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Estrae i nomi delle colonne categoriche e le inserisce in una lista
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Conteggio NaN per colonna
    nan_per_column = df.isnull().sum().to_dict()
    
    # Riepilogo target se specificato
    target_summary = None
    if target_col is not None and target_col in df.columns:
        target_summary = summarize_target(df, target_col)
    
    return {
        "n_rows": n_rows,
        "n_cols": n_cols,
        "numeric_cols": numeric_cols,
        "categorical_cols": categorical_cols,
        "nan_per_column": nan_per_column,
        "target_summary": target_summary
    }
