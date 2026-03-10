/*
 * cliente.cpp - Implementazione della classe Cliente
 * Contiene l'implementazione di tutti i metodi della classe Cliente
 * Gestisce i dati personali e le interazioni di ogni cliente
 */

#include "cliente.h"
#include "gestione_errori.h"

#include <iostream>
#include <algorithm>
#include <cctype>

using namespace std;

// Costruttore di default: inizializza tutti i campi a stringa vuota
Cliente::Cliente() {
    nome = "";
    cognome = "";
    email = ""; 
    telefono = "";
    indirizzo = "";
    codiceFiscale = "";
    dataNascita = "";
    // Il vettore interazioni è già vuoto di default
}

// Costruttore parametrico: inizializza con i dati forniti
Cliente::Cliente(string nome, string cognome, 
                 string email, string telefono,
                 string indirizzo, string codiceFiscale,
                 string dataNascita) {
    // Assegnazione di nome, cognome, email, telefono, indirizzo, codice fiscale e data di nascita
    // this->tipo = tipo; // Assegnazione del tipo di interazione
    this->nome = nome;
    this->cognome = cognome;
    this->email = email;
    this->telefono = telefono;
    this->indirizzo = indirizzo;
    this->codiceFiscale = codiceFiscale;
    this->dataNascita = dataNascita;
    // Il vettore interazioni rimane vuoto
}

// Metodo per aggiungere una nuova interazione al vettore del cliente
void Cliente::aggiungiInterazione(Interazione& interazione) {
    interazioni.push_back(interazione); // Aggiunge l'interazione alla fine del vettore
}

// Metodo per rimuovere un'interazione dal vettore (tramite indice)
void Cliente::rimuoviInterazione(int indice) {
    if (indice >= 0 && indice < (int)interazioni.size()) {
        interazioni.erase(interazioni.begin() + indice); // Rimuove l'elemento all'indice specificato
    }
}

// Metodo per visualizzare tutte le interazioni del cliente
void Cliente::visualizzaInterazioni() {
    if (interazioni.empty()) {
        stampaErroreUtente("Nessuna interazione registrata per questo cliente.");
        return;
    }

    cout << "\n=== INTERAZIONI DI " << getNomeCompleto() << " ===\n";
    for (size_t i = 0; i < interazioni.size(); i++) {
        cout << "\nInterazione #" << (i + 1) << ":\n";
        interazioni[i].stampaDettagli();
    }
}

// Metodo per ottenere nome e cognome del cliente come stringa completa
string Cliente::getNomeCompleto() {
    return nome + " " + cognome;
}

// Metodo per la ricerca case-insensitive nei campi principali del cliente
bool Cliente::contieneStringa(string& ricerca) {
    string ricercaLower = ricerca;
    string nomeLower = nome;
    string cognomeLower = cognome;
    string emailLower = email;
    string telefonoLower = telefono;

    // Conversione di tutte le stringhe in minuscolo per confronto case-insensitive
    transform(ricercaLower.begin(), ricercaLower.end(), ricercaLower.begin(), ::tolower);
    transform(nomeLower.begin(), nomeLower.end(), nomeLower.begin(), ::tolower);
    transform(cognomeLower.begin(), cognomeLower.end(), cognomeLower.begin(), ::tolower);
    transform(emailLower.begin(), emailLower.end(), emailLower.begin(), ::tolower);
    transform(telefonoLower.begin(), telefonoLower.end(), telefonoLower.begin(), ::tolower);
    
    // Ricerca la stringa in tutti i campi principali del cliente
    if (nomeLower.find(ricercaLower) != string::npos) return true;
    if (cognomeLower.find(ricercaLower) != string::npos) return true;
    if (emailLower.find(ricercaLower) != string::npos) return true;
    if (telefonoLower.find(ricercaLower) != string::npos) return true;
    if (codiceFiscale.find(ricerca) != string::npos) return true;
    return false;
}

// Metodo per stampare tutti i dettagli del cliente su console
void Cliente::stampaDettagli() {
    cout << "\n=== DETTAGLI CLIENTE ===\n";
    cout << "Nome: " << nome << "\n";
    cout << "Cognome: " << cognome << "\n";
    cout << "Email: " << email << "\n";
    cout << "Telefono: " << telefono << "\n";
    cout << "Indirizzo: " << indirizzo << "\n";
    cout << "Codice Fiscale: " << codiceFiscale << "\n";
    cout << "Data di Nascita: " << dataNascita << "\n";
    cout << "Numero di Interazioni: " << interazioni.size() << "\n";
}

/*
 * FUNZIONAMENTO:
 * Questo file implementa tutti i metodi della classe Cliente:
 * - Costruttori per creare nuovi clienti con o senza dati iniziali
 * - Gestione delle interazioni (aggiunta, rimozione, visualizzazione)
 * - Controlli di validità per evitare errori di accesso ai vettori
 * - Conversione automatica in minuscolo per ricerche più flessibili
 */ 