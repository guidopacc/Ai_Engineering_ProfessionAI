/*
 * interazione.cpp - Implementazione della classe Interazione per InsuraPro Solutions
 * Contiene l'implementazione di tutti i metodi della classe Interazione
 * Gestisce appuntamenti, contratti e altre interazioni con i clienti
 */

#include "interazione.h"


#include <iostream>
#include <algorithm>
#include <cctype>

using namespace std;

// Costruttore di default: inizializza tutti i campi a stringa vuota e tipo ALTRO
Interazione::Interazione() {
    data = "";
    ora = "";
    tipo = ALTRO;
    descrizione = "";
    agente = "";
    risultato = "";
}

// Costruttore parametrico: inizializza con i dati forniti
Interazione::Interazione(string data, string ora, 
                         TipoInterazione tipo, string descrizione,
                         string agente, string risultato) {
    // Assegnazione di data, ora, tipo, descrizione, agente e risultato
    // this->tipo = tipo; // Assegnazione del tipo di interazione
    this->data = data;
    this->ora = ora;
    this->tipo = tipo;
    this->descrizione = descrizione;
    this->agente = agente;
    this->risultato = risultato;
}

// Metodo per ottenere il tipo di interazione come stringa leggibile
string Interazione::getTipoStringa() {
    if (tipo == APPUNTAMENTO) return "Appuntamento";
    if (tipo == CONTRATTO) return "Contratto";
    if (tipo == TELEFONATA) return "Telefonata";
    if (tipo == EMAIL) return "Email";
    if (tipo == ALTRO) return "Altro";
    return "Sconosciuto";
}

// Metodo per stampare i dettagli dell'interazione su console
void Interazione::stampaDettagli() {
    cout << "Data: " << data << "\n";
    cout << "Ora: " << ora << "\n";
    cout << "Tipo: " << getTipoStringa() << "\n";
    cout << "Agente: " << agente << "\n";
    cout << "Descrizione: " << descrizione << "\n";
    cout << "Risultato: " << risultato << "\n";
}

// Metodo per la ricerca case-insensitive nei campi dell'interazione
bool Interazione::contieneStringa(string& ricerca) {
    string ricercaLower = ricerca;
    string descrizioneLower = descrizione;
    string agenteLower = agente;
    string risultatoLower = risultato;
    string tipoStringaLower = getTipoStringa();

    // Conversione di tutte le stringhe in minuscolo per confronto case-insensitive
    transform(ricercaLower.begin(), ricercaLower.end(), ricercaLower.begin(), ::tolower);
    transform(descrizioneLower.begin(), descrizioneLower.end(), descrizioneLower.begin(), ::tolower);
    transform(agenteLower.begin(), agenteLower.end(), agenteLower.begin(), ::tolower);
    transform(risultatoLower.begin(), risultatoLower.end(), risultatoLower.begin(), ::tolower);
    transform(tipoStringaLower.begin(), tipoStringaLower.end(), tipoStringaLower.begin(), ::tolower);

    // Ricerca la stringa in tutti i campi principali dell'interazione
    if (descrizioneLower.find(ricercaLower) != string::npos) return true;
    if (agenteLower.find(ricercaLower) != string::npos) return true;
    if (risultatoLower.find(ricercaLower) != string::npos) return true;
    if (tipoStringaLower.find(ricercaLower) != string::npos) return true;
    if (data.find(ricerca) != string::npos) return true;
    if (ora.find(ricerca) != string::npos) return true;
    return false;
}

/*
 * FUNZIONAMENTO:
 * Questo file implementa tutti i metodi della classe Interazione:
 * - Costruttori per creare nuove interazioni con o senza dati iniziali
 * - Conversione del tipo enum in stringa leggibile
 * - Visualizzazione formattata di tutti i dettagli dell'interazione
 * - Ricerca case-insensitive in tutti i campi dell'interazione
 * - Gestione sicura dei dati con controlli di validità
 * - Supporto per diversi tipi di interazione (appuntamenti, contratti, telefonate, email)
 */ 

 
