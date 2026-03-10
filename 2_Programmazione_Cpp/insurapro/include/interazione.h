/*
 * interazione.h - Definizione della classe Interazione
 * Rappresenta appuntamenti, contratti e altre interazioni con i clienti
 * Traccia la storia delle relazioni commerciali con ogni cliente
 */

#ifndef INTERAZIONE_H
#define INTERAZIONE_H

#include <string>

// Definizione dell'enumerazione TipoInterazione
enum TipoInterazione {
    APPUNTAMENTO,
    CONTRATTO,
    TELEFONATA,
    EMAIL,
    ALTRO
};

// Definizione della classe Interazione
class Interazione {
private:
    std::string data;
    std::string ora;
    TipoInterazione tipo;
    std::string descrizione;
    std::string agente;
    std::string risultato;
    
public:
    // Costruttore di default
    Interazione();
    
    // Costruttore con parametri
    Interazione(std::string data, std::string ora,
                TipoInterazione tipo, std::string descrizione,
                std::string agente, std::string risultato);
    
    // Metodi getter per accedere ai dati privati della classe
    std::string getData() { return data; }
    std::string getOra() { return ora; }
    TipoInterazione getTipo() { return tipo; }
    std::string getDescrizione() { return descrizione; }
    std::string getAgente() { return agente; }
    std::string getRisultato() { return risultato; }
    
    // Metodi setter per modificare i dati privati della classe
    void setData(std::string data) { this->data = data; }
    void setOra(std::string ora) { this->ora = ora; }
    void setTipo(TipoInterazione tipo) { this->tipo = tipo; }
    void setDescrizione(std::string descrizione) { this->descrizione = descrizione; }
    void setAgente(std::string agente) { this->agente = agente; }
    void setRisultato(std::string risultato) { this->risultato = risultato; }
    
    // Metodi di utilità per ottenere informazioni sull'interazione
    std::string getTipoStringa();
    void stampaDettagli();
    bool contieneStringa(std::string& ricerca);
};

#endif

/*
 * FUNZIONAMENTO:
 * La classe Interazione rappresenta ogni contatto o attività con un cliente:
 * - Traccia data, ora e tipo di interazione (appuntamento, contratto, telefonata, email)
 * - Memorizza descrizione dettagliata, agente responsabile e risultato
 * - Fornisce metodi per visualizzazione e ricerca nelle interazioni
 * - Utilizza enum per tipizzare le diverse categorie di interazione
 */ 