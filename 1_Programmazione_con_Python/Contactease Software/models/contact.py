# models/contact.py

# Modulo per la gestione dei contatti telefonici.
# Contiene la classe Contact che rappresenta un singolo contatto con
# informazioni di base (nome, cognome, telefono) e campi opzionali.

__all__ = ["Contact"]

class Contact:
    """
    Rappresenta un contatto telefonico della rubrica.
    
    Attributi:
        nome: Nome della persona.
        cognome: Cognome della persona.
        telefono: Numero di telefono.
        email: Indirizzo email (opzionale).
        note: Note aggiuntive (opzionali).
        id: Identificativo univoco.
    """

    def __init__(self, nome, cognome, telefono, 
                 email=None, note=None, id=None):
        """
        Inizializza un nuovo contatto.
        """
        self.nome = nome
        self.cognome = cognome
        self.telefono = telefono
        self.email = email
        self.note = note
        self.id = id

    def __str__(self):
        """
        Restituisce una rappresentazione del contatto.
        """
        testo = f"{self.nome} {self.cognome} - Tel: {self.telefono}"
        
        # Aggiunge l'email se presente.
        if self.email:
            testo += f"\nEmail: {self.email}"
        
        # Aggiunge una nota se presente.
        if self.note:
            testo += f"\nNote: {self.note}"
            
        return testo

    def to_dict(self):
        """
        Converte il contatto in formato dizionario.
        """
        return {
            'nome': self.nome,
            'cognome': self.cognome,
            'telefono': self.telefono,
            'email': self.email,
            'note': self.note,
            'id': self.id,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Questa funzione crea un nuovo contatto partendo da un dizionario.
        """
        return cls(
            nome=data['nome'],
            cognome=data['cognome'],
            telefono=data['telefono'],
            email=data.get('email'),
            note=data.get('note'),
            id=data.get('id'),
        )