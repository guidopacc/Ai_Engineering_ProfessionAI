# ContactEase
## Gestore di contatti da terminale in Python

---

## Descrizione

ContactEase è un programma Python che gestisce una rubrica personale da riga di comando. Permette di aggiungere, modificare, eliminare e cercare contatti, con persistenza automatica su file JSON.

Funzionalità principali:
- Aggiungere nuovi contatti con nome, cognome, telefono, email e note
- Modificare o eliminare contatti esistenti
- Cercare contatti per nome, cognome o parte del numero di telefono
- Visualizzare l'intera rubrica

---

## Autore e contesto

**Autore:** Guido Pacciani  
Sviluppato come progetto finale del modulo *"Python Programming"* del **Master Professionale in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

---

## Struttura del progetto

```
Contactease Software/
├── main.py                 # Punto di ingresso del programma
├── pyproject.toml          # Configurazione del progetto
├── contacts.json           # File dati (creato automaticamente al primo uso)
├── cli/
│   └── menu.py             # Gestione del menu e interazione utente
├── models/
│   └── contact.py          # Definizione della classe Contact
├── repositories/
│   └── contact_repo.py     # Caricamento e salvataggio contatti su JSON
├── services/
│   └── contact_service.py  # Logica di business e validazione input
└── utils/
    └── validators.py       # Validazione telefono ed email
```

---

## Requisiti e installazione

- Python 3.10 o superiore

Nessuna dipendenza esterna. Scarica i file del progetto e avvia direttamente:

```bash
python main.py
```

---

## Come usare

All'avvio compare un menu testuale:

```
=== CONTACTEASE ===
1. Aggiungi contatto
2. Modifica contatto
3. Elimina contatto
4. Cerca contatti
5. Lista contatti
0. Esci
```

### Aggiungere un contatto

1. Scegli l'opzione `1`
2. Inserisci nome, cognome e telefono (obbligatori)
3. Email e note sono opzionali
4. Il contatto viene salvato con un ID generato automaticamente

### Modificare un contatto

1. Scegli l'opzione `2`, poi seleziona l'ID del contatto da aggiornare e inserisci i nuovi valori

### Eliminare un contatto

1. Scegli l'opzione `3`, inserisci l'ID e conferma con `s`

### Cercare contatti

1. Scegli l'opzione `4` e inserisci una stringa di ricerca (parte del nome, cognome o numero)

---

## Formato dei dati e validazione

### Telefono

- Almeno 8 cifre numeriche
- Può iniziare con `+` (es. `+39123456789`)
- Spazi ammessi per leggibilità (es. `123 456 7890`)

### Email (opzionale)

- Formato standard `nome@dominio.com`

### ID contatto

Generato automaticamente nel formato `[Iniziale Nome][Iniziale Cognome][Ultime 4 cifre telefono]`.

Esempio: Guido Pacciani, telefono 1234567890 → ID `GP7890`

---

## Approfondimento tecnico

Il progetto è organizzato secondo un'architettura a strati ispirata al pattern **Repository**:

- **`models/contact.py`**: definisce la struttura dati del contatto come classe Python
- **`repositories/contact_repo.py`**: gestisce la persistenza (lettura/scrittura su JSON), separando il layer dati dalla logica applicativa
- **`services/contact_service.py`**: contiene la logica di business — validazione, generazione ID, orchestrazione delle operazioni CRUD
- **`cli/menu.py`**: interfaccia utente testuale, disaccoppiata dalla logica interna
- **`utils/validators.py`**: funzioni pure di validazione con regex per telefono ed email

Questa separazione permette di testare ogni strato indipendentemente dagli altri.

---

## Risoluzione problemi

**Il programma non si avvia**
- Verifica la versione Python: `python --version` (richiesta 3.10+)
- Su alcuni sistemi usa `python3 main.py`

**I contatti non vengono salvati**
- Controlla che il file `contacts.json` non sia corrotto (deve contenere JSON valido)

---

## Licenza

Rilasciato con licenza **MIT** — libero per uso personale, studio o sviluppo. Clona e modifica liberamente.
