# utils/validators.py

# Modulo che contiene tutte le funzioni di validazione utilizzate all'interno del programma.

# Ogni funzione restituisce tuple[bool, str]:
#  - (True, "") se il valore supera tutti i controlli.
#  - (False, msg) se viene rilevato un errore.

__all__ = ["validate_phone", "validate_email", "validate_contact"]

def validate_phone(phone):
    """
    Controlla la validità di un numero di telefono.
    """
    
    # Rimuove gli spazi dal numero.
    phone = phone.replace(" ", "")

    # Rimuove il carattere + dal prefisso internazionale (se presente).
    if phone.startswith("+"):
        phone = phone[1:]

    # Verifica la presenza di soli caratteri numerici.
    if not phone.isdigit():
        return False, (
            "Il numero di telefono deve contenere solo cifre "
            "(o iniziare con + per numeri internazionali)"
        )

    # Controlla che il numero contenga almeno 8 cifre
    if len(phone) < 8:
        return False, "Il numero di telefono deve essere composto da almeno 8 cifre"

    return True, ""


def validate_email(email):
    """
    Controlla la validità di una email.
    """

    # Campo email opzionale, nessuna validazione se vuoto.
    if not email:
        return True, ""

    # Rimuove gli spazi dal numero.
    email = email.replace(" ", "")

    # Divide l'email in parti.
    try:
        user_part, domain_part = email.split("@")
        domain, extension = domain_part.split(".")
    
    # Gestisce eventuali eccezioni.
    except ValueError:
        return False, "Email priva di '@' o di dominio/estensione"

    # Verifica del nome utente.
    for char in user_part:
        if not (char.isalnum() or char in "-_"):
            return False, "Carattere non valido nel nome utente"

    # Verifica del dominio.
    if not all(c.isalnum() or c == "-" for c in domain):
        return False, "Dominio non valido"

    # Verifica dell'estensione.
    if len(extension) > 3:
        return False, "Estensione troppo lunga"

    return True, ""

def validate_contact(telefono, email=None):
    """
    Utilizza le funzioni precedenti per effettuare una
    verifica completa di numero di telefono ed email.
    """
    
    # Verifica completa del numero di telefono.
    ok, msg = validate_phone(telefono)
    if not ok:
        return False, msg

    # Verifica completa della email.
    ok, msg = validate_email(email)
    if not ok:
        return False, msg

    # Validazione completata con successo.
    return True, ""

