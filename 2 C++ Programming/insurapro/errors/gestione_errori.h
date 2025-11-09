/*
 * gestione_errori.h - Dichiarazioni delle funzioni per la gestione degli errori
 * Fornisce funzioni per la visualizzazione e la gestione degli errori relativi agli utenti e al sistema,
 * oltre a controlli sull'esistenza dei clienti.
 */

#ifndef GESTIONE_ERRORI_H
#define GESTIONE_ERRORI_H

#include <string>
#include <vector>
#include "../include/cliente.h"

// Funzione per mostrare un messaggio di errore se la condizione è vera
bool mostraErrore(bool condizione, std::string messaggio);

// Funzione per controllare l'esistenza di un cliente tramite codice fiscale
int controllaEsistenzaCliente(std::vector<Cliente>& clienti, std::string codiceFiscale);

// Funzione per stampare un messaggio di errore rivolto all'utente
void stampaErroreUtente(std::string messaggio);

// Funzione per stampare un messaggio di errore di sistema
void stampaErroreSistema(std::string messaggio);

#endif

/*
 * FUNZIONAMENTO:
 * Le funzioni definite in questo header file sono utilizzate per gestire gli errori nel sistema.
 * - `mostraErrore` visualizza un messaggio di errore se la condizione specificata è vera.
 * - `controllaEsistenzaCliente` verifica se un cliente esiste nella lista dei clienti confrontando il codice fiscale.
 * - `stampaErroreUtente` e `stampaErroreSistema` stampano rispettivamente messaggi di errore rivolti all'utente e al sistema,
 *   permettendo una chiara distinzione tra errori di input/output e problemi interni del sistema.
 */ 