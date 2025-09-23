from __future__ import annotations

"""
data_io.py
-----------

I/O per dataset, modelli e metriche. 
Supporta URL GitHub → raw per Colab.
"""

from pathlib import Path
from typing import Any, Mapping, TYPE_CHECKING
from urllib.parse import urlparse
from datetime import datetime
import json

import pandas as pd
import numpy as np
from joblib import dump as joblib_dump, load as joblib_load

if TYPE_CHECKING:
    from matplotlib.figure import Figure


# ------------------------------------------------------------
# Utility percorso/cartelle
# ------------------------------------------------------------

def ensure_dir(path: str) -> None:
    """
    Garantisce l'esistenza della directory padre del percorso fornito.
    In pratica, se il percorso non esiste, la funzione crea la directory padre.
    Se la directory esiste già, non fa nulla.
    Evita errori come "No such file or directory"
    
    Parametri:
        path: Percorso di file o directory. La directory padre verrà creata
              con `parents=True` per garantire che tutte le cartelle intermedie esistano.
              `exist_ok=True` -> se la cartella esiste già, non dà errore.

    Ritorna:
        None
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Rilevamento e normalizzazione URL
# ------------------------------------------------------------

def is_url(s: str) -> bool:
    """
    Rileva se la stringa è un URL HTTP/HTTPS.

    Parametri:
        s: Stringa da testare.

    Ritorna:
        bool: True se `s` è un URL con schema http/https, altrimenti False.
    """
    try:
        parsed = urlparse(s) # suddivide l'URL in parti: scheme, netloc, path, query, fragment
        return parsed.scheme in {"http", "https"} # verifica se lo schema è http o https
    except Exception:
        return False


def to_github_raw(url: str) -> str:
    """
    Converte URL GitHub pagina in raw per pandas.

    Parametri:
        url: URL GitHub.
    
    Ritorna:
        str: URL GitHub raw.

    Note:
    GitHub serve i file via interfaccia web con URL del tipo:
    https://github.com/user/repo/blob/branch/path/to/file.csv
    Per scaricare il file grezzo (ad es. con pandas.read_csv) serve il link "raw":
    https://raw.githubusercontent.com/user/repo/branch/path/to/file.csv
    Pertanto, la funzione converte l'URL GitHub da versione web a versione raw 
    rimuovendo '/blob/' e cambiando dominio.

    Aggiunge ?raw=true per asset binari.
    """
    parsed = urlparse(url)
    netloc = parsed.netloc.lower() # netloc è la parte del dominio, come www.google.com

    # se è già raw o ha ?raw=true, lo restituisce così com'è
    if "raw.githubusercontent.com" in netloc or "?raw=true" in parsed.query: # query è la parte della query string, come ?raw=true
        return url
    
    # se è github.com e ha /blob/, lo converte in raw.githubusercontent.com
    if "github.com" in netloc and "/blob/" in parsed.path: # path è la parte del percorso, come /fruits.csv
        # Esempio: /owner/repo/blob/branch/file → /owner/repo/branch/file
        parts = parsed.path.split("/blob/")
        if len(parts) == 2:
            left, right = parts  # left="/owner/repo", right="main/file.csv"
            new_path = f"{left}/{right}"  # "/owner/repo/main/file.csv"
            return parsed._replace(  # Crea nuovo URL con componenti modificate
                scheme="https",
                netloc="raw.githubusercontent.com",  # Cambia dominio
                path=new_path,                       # Usa nuovo path
                query="",                            # Rimuove query string
            ).geturl()  # Ricostruisce l'URL completo
    
    # Per asset binari (es. immagini, PDF): il parametro ?raw=true
    # fa sì che GitHub restituisca il file grezzo invece di una pagina HTML.
    if "github.com" in netloc:
        
        # Prende la query string (la parte dopo il "?" nell'URL)
        q = parsed.query
        
        # Se non c'è già "raw=true", lo aggiunge
        if "raw=true" not in q:
            if q:  # Se esiste già qualche parametro, aggiunge con &
                q = q + "&raw=true"
            else:  # Altrimenti mette solo raw=true
                q = "raw=true"
        
        # Ricostruisce l'URL con la query aggiornata
        return parsed._replace(query=q).geturl()

    return url


# ------------------------------------------------------------
# Caricamento dataset
# ------------------------------------------------------------

def _read_local(path: Path, 
                *, 
                sheet: str | int | None, # sheet è il nome della scheda in Excel, oppure l'indice della scheda (es. 0 o "Sheet1")
                dtype: Mapping[str, Any] | None, # dtype è il tipo di dato per ogni colonna (es. {"age": int, "name": str})
                na_values: list | None # na_values è la lista dei valori mancanti da sostituire con NaN
) -> pd.DataFrame: 
    """
    Carica dataset *da locale* (CSV/Parquet/Excel).
    Le estensioni supportate sono .csv, .parquet, .xlsx/.xls.
   
    Parametri:
        path: Percorso del file.
        sheet: Nome della scheda in Excel, oppure indice della scheda (es. 0 o "Sheet1").
        dtype: Tipo di dato per ogni colonna (es. {"age": int, "name": str}).
        na_values: Lista dei valori mancanti da sostituire con NaN.
    
    Ritorna:
        pd.DataFrame: Dataset caricato.

    Eccezioni:
        ValueError: Se l'estensione non è supportata.
    """
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, dtype=dtype, na_values=na_values)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet, dtype=dtype, na_values=na_values)
    raise ValueError(f"Estensione file non supportata: {suffix}. Usa .csv, .parquet, .xlsx/.xls")


def _read_url(
        url: str, 
        *, 
        sheet: str | int | None,
        dtype: Mapping[str, Any] | None,
        na_values: list | None
) -> pd.DataFrame: 
    """
    Carica dataset *da URL* (GitHub raw).

    Parametri:
        url: URL del file da caricare.
        sheet: Nome della scheda in Excel, oppure indice della scheda (es. 0 o "Sheet1").
        dtype: Tipo di dato per ogni colonna (es. {"age": int, "name": str}).
        na_values: Lista dei valori mancanti da sostituire con NaN.
    
    Ritorna:
        pd.DataFrame: Dataset caricato.

    Eccezioni:
        ValueError: Se l'estensione non è supportata.
        ValueError: Se l'URL non è valido.
        ValueError: Se l'URL restituisce HTML invece di CSV.
    """
    normalized = to_github_raw(url)  # GitHub blob → raw per pandas
    parsed = urlparse(normalized) # suddivide l'URL in parti: scheme, netloc, path, query, fragment
    suffix = Path(parsed.path).suffix.lower() # salva l'estensione del file
    
    if suffix == ".csv":
        df = pd.read_csv(normalized, dtype=dtype, na_values=na_values)
    elif suffix == ".parquet":
        df = pd.read_parquet(normalized)
    elif suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(normalized, sheet_name=sheet, dtype=dtype, na_values=na_values)
    else:
        # Fallback: prova come CSV
        try:
            df = pd.read_csv(normalized, dtype=dtype, na_values=na_values)
        except Exception as exc:
            raise ValueError("File non supportato o URL non valido") from exc
    
    # Controllo: se sembra HTML invece di CSV
    if df.shape[1] <= 1 and df.shape[0] > 0 and df.iloc[0].astype(str).str.contains("<html|<!doctype", case=False, regex=True).any():
        raise ValueError("URL restituisce HTML: converti a raw")
    return df


def load_dataset(
        path_or_url: str,
        *,
        sheet: str | int | None = None,
        dtype: Mapping[str, Any] | None = None,
        na_values: list | None = None,
) -> pd.DataFrame:
    """
    Carica dataset da locale o URL (CSV/Parquet/Excel).
    Utilizza le funzioni _read_local e _read_url per caricare il dataset.

    Parametri:
        path_or_url: Percorso del file o URL del dataset.
        sheet: Nome della scheda in Excel, oppure indice della scheda (es. 0 o "Sheet1").
        dtype: Tipo di dato per ogni colonna (es. {"age": int, "name": str}).
        na_values: Lista dei valori mancanti da sostituire con NaN.

    Ritorna:
        pd.DataFrame: Dataset caricato.

    Eccezioni:
        FileNotFoundError: Se il file non è stato trovato.
    """
    if is_url(path_or_url):
        return _read_url(path_or_url, sheet=sheet, dtype=dtype, na_values=na_values)

    p = Path(path_or_url)
    if not p.exists():
        raise FileNotFoundError(f"File non trovato: {p}")
    return _read_local(p, sheet=sheet, dtype=dtype, na_values=na_values)


# ------------------------------------------------------------
# Salvataggio/lettura DataFrame
# ------------------------------------------------------------

def save_dataframe(df: pd.DataFrame, path: str) -> None:
    """
    Salva un DataFrame in CSV o Parquet in base all'estensione.

    Parametri:
        df: DataFrame da salvare.
        path: Percorso di destinazione (.csv o .parquet).
    
    Ritorna:
        None

    Eccezioni:
        ValueError: Se l'estensione non è supportata.
    """
    ensure_dir(path) # crea la directory se non esiste
    suffix = Path(path).suffix.lower() # salva l'estensione del file

    # Salva il DataFrame in CSV o Parquet in base all'estensione
    if suffix == ".csv":
        df.to_csv(path, index=False)
    elif suffix == ".parquet":
        df.to_parquet(path, index=False)
    else:
        raise ValueError("Solo formati .csv o .parquet sono supportati per save_dataframe.")


# ------------------------------------------------------------
# Persistenza modello con joblib
# ------------------------------------------------------------

def save_model(model: object, path: str) -> None:
    """
    Salva un oggetto modello *in locale* usando joblib.

    Parametri:
        model: Oggetto serializzabile da joblib.
        path: Percorso file di destinazione.

    Ritorna:
        None
    """
    ensure_dir(path)
    joblib_dump(model, path) # salva il modello in un file .joblib


def load_model(path: str) -> object:
    """
    Carica un modello *da locale* usando joblib.
    Restituisce un oggetto Python identico a quello salvato.

    Parametri:
        path: Percorso del file del modello.

    Ritorna:
        object: Modello deserializzato.
    """
    return joblib_load(path)


# ------------------------------------------------------------
# Metriche e risultati JSON
# ------------------------------------------------------------

def save_metrics(metrics: Mapping[str, Any],
                 path: str) -> None:
    """
    Salva un dizionario di metriche *in locale* in formato JSON UTF-8 con indentazione 2.

    Parametri:
        metrics: Dizionario di metriche/risultati.
        path: Percorso file di destinazione (.json).

    Ritorna:
        None
    """
    ensure_dir(path)
    # with open() per garantire che il file venga chiuso correttamente
    with open(path, "w", encoding="utf-8") as f: # apri il file e memorizza in f in modalità scrittura
        json.dump(dict(metrics),
                  f, # usa f come destinazione in cui salvare i dati.
                  ensure_ascii=False, 
                  indent=2)


def load_metrics(path: str) -> dict[str, Any]:
    """
    Carica un file JSON di metriche *da locale*.

    Parametri:
        path: Percorso del file .json

    Ritorna:
        dict[str, Any]: Metriche caricate.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------
# Salvataggio figure
# ------------------------------------------------------------

def save_plot(fig: "Figure", 
              path: str, 
              *, 
              dpi: int = 120,
              bbox_inches: str = "tight"
) -> None:
    """
    Salva figura matplotlib (PNG/SVG/PDF).
    Non chiude la figura per riuso.

    Parametri:
        fig: Figura matplotlib.
        path: Percorso del file di output.
        dpi: Risoluzione della figura (numero di pixel per pollice).
        bbox_inches: Area di contenimento della figura.
    """
    ensure_dir(path)
    fig.savefig(path, dpi=dpi, bbox_inches=bbox_inches)  # salva la figura


# ------------------------------------------------------------
# Operazioni pratiche frequenti (opzionali)
# ------------------------------------------------------------

def sample_dataset(
    df: pd.DataFrame,
    n: int | None = None,
    frac: float | None = None,
    random_state: int | None = None, 
) -> pd.DataFrame:
    """
    Estrae un campione del DataFrame (per debug o smoke test).

    Parametri:
        df: DataFrame di input.
        n: Numero di righe da campionare (mutualmente esclusivo con `frac`).
        frac: Frazione di righe da campionare (0 < frac <= 1).
        random_state: numero che fissa la sequenza casuale, così eseguendo il codice più volte si ottengono sempre gli stessi risultati.

    Ritorna:
        pd.DataFrame: Campione del dataset.

    Eccezioni:
        ValueError: Se sia `n` che `frac` sono specificati.
    """
    if n is not None and frac is not None:
        raise ValueError("Specificare solo uno tra 'n' e 'frac'.")
    return df.sample(n=n, frac=frac, random_state=random_state)


def export_predictions(
    ids: pd.Series | None,
    y_pred: "np.ndarray | pd.Series",
    path: str,
    id_name: str = "id",
    target_name: str = "prediction",
) -> None:
    """
    Esporta le predizioni in CSV, includendo opzionalmente una colonna ID.

    Parametri:
        ids: Serie con identificativi (opzionale).
        y_pred: Predizioni come array/Serie.
        path: Percorso del file CSV di output.
        id_name: Nome della colonna ID.
        target_name: Nome della colonna delle predizioni.
    """
    
    ensure_dir(path)

    # Converte il parametro y_pred in una Series con nome 'target_name'
    pred_array = np.asarray(y_pred)                         # garantisce che sia un array NumPy, invece che una lista
    pred_series = pd.Series(pred_array, name=target_name)   # converte l'array in una Series con nome 'target_name'

    # Crea il DataFrame finale
    if ids is not None:
        # Se sono presenti ID, crea un DataFrame con due colonne
        ids_reset = ids.reset_index(drop=True)          # resetta l'indice degli ID
        out = pd.DataFrame({id_name: ids_reset, target_name: pred_series})
    else:
        # Altrimenti crea un DataFrame con solo la colonna delle predizioni
        out = pred_series.to_frame()

    # 4. Salva il DataFrame in CSV
    out.to_csv(path, index=False)


def timestamped_path(base_dir: str, stem: str, ext: str = ".json") -> str:
    """
    Genera un percorso con timestamp: base_dir/YYYY-MM-DD_HHMMSS_stem.ext

    Parametri:
        base_dir: Directory base da creare se mancante.
        stem: Parte centrale del nome file.
        ext: Estensione (incluso il punto), default .json.

    Ritorna:
        str: Percorso completo come stringa.
    """
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return str(Path(base_dir) / f"{ts}_{stem}{ext}")


