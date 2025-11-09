/*
 * crm.h - Definizione della classe CRM
 * Gestisce tutte le operazioni del sistema: clienti, interazioni, salvataggio/caricamento
 * Classe principale che coordina tutte le funzionalità del CRM
 */

#ifndef CRM_H
#define CRM_H

#include <vector>
#include <string>
#include "cliente.h"

// Definizione della classe principale CRM
class CRM {
private:
    std::vector<Cliente> clienti;
    std::string nomeFileClienti;
    std::string nomeFileInterazioni;
    
public:
    CRM(); // Costruttore della classe CRM
    
    // Metodi pubblici per la gestione dei clienti
    void aggiungiCliente();
    void visualizzaClienti();
    void modificaCliente();
    void eliminaCliente();
    void cercaCliente();
    
    // Metodi pubblici per la gestione delle interazioni
    void aggiungiInterazione();
    void visualizzaInterazioniCliente();
    void cercaInterazioni();
    void eliminaInterazione();
    void modificaInterazione();

    
    // Metodi per la persistenza dei dati
    bool salvaDati();
    bool caricaDati();
    
private:
    // Metodi di utilità privati
    int trovaCliente(std::string codiceFiscale);
    int trovaCliente(std::string nome, std::string cognome);
    void stampaMenuTipiInterazione();
    TipoInterazione scegliTipoInterazione();
    bool validaData(std::string data);
    bool validaOra(std::string ora);
    std::string ottieniInputSicuro(std::string messaggio);
};

#endif

/*
 * FUNZIONAMENTO:
 * La classe CRM è il cuore del sistema che:
 * - Mantiene un vettore di tutti i clienti dell'impresa
 * - Fornisce metodi per tutte le operazioni CRUD sui clienti
 * - Gestisce le interazioni associate a ogni cliente
 * - Implementa salvataggio e caricamento dati su file
 * - Include metodi di utilità per validazione e gestione input
 * - Coordina tutte le funzionalità del sistema CRM
 */ 