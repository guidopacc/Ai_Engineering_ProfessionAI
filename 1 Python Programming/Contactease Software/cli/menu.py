# cli/menu.py

# Modulo per la gestione dell'interfaccia utente e del menu principale.

from services.contact_service import ContactService

__all__ = ["Menu"]

# Dizionario con le opzioni disponibili nel menu principale.
MENU_OPTIONS = {
    "1": "Aggiungi contatto",
    "2": "Modifica contatto",
    "3": "Elimina contatto",
    "4": "Cerca contatti",
    "5": "Lista contatti",
    "0": "Esci"
}

class Menu:
    """
    Gestisce il menu principale e le interazioni con l'utente.
    """
    
    def __init__(self, service):

        # Memorizza il servizio per la gestione dei contatti.
        self.service = service

    def show_menu(self):
        """
        Visualizza il menu principale dell'applicazione.
        """
        
        # Stampa l'intestazione dell'applicazione.
        print("\n=== CONTACTEASE ===")
        
        # Mostra tutte le opzioni disponibili.
        for key, value in MENU_OPTIONS.items():
            print(f"{key}. {value}")

    def get_input(self, prompt):
        """
        Richiede input dall'utente.
        """
        
        # Chiede input all'utente e rimuove spazi bianchi.
        return input(f"\n{prompt} ").strip()

    def add_contact(self):
        """
        Gestisce l'aggiunta di un nuovo contatto.
        """
        
        # Mostra l'intestazione della sezione.
        print("\n=== AGGIUNGI CONTATTO ===")
        
        # Raccoglie i dati obbligatori del contatto.
        nome = self.get_input("Nome:")
        cognome = self.get_input("Cognome:")
        telefono = self.get_input("Telefono:")
        
        # Raccoglie i dati opzionali del contatto.
        email = self.get_input("Email (opzionale):")
        note = self.get_input("Note (opzionale):")

        # Chiama il servizio per aggiungere il contatto.
        ok, msg = self.service.add_contact(
            nome=nome, 
            cognome=cognome, 
            telefono=telefono, 
            email=email if email else None, 
            note=note if note else None
        )

        # Mostra il risultato dell'operazione.
        if ok:
            print(f"Contatto aggiunto con ID: {msg}")
        else:
            print(f"Errore: {msg}")

    def update_contact(self):
        """
        Gestisce la modifica di un contatto esistente.
        """
        
        # Mostra l'intestazione della sezione.
        print("\n=== MODIFICA CONTATTO ===")
        
        # Recupera tutti i contatti disponibili.
        contacts = self.service.get_all_contacts()
        if not contacts:
            print("Nessun contatto presente")
            return

        # Visualizza l'elenco dei contatti disponibili.
        print("\nContatti disponibili:")
        for contact in contacts:
            print(f"ID: {contact.id} - {contact.nome} {contact.cognome}")

        # Chiede all'utente quale contatto modificare.
        contact_id = self.get_input("\nInserisci l'ID del contatto da modificare (o premi invio per tornare al menu):")
        if not contact_id:
            return

        # Raccoglie i nuovi dati del contatto.
        nome = self.get_input("Nuovo nome:")
        cognome = self.get_input("Nuovo cognome:")
        telefono = self.get_input("Nuovo telefono:")
        email = self.get_input("Nuova email (opzionale):")
        note = self.get_input("Nuove note (opzionale):")

        # Chiama il servizio per aggiornare il contatto.
        ok, msg = self.service.update_contact(
            contact_id=contact_id, 
            nome=nome, 
            cognome=cognome, 
            telefono=telefono, 
            email=email if email else None, 
            note=note if note else None
        )

        # Mostra il risultato dell'operazione.
        if ok:
            print("Contatto aggiornato con successo")
        else:
            print(f"Errore: {msg}")

    def remove_contact(self):
        """
        Gestisce l'eliminazione di un contatto.
        """
        
        # Mostra l'intestazione della sezione.
        print("\n=== ELIMINA CONTATTO ===")
        
        # Recupera tutti i contatti disponibili.
        contacts = self.service.get_all_contacts()
        if not contacts:
            print("Nessun contatto presente")
            return

        # Visualizza l'elenco dei contatti disponibili.
        print("\nContatti disponibili:")
        for contact in contacts:
            print(f"ID: {contact.id} - {contact.nome} {contact.cognome}")

        # Chiede all'utente quale contatto eliminare.
        contact_id = self.get_input("\nInserisci l'ID del contatto da eliminare (o premi invio per tornare al menu):")
        if not contact_id:
            return

        # Richiede conferma prima dell'eliminazione.
        confirm = self.get_input("Sei sicuro? (s/n):")
        if confirm.lower() != "s":
            print("Operazione annullata")
            return

        # Chiama il servizio per eliminare il contatto.
        ok, msg = self.service.remove_contact(contact_id)
        
        # Mostra il risultato dell'operazione.
        if ok:
            print("Contatto eliminato con successo")
        else:
            print(f"Errore: {msg}")

    def search_contacts(self):
        """
        Gestisce la ricerca dei contatti.
        """
        
        # Mostra l'intestazione della sezione.
        print("\n=== CERCA CONTATTI ===")
        
        # Chiede il termine di ricerca all'utente.
        query = self.get_input("Inserisci il testo da cercare:")
        if not query:
            print("Nessun termine di ricerca specificato")
            return

        # Esegue la ricerca tramite il servizio.
        results = self.service.search_contacts(query)
        
        # Controlla se ci sono risultati.
        if not results:
            print("Nessun contatto trovato")
            return

        # Visualizza i risultati della ricerca.
        print(f"\nTrovati {len(results)} contatti:")
        for contact in results:
            print(f"\nID: {contact.id}")
            print(f"Nome: {contact.nome}")
            print(f"Cognome: {contact.cognome}")
            print(f"Telefono: {contact.telefono}")
            
            # Mostra email solo se presente.
            if contact.email:
                print(f"Email: {contact.email}")
                
            # Mostra note solo se presenti.
            if contact.note:
                print(f"Note: {contact.note}")

    def list_contacts(self):
        """
        Visualizza tutti i contatti presenti nella rubrica.
        """
        
        # Mostra l'intestazione della sezione.
        print("\n=== LISTA CONTATTI ===")
        
        # Recupera tutti i contatti dal servizio.
        contacts = self.service.get_all_contacts()
        if not contacts:
            print("Nessun contatto presente")
            return

        # Visualizza ogni contatto con tutti i dettagli.
        for contact in contacts:
            print(f"\nID: {contact.id}")
            print(f"Nome: {contact.nome}")
            print(f"Cognome: {contact.cognome}")
            print(f"Telefono: {contact.telefono}")
            
            # Mostra email solo se presente.
            if contact.email:
                print(f"Email: {contact.email}")
                
            # Mostra note solo se presenti.
            if contact.note:
                print(f"Note: {contact.note}")

    def run(self):
        """
        Avvia il ciclo principale dell'applicazione.
        """
        
        # Loop principale del menu.
        while True:

            # Visualizza il menu delle opzioni.
            self.show_menu()
            choice = self.get_input("\nScelta:")

            # Gestisce la scelta dell'utente.
            if choice == "0":
                # Termina l'applicazione.
                print("\nArrivederci!")
                break

            elif choice == "1":
                # Aggiunge un nuovo contatto.
                self.add_contact()
    
            elif choice == "2":
                # Modifica un contatto esistente.
                self.update_contact()

            elif choice == "3":
                # Elimina un contatto.
                self.remove_contact()

            elif choice == "4":
                # Cerca contatti.
                self.search_contacts()

            elif choice == "5":
                # Visualizza tutti i contatti.
                self.list_contacts()

            else:
                # Gestisce scelte non valide.
                print("\nScelta non valida")