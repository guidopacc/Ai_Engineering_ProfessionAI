# InsuraPro Solutions CRM
## Sistema di gestione clienti da terminale in C++

---

## Descrizione

InsuraPro Solutions CRM è un sistema di gestione clienti (Customer Relationship Management) da terminale, sviluppato in C++ per le attività quotidiane di un'impresa assicurativa. Consente di tracciare clienti, interazioni, appuntamenti, contratti e comunicazioni in modo strutturato, con persistenza automatica su file di testo.

Funzionalità principali:
- Aggiungere, modificare, eliminare e cercare clienti
- Registrare interazioni di diverso tipo: appuntamenti, contratti, telefonate, email
- Ogni interazione viene tracciata con data, tipo e note descrittive
- Salvataggio e caricamento automatici dei dati da file

---

## Autore e contesto

**Autore:** Guido Pacciani  
Sviluppato come progetto finale del modulo *"Programmazione avanzata in C++"* del **Master Professionale in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

---

## Struttura del progetto

```
insurapro/
├── src/                     # File sorgente (.cpp)
│   ├── main.cpp             # Menu principale e logica di flusso
│   ├── crm.cpp              # Implementazione della classe CRM
│   ├── cliente.cpp          # Implementazione della classe Cliente
│   └── interazione.cpp      # Implementazione della classe Interazione
├── include/                 # File header (.h)
│   ├── crm.h
│   ├── cliente.h
│   └── interazione.h
├── errors/                  # Modulo gestione errori
│   ├── gestione_errori.cpp
│   └── gestione_errori.h
├── build/                   # File oggetto ed eseguibile (generato dalla compilazione)
├── data/                    # File dati persistenti (generato dalla compilazione)
│   ├── clienti.txt
│   └── interazioni.txt
├── Makefile
└── README.md
```

---

## Requisiti

- Compilatore C++ con supporto C++11 (`g++`, `clang++`, Visual Studio)
- Sistema operativo: Windows, macOS, Linux
- Permessi di scrittura nelle cartelle `build/` e `data/`

---

## Installazione del compilatore

### macOS e Linux

Verifica la presenza di `g++`:
```bash
g++ --version
```

Se assente, installalo:
- **macOS**: `brew install gcc`
- **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install build-essential`

### Windows (con MSYS2)

1. Installa MSYS2: `winget install -e --id MSYS2.MSYS2`
2. Dal terminale MSYS2 aggiorna i pacchetti: `pacman -Syu`
3. Installa il compilatore: `pacman -S mingw-w64-x86_64-gcc`

---

## Compilazione ed esecuzione

### macOS / Linux

```bash
cd insurapro/
make
./build/insurapro_crm
```

Per pulire i file generati:
```bash
make clean
```

### Windows — MinGW-w64

```bash
g++ -Iinclude -Ierrors -o build/insurapro_crm.exe src/*.cpp errors/*.cpp
build/insurapro_crm.exe
```

### Windows — Visual Studio

1. Crea un progetto C++ Console Application
2. Aggiungi i file dalle cartelle `src/`, `include/` ed `errors/`
3. Imposta `include/` ed `errors/` come directory di inclusione
4. Compila ed esegui

---

## Approfondimento tecnico

Il progetto utilizza un design orientato agli oggetti con tre classi principali:

- **`Cliente`**: anagrafica del cliente (nome, cognome, dati di contatto, ID univoco)
- **`Interazione`**: singola interazione tracciata, con tipo enumerato (appuntamento, contratto, telefonata, email), data e note testuali
- **`CRM`**: classe aggregatrice che gestisce una collezione di clienti con le relative interazioni, espone le operazioni CRUD e coordina la persistenza

La gestione degli errori è centralizzata nel modulo `errors/gestione_errori`, separata dalla logica applicativa. I dati vengono serializzati come file di testo strutturato in `data/`, con caricamento automatico all'avvio del programma. Il `Makefile` gestisce la compilazione incrementale tramite file oggetto `.o`.

---

## Note

- Le cartelle `data/` e `build/` vengono create automaticamente se mancanti
- Assicurati di avere i permessi di scrittura in entrambe

---

## Licenza

Rilasciato con licenza **MIT** — libero per uso personale, studio o sviluppo. Clona e modifica liberamente.
