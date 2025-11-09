# main.py

"""
Modulo principale.
"""

from cli.menu import Menu
from repositories.contact_repo import ContactRepository
from services.contact_service import ContactService

def main():
    """
    Funzione principale del programma.
    """

    # Generazione del repository dove salvare i contatti.
    repository = ContactRepository()
    
    # Generazione di un servizio che gestisce i contatti.
    service = ContactService(repository)
    
    # Generazione del menù mostrato all'utente.
    menu = Menu(service)
    
    # Avvio del programma.
    menu.run()

if __name__ == "__main__":
    main() 