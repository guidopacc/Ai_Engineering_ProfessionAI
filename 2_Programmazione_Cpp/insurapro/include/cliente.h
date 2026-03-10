/*
 * cliente.h - Definizione della classe Cliente
 * Contiene tutte le informazioni personali e di contatto del cliente
 * Struttura dati principale per la gestione dei clienti assicurativi
 */

#ifndef CLIENTE_H
#define CLIENTE_H

#include <string>
#include <vector>
#include "interazione.h"

// Definizione della classe Cliente
class Cliente {
private:
    std::string nome;
    std::string cognome;
    std::string email;
    std::string telefono;
    std::string indirizzo;
    std::string codiceFiscale;
    std::string dataNascita;
    std::vector<Interazione> interazioni;
    
public:
    // Costruttore di default
    Cliente();
    
    // Costruttore con parametri (con argomenti di default)
    Cliente(std::string nome = "", std::string cognome = "",
            std::string email = "", std::string telefono = "",
            std::string indirizzo = "", std::string codiceFiscale = "",
            std::string dataNascita = "");
    
    // Metodi getter per accedere ai dati privati
    std::string getNome() { return nome; }
    std::string getCognome() { return cognome; }
    std::string getEmail() { return email; }
    std::string getTelefono() { return telefono; }
    std::string getIndirizzo() { return indirizzo; }
    std::string getCodiceFiscale() { return codiceFiscale; }
    std::string getDataNascita() { return dataNascita; }
    std::vector<Interazione> getInterazioni() { return interazioni; }
    
    // Metodi setter per modificare i dati
    void setNome(std::string n) { nome = n; }
    void setCognome(std::string c) { cognome = c; }
    void setEmail(std::string e) { email = e; }
    void setTelefono(std::string t) { telefono = t; }
    void setIndirizzo(std::string i) { indirizzo = i; }
    void setCodiceFiscale(std::string cf) { codiceFiscale = cf; }
    void setDataNascita(std::string dn) { dataNascita = dn; }
    
    // Metodi per la gestione delle interazioni
    void aggiungiInterazione(Interazione& interazione);
    void rimuoviInterazione(int indice);
    void visualizzaInterazioni();
    
    // Metodi di utilità
    std::string getNomeCompleto();
    bool contieneStringa(std::string& ricerca);
    void stampaDettagli();
    
    // Overloading operatore di confronto ==
    bool operator==(Cliente& other) {
        return codiceFiscale == other.codiceFiscale;
    }
};

#endif

/*
 * FUNZIONAMENTO:
 * La classe Cliente rappresenta un cliente dell'impresa di assicurazioni con:
 * - Dati personali completi (nome, cognome, email, telefono, indirizzo, CF, data nascita)
 * - Vettore di interazioni per tenere traccia di appuntamenti e contratti
 * - Metodi getter/setter per accesso controllato ai dati
 * - Funzionalità per gestire le interazioni associate al cliente
 * - Metodi di utilità per visualizzazione e ricerca
 */ 