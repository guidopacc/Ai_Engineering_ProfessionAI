# services/contact_service.py

# Modulo per la gestione dei contatti con validazione dati.

from models.contact import Contact
from repositories.contact_repo import ContactRepository
from utils.validators import validate_contact

__all__ = ["ContactService"]

class ContactService:
    """
    Classe designata alla gestione e validazione dei contatti.
    """
    
    def __init__(self, repository):
        """
        Inizializza il repository specificato per la memorizzazione del file.
        """

        self.repository = repository

    def add_contact(self, nome, cognome, telefono, email=None, note=None):
        """
        Aggiunge un nuovo contatto dopo validazione.
        """

        # Valida telefono ed email.
        ok, msg = validate_contact(telefono, email)
        if not ok:
            return False, msg
        
        # Crea il nuovo contatto.
        contact = Contact(nome, cognome, telefono, email, note)

        # Salva e restituisce l'ID assegnato.
        contact_id = self.repository.add(contact)
        return True, contact_id

    def update_contact(self, contact_id, nome, cognome, telefono, email=None, note=None):
        """
        Modifica un contatto esistente dopo validazione.
        """

        # Valida i nuovi dati.
        ok, msg = validate_contact(telefono, email)
        if not ok:
            return False, msg
        
        # Crea il contatto con i dati aggiornati.
        nuovo = Contact(
            nome=nome,
            cognome=cognome,
            telefono=telefono,
            email=email,
            note=note,
            id=contact_id
        )

        # Aggiorna il contatto nel repository.
        if self.repository.update_by_id(contact_id, nuovo):
            return True, "Contatto aggiornato con successo"
        
        # Contatto non trovato.
        return False, "ID contatto non valido"
    
    def remove_contact(self, contact_id):
        """
        Rimuove un contatto tramite ID.
        """

        # Tenta la rimozione se il contatto è presente in memoria.
        if self.repository.remove(contact_id):
            return True, "Contatto rimosso con successo"
        
        # Contatto non trovato
        return False, "ID contatto non valido"
    
    def get_all_contacts(self):
        """
        Restituisce tutti i contatti della rubrica.
        """

        return self.repository.get_all()
    
    def search_contacts(self, query):
        """
        Cerca contatti per nome, cognome o telefono.
        """
        
        return self.repository.find_by_name(query)
