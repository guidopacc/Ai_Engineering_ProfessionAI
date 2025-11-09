# InsuraPro Solutions CRM

InsuraPro Solutions CRM (Customer Relationship Management) è un sistema di gestione clienti da terminale, sviluppato in C++ per supportare le attività quotidiane delle imprese di assicurazioni.  
Consente di tracciare interazioni, appuntamenti, contratti, email e telefonate in modo strutturato e persistente.

---

## Descrizione

InsuraPro Solutions CRM permette di:

- Aggiungere, modificare, eliminare e cercare clienti
- Gestire appuntamenti, contratti, telefonate, email e altre interazioni (ogni interazione è tracciata con data, tipo e note)
- Salvare e caricare i dati automaticamente in file di testo
- Gestire errori in modo centralizzato tramite un modulo dedicato

---

## Struttura del progetto

```
insurapro/
│
├── src/                     # File sorgente principali (.cpp)
│   ├── main.cpp             # File principale con menu e logica generale
│   ├── crm.cpp              # Implementazione della classe CRM
│   ├── cliente.cpp          # Implementazione della classe Cliente
│   └── interazione.cpp      # Implementazione della classe Interazione
│
├── include/                 # File header (.h)
│   ├── crm.h                # Definizione della classe CRM
│   ├── cliente.h            # Definizione della classe Cliente
│   └── interazione.h        # Definizione della classe Interazione
│
├── errors/                  # Modulo gestione errori
│   ├── gestione_errori.cpp  # Funzioni di gestione errori
│   └── gestione_errori.h    # Header gestione errori
│
├── build/                   # File oggetto ed eseguibili (cartella generata dalla compilazione)
│   ├── insurapro_crm        # Eseguibile principale (Linux/macOS)
│   └── *.o                  # File oggetto
│
├── data/                    # File dati (cartella generata dalla compilazione)
│   ├── clienti.txt          # Dati anagrafici clienti
│   └── interazioni.txt      # Storico interazioni
│
├── README.md                # Documentazione del progetto
│
├── Makefile                 # File per la compilazione automatica
```

---

## Requisiti

- Compilatore C++ con supporto a C++11 (g++, clang++, Visual Studio)
- Sistema operativo: **Windows**, **macOS**, **Linux**
- Permessi di scrittura nelle cartelle `build/` e `data/`

---

## Installazione del compilatore

### macOS e Linux

1. Verifica la presenza di `g++` con:
   ```bash
   g++ --version
   ```
2. Se assente, installalo con:
   - **macOS**:
     ```bash
     brew install gcc
     ```
   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt update
     sudo apt install build-essential
     ```

---

### Windows (con MSYS2)

1. Premi `Win + R`, digita `cmd` e premi Invio  
2. Installa MSYS2 con winget:
   ```bash
   winget install -e --id MSYS2.MSYS2
   ```
3. Apri il terminale "MSYS2 MSYS" e aggiorna i pacchetti:
   ```bash
   pacman -Syu
   ```
4. Chiudi e riapri il terminale, poi installa il compilatore:
   ```bash
   pacman -S mingw-w64-x86_64-gcc
   ```

---

## Compilazione ed esecuzione

### macOS / Linux

1. Apri il terminale nella cartella del progetto:
   ```bash
   cd insurapro/
   ```

2. Compila con Makefile:
   ```bash
   make
   ```

3. Esegui:
   ```bash
   ./build/insurapro_crm
   ```

4. Pulisci i file generati:
   ```bash
   make clean
   ```

---

### Windows – Opzione 1: MinGW-w64 + Prompt dei comandi

1. Apri il prompt dei comandi nella cartella `insurapro/`

2. Compila:
   ```bash
   g++ -Iinclude -Ierrors -o build/insurapro_crm.exe src/*.cpp errors/*.cpp
   ```

3. Esegui:
   ```bash
   build/insurapro_crm.exe
   ```

4. Se serve, crea manualmente la cartella:
   ```bash
   mkdir build
   ```

---

### Windows – Opzione 2: Visual Studio

1. Crea un nuovo progetto C++ Console Application  
2. Aggiungi i file delle cartelle `src/`, `include/` ed `errors/`  
3. Imposta `include/` ed `errors/` come directory di inclusione  
4. Compila ed esegui direttamente da Visual Studio

---

## Note

- I dati vengono salvati in `data/` come `.txt`
- Le cartelle `data/` e `build/` vengono create se mancanti
- Assicurati di avere i permessi di scrittura in entrambe

---

## Licenza

**Autore:** Guido Pacciani  
**Il progetto è open source**, sviluppato per il corso _"Programmazione avanzata in C++"_ del **Master professionalizzante in AI Engineering** erogato da ProfessionAI.  
**Data di realizzazione:** Luglio 2025
