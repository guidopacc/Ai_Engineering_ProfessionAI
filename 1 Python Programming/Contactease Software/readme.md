# ContactEase

Una rubrica telefonica da riga di comando per gestire i contatti telefonici.

## Descrizione

ContactEase è un programma Python che permette di:
* Aggiungere nuovi contatti con nome, cognome, telefono, email e note
* Modificare contatti esistenti
* Eliminare contatti
* Cercare contatti per nome, cognome o telefono
* Visualizzare tutti i contatti salvati

I contatti vengono salvati automaticamente in un file JSON.

## Requisiti

* Python 3.10 o superiore

## Come installare

1. Scarica tutti i file del progetto
2. Apri il terminale/prompt dei comandi nella cartella del progetto

## Come usare

Avvia il programma con:

```bash
python main.py
```

Vedrai un menu con queste opzioni:

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
3. Inserisci email e note (opzionali)
4. Il contatto verrà salvato con un ID unico generato automaticamente

### Modificare un contatto

1. Scegli l'opzione `2`
2. Vedrai la lista degli ID e nomi dei contatti
3. Inserisci l'ID del contatto da modificare
4. Inserisci i nuovi dati

### Eliminare un contatto

1. Scegli l'opzione `3`
2. Inserisci l'ID del contatto da eliminare
3. Conferma con `s` per procedere

### Cercare contatti

1. Scegli l'opzione `4`
2. Inserisci il testo da cercare (può essere parte del nome, cognome o telefono)
3. Vedrai tutti i contatti che corrispondono alla ricerca

### Visualizzare tutti i contatti

1. Scegli l'opzione `5`
2. Vedrai la lista completa di tutti i contatti salvati

## Formato dei dati

### Telefono

* Deve contenere almeno 8 cifre
* Può iniziare con `+` (es. `+39123456789`)
* Sono accettati spazi per la leggibilità (es. `123 456 7890`)

### Email (opzionale)

* Deve essere in formato valido (es. `nome@dominio.com`)
* Può essere lasciata vuota

### ID contatto

Gli ID vengono generati automaticamente nel formato: `[Iniziale Nome][Iniziale Cognome][Ultime 4 cifre telefono]`

Esempio: Guido Pacciani con telefono 1234567890 → ID: `GP7890`

## Struttura del progetto

```
progetto-contactease/
├── main.py                 # File principale per avviare il programma
├── pyproject.toml          # Configurazione del progetto
├── contacts.json           # File dove vengono salvati i contatti (creato automaticamente)
├── cli/
│   ├── __init__.py
│   └── menu.py            # Gestione del menu e interazione utente
├── models/
│   ├── __init__.py
│   └── contact.py         # Definizione della classe Contact
├── repositories/
│   ├── __init__.py
│   └── contact_repo.py    # Gestione salvataggio/caricamento contatti
├── services/
│   ├── __init__.py
│   └── contact_service.py # Logica di business e validazione
└── utils/
    ├── __init__.py
    └── validators.py       # Funzioni per validare telefono ed email
```

## Dove vengono salvati i contatti

I contatti vengono salvati nel file `contacts.json` nella stessa cartella del programma. Questo file viene creato automaticamente la prima volta che aggiungi un contatto.

## Risoluzione problemi

### Il programma non si avvia

* Controlla di avere Python 3.10 o superiore: `python --version`
* Assicurati di essere nella cartella giusta
* Prova con `python3 main.py` se `python main.py` non funziona

### I contatti non vengono salvati

* Se il file `contacts.json` esiste, controlla che non sia corrotto

---

Grazie per aver scaricato la mia soluzione di Contactease.