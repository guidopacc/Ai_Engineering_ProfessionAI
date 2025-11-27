# 📒 ContactEase

> Un gestore di contatti CLI (Command Line Interface) robusto, sviluppato in Python con un'architettura modulare.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-completed-brightgreen)

## 💡 Il Progetto

ContactEase non è una semplice rubrica. È un'applicazione progettata seguendo i principi della **Clean Architecture** e della **Separation of Concerns**. L'obiettivo era creare un tool che gestisse operazioni CRUD (Create, Read, Update, Delete) garantendo l'integrità dei dati tramite validazione rigorosa e persistenza su file JSON.

### ✨ Funzionalità Principali

* **Gestione CRUD Completa:** Aggiunta, modifica, rimozione e lettura dei contatti.
* **Validazione Dati Robusta:** Controllo automatico del formato email e numero di telefono (minimo 8 cifre, gestione prefissi internazionali).
* **Ricerca Intelligente:** Query flessibili per nome, cognome o numero.
* **Generazione ID Automatica:** Creazione di ID univoci basati su nome e numero per evitare collisioni.
* **Persistenza Dati:** Salvataggio automatico su `contacts.json` per mantenere i dati tra le sessioni.

---

## 🏗️ Architettura del Software

Il punto di forza di questo progetto è la struttura del codice, organizzata in moduli distinti per facilitare la manutenzione e la scalabilità:

```text
progetto-contactease/
├── main.py                 # Entry point dell'applicazione
├── models/
│   └── contact.py          # Data Model (La struttura del dato)
├── repositories/
│   └── contact_repo.py     # Data Layer (Gestione I/O su file JSON)
├── services/
│   └── contact_service.py  # Business Logic (Validazione e coordinamento)
├── cli/
│   └── menu.py             # Presentation Layer (Interfaccia Utente)
└── utils/
    └── validators.py       # Helper functions (Logica di validazione pura)
Questa struttura permette di cambiare, ad esempio, il metodo di salvataggio (da JSON a Database SQL) modificando solo il Repository, senza toccare il resto del programma.

🚀 Come iniziare
Prerequisiti

Python 3.10 o superiore.

Installazione ed Esecuzione

Clona la repository:

Bash
git clone [https://github.com/TUO-USERNAME/ContactEase.git](https://github.com/TUO-USERNAME/ContactEase.git)
cd ContactEase
Avvia il programma:

Bash
python main.py
🧪 Esempio di Utilizzo
Plaintext
=== CONTACTEASE ===
1. Aggiungi contatto
2. Modifica contatto
3. Elimina contatto
...
Scelta: 1

=== AGGIUNGI CONTATTO ===
Nome: Guido
Cognome: Pacciani
Telefono: +39 333 1234567
Email (opzionale): guido@example.com
...
Contatto aggiunto con successo!
👨‍💻 Autore
Sviluppato come progetto pratico per il modulo Python di ProfessionAI.      # Helper functions (Logica di validazione pura)
