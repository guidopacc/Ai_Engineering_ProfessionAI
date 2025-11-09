# repositories/contact_repo.py

# Modulo per la gestione del salvataggio e del caricamento dei contatti da file.

import json
from pathlib import Path
from models.contact import Contact

__all__ = ["ContactRepository"]

class ContactRepository:
    """
    Gestore per la persistenza dei contatti.
    
    Salva e carica i contatti da file.
    """
    
    def __init__(self, file_path="contacts.json"):
        # Memorizza il percorso del file dei contatti.
        self.file_path = Path(file_path)
        
        # Genera una lista vuota per i contatti.
        self.contacts = []
        
        # Carica i contatti (se esistono) dal file.
        self.load_from_file()

    def _generate_id(self, contact):
        """
        Crea un codice univoco per ogni contatto.
        Prende le iniziali del nome e cognome e le ultime 4 cifre del telefono.
        """
        
        # Rimuove spazi e "+" dal numero di telefono.
        phone = contact.telefono.replace(" ", "").replace("+", "")
        
        # Genera il codice id con le iniziali e le ultime 4 cifre.
        base = contact.nome[0].upper() + contact.cognome[0].upper() + phone[-4:]
        
        # Se l'ID esiste già, aggiunge suffisso incrementale (-1, -2, ecc.).
        suffix = 0
        new_id = base
        existing_ids = {c.id for c in self.contacts}
        while new_id in existing_ids:
            suffix += 1
            new_id = f"{base}-{suffix}"
        return new_id
    
    def add(self, contact):
        """
        Aggiunge un contatto alla rubrica e restituisce l'ID assegnato.
        """
        
        # Assegna un ID se mancante.
        if contact.id is None:
            contact.id = self._generate_id(contact)

        # Aggiunge il contatto alla lista.
        self.contacts.append(contact)

        # Salva la lista completa dei contatti nel file.
        self.save_to_file()

        # Restituisce il codice del contatto aggiunto.
        return contact.id
    
    def update_by_id(self, contact_id, new_data):
        """
        Modifica un contatto esistente tramite ID.
        """

        # Ricerca del contatto.
        for i, c in enumerate(self.contacts):
            if c.id == contact_id:

                # Mantiene lo stesso ID.
                new_data.id = contact_id

                # Sostituisce il contatto esistente.
                self.contacts[i] = new_data

                # Salva le modifiche nel file.
                self.save_to_file()
                return True
            
        # Contatto non trovato
        return False
    
    def remove(self, contact_id):
        """
        Rimuove un contatto dalla rubrica tramite ID.
        """

        # Cerca il contatto con l'ID specificato.
        for i, c in enumerate(self.contacts):
            if c.id == contact_id:

                # Rimuove il contatto dalla lista.
                self.contacts.pop(i)

                # Salva le modifiche nel file.
                self.save_to_file()
                return True
            
        # Contatto non trovato.
        return False
    
    def get_all(self):
        """
        Restituisce tutti i contatti della rubrica.
        """

        # Restituisce una copia della lista contatti.
        return self.contacts.copy()
    
    def find_by_name(self, query):
        """
        Cerca contatti per nome, cognome o telefono.
        """

        # Converte la ricerca in minuscolo.
        query = query.lower()

        # Inizializza una lista per i risultati della ricerca.
        risultati = []

        # Controlla ogni contatto.
        for contact in self.contacts:
            if query in contact.nome.lower() or query in contact.cognome.lower() or query in contact.telefono:
                risultati.append(contact)

        # Ritorna la lista dei risultati.
        return risultati
    
    def save_to_file(self):
        """
        Salva i contatti nel file.
        """

        # Converte i contatti in dizionari.
        data = [contact.to_dict() for contact in self.contacts]

        # Crea la cartella se non esiste.
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Salva nel file.
        try:
            with self.file_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        # Gestisce eventuali eccezioni.
        except Exception as e:
            print(f"[ERRORE] Impossibile salvare i contatti:\n{e}\nNel file: {self.file_path}")
    
    def load_from_file(self):
        """
        Carica i contatti dal file.
        """

        # Se il file non esiste, inizializza lista vuota.
        if not self.file_path.exists():
            self.contacts = []
            return
        
        # Legge dal file.
        try:
            with self.file_path.open("r", encoding="utf-8") as f:

                # Legge il contenuto JSON.
                data = json.load(f)

                # Converte i dizionari in oggetti Contact.
                self.contacts = [Contact.from_dict(d) for d in data]
                
        # Gestisce eventuali eccezioni
        except Exception as e:
            print(f"[ERRORE] Impossibile caricare i contatti:\n{e}\nNel file: {self.file_path}")
            self.contacts = []