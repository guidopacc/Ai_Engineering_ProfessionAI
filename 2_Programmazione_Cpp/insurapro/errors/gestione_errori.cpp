/*
 * gestione_errori.cpp - Implementazione delle funzioni di gestione errori
 * Fornisce funzioni centralizzate per la gestione e la visualizzazione degli errori
 * relativi alle operazioni sui clienti, come la verifica dell'esistenza tramite codice fiscale
 * e la stampa di messaggi di errore.
 */

#include "gestione_errori.h"
#include <iostream>

// Funzione per mostrare un messaggio di errore se la condizione è vera
bool mostraErrore(bool condizione, std::string messaggio) {
    if (condizione) {
        if (messaggio.empty()) {
            std::cerr << "Errore.\n";
        } else {
            std::cerr << "Errore: " << messaggio << "\n";
        }
        return true;
    }
    return false;
}

// Funzione per controllare l'esistenza di un cliente tramite codice fiscale
int controllaEsistenzaCliente(std::vector<Cliente>& clienti, std::string codiceFiscale) {
    for (size_t i = 0; i < clienti.size(); i++) {               // Scorre tutti i clienti
        if (clienti[i].getCodiceFiscale() == codiceFiscale) {   // Confronta il codice fiscale del cliente corrente
            return static_cast<int>(i);                         // Restituisce l'indice del cliente se trovato
        }
    }
    std::cout << "Errore: cliente non trovato!\n";              // Stampa un messaggio se il cliente non è stato trovato
    return -1;                                                  // Restituisce -1 per indicare che il cliente non esiste
}

// Funzione per stampare un messaggio di errore rivolto all'utente
void stampaErroreUtente(std::string messaggio) {
    std::cout << messaggio << "\n";
}

// Funzione per stampare un messaggio di errore di sistema
void stampaErroreSistema(std::string messaggio) {
    std::cerr << messaggio << "\n";
}

/*
 * FUNZIONAMENTO:
 * Questo file implementa funzioni di utilità per la gestione centralizzata degli errori:
 * - mostraErrore: stampa un messaggio e restituisce true se la condizione di errore è verificata
 * - controllaEsistenzaCliente: ricerca un cliente tramite codice fiscale e restituisce l'indice o -1
 * - stampaErroreUtente: stampa un messaggio di errore rivolto all'utente
 * - stampaErroreSistema: stampa un messaggio di errore di sistema
 * Queste funzioni favoriscono la robustezza e la leggibilità del codice principale.
 */
