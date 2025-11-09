/*
 * crm.cpp - Implementazione della classe CRM
 * Contiene l'implementazione di tutti i metodi della classe CRM
 * Gestisce tutte le operazioni del sistema: clienti, interazioni, file I/O
 */

#include "crm.h"
#include "gestione_errori.h"

#include <iostream>
#include <fstream>
#include <limits>
#include <algorithm>
#include <cctype>

using namespace std; 

// Costruttore: inizializza i nomi dei file per il salvataggio dei dati
CRM::CRM() {
    nomeFileClienti = "data/clienti.txt";         // File per i dati dei clienti
    nomeFileInterazioni = "data/interazioni.txt"; // File per i dati delle interazioni
    // Il vettore clienti è già vuoto di default
}

// Metodo per aggiungere un nuovo cliente al sistema
void CRM::aggiungiCliente() {
    cout << "\n=== AGGIUNGI NUOVO CLIENTE ===\n";
    
    string nome = ottieniInputSicuro("Nome: ");
    string cognome = ottieniInputSicuro("Cognome: ");
    string email = ottieniInputSicuro("Email: ");         
    string telefono = ottieniInputSicuro("Telefono: ");
    string indirizzo = ottieniInputSicuro("Indirizzo: "); 
    string codiceFiscale = ottieniInputSicuro("Codice Fiscale: ");
    string dataNascita = ottieniInputSicuro("Data di Nascita (DD/MM/YYYY): ");
    
    // Verifica se il cliente esiste già per codice fiscale
    if (trovaCliente(codiceFiscale) != -1) {
        cout << "Errore: Cliente con questo codice fiscale già presente!\n";
        return;
    }
    
    // Crea e aggiunge il nuovo cliente
    Cliente nuovoCliente(nome, cognome, email, telefono, indirizzo, codiceFiscale, dataNascita);
    clienti.push_back(nuovoCliente); // Inserisce il cliente nel vettore
    
    cout << "Cliente aggiunto con successo!\n";
}

// Metodo per visualizzare tutti i clienti presenti nel sistema
void CRM::visualizzaClienti() {
    if (mostraErrore(clienti.empty(), "Nessun cliente presente nel sistema.")) return; // Controllo presenza clienti
    
    cout << "\n=== LISTA CLIENTI ===\n";
    for (size_t i = 0; i < clienti.size(); i++) {
        cout << "\nCliente #" << (i + 1) << ":\n";
        cout << "Nome: " << clienti[i].getNomeCompleto() << "\n";
        cout << "Email: " << clienti[i].getEmail() << "\n";
        cout << "Telefono: " << clienti[i].getTelefono() << "\n";
        cout << "Codice Fiscale: " << clienti[i].getCodiceFiscale() << "\n";
        cout << "Interazioni: " << clienti[i].getInterazioni().size() << "\n";
    }
}

// Metodo per modificare i dati di un cliente esistente
void CRM::modificaCliente() {
    if (mostraErrore(clienti.empty(), "Nessun cliente presente nel sistema.")) return; // Controllo presenza clienti
    
    cout << "\n=== MODIFICA CLIENTE ===\n";
    string codiceFiscale = ottieniInputSicuro("Inserisci il codice fiscale del cliente da modificare: ");
    
    int indice = controllaEsistenzaCliente(clienti, codiceFiscale); // Ricerca cliente
    if (indice == -1) return;
    
    cout << "Modifica i dati del cliente (lascia vuoto per non modificare):\n";
    
    string nuovoNome = ottieniInputSicuro("Nuovo nome: ");
    if (!nuovoNome.empty()) clienti[indice].setNome(nuovoNome);
    
    string nuovoCognome = ottieniInputSicuro("Nuovo cognome: ");
    if (!nuovoCognome.empty()) clienti[indice].setCognome(nuovoCognome);
    
    string nuovaEmail = ottieniInputSicuro("Nuova email: ");
    if (!nuovaEmail.empty()) clienti[indice].setEmail(nuovaEmail);
    
    string nuovoTelefono = ottieniInputSicuro("Nuovo telefono: ");
    if (!nuovoTelefono.empty()) clienti[indice].setTelefono(nuovoTelefono);
    
    string nuovoIndirizzo = ottieniInputSicuro("Nuovo indirizzo: ");
    if (!nuovoIndirizzo.empty()) clienti[indice].setIndirizzo(nuovoIndirizzo);
    
    string nuovaDataNascita = ottieniInputSicuro("Nuova data di nascita: ");
    if (!nuovaDataNascita.empty()) clienti[indice].setDataNascita(nuovaDataNascita);
    
    cout << "Cliente modificato con successo!\n";
}

// Metodo per eliminare un cliente dal sistema
void CRM::eliminaCliente() {
    if (mostraErrore(clienti.empty(), "Nessun cliente presente nel sistema.")) return; // Controllo presenza clienti
    
    cout << "\n=== ELIMINA CLIENTE ===\n";
    string codiceFiscale = ottieniInputSicuro("Inserisci il codice fiscale del cliente da eliminare: ");
    
    int indice = controllaEsistenzaCliente(clienti, codiceFiscale); // Ricerca cliente
    if (indice == -1) return;
    
    cout << "Stai per eliminare il cliente: " << clienti[indice].getNomeCompleto() << "\n";
    string conferma = ottieniInputSicuro("Sei sicuro? (si/no): ");
    
    if (conferma == "si" || conferma == "SI" || conferma == "Si") {
        clienti.erase(clienti.begin() + indice); // Rimozione cliente
        cout << "Cliente eliminato con successo!\n";
    } else {
        cout << "Operazione annullata.\n";
    }
}

// Metodo per cercare clienti per nome, cognome, email o telefono
void CRM::cercaCliente() {
    if (mostraErrore(clienti.empty(), "Nessun cliente presente nel sistema.")) return; // Controllo presenza clienti
    
    cout << "\n=== CERCA CLIENTE ===\n";
    string ricerca = ottieniInputSicuro("Inserisci il termine di ricerca: ");

    bool trovato = false; // Flag per verificare se sono stati trovati clienti
    // Scorre tutti i clienti e verifica se contengono il termine di ricerca
    for (size_t i = 0; i < clienti.size(); i++) {
        if (clienti[i].contieneStringa(ricerca)) {
            if (!trovato) {
                cout << "\n=== RISULTATI RICERCA ===\n";
                trovato = true;
            }
            cout << "\nCliente #" << (i + 1) << ":\n";
            clienti[i].stampaDettagli();
        }
    }
    
    if (!trovato) {
        cout << "Nessun cliente trovato con il termine '" << ricerca << "'.\n";
    }
}

// Metodo per aggiungere un'interazione a un cliente specifico
void CRM::aggiungiInterazione() {
    if (mostraErrore(clienti.empty(), "Nessun cliente presente nel sistema.")) return; // Controllo presenza clienti
    
    cout << "\n=== AGGIUNGI INTERAZIONE ===\n";
    string codiceFiscale = ottieniInputSicuro("Inserisci il codice fiscale del cliente: ");
    
    int indice = controllaEsistenzaCliente(clienti, codiceFiscale); // Ricerca cliente
    if (indice == -1) return;
    
    cout << "Aggiungendo interazione per: " << clienti[indice].getNomeCompleto() << "\n";
    
    string data = ottieniInputSicuro("Data (DD/MM/YYYY): ");
    if (!validaData(data)) {
        cout << "Formato data non valido!\n";
        return;
    }
    
    string ora = ottieniInputSicuro("Ora (HH:MM): ");
    if (!validaOra(ora)) {
        cout << "Formato ora non valido!\n";
        return;
    }
    
    TipoInterazione tipo = scegliTipoInterazione(); // Scelta del tipo tramite menu
    string descrizione = ottieniInputSicuro("Descrizione: ");
    string agente = ottieniInputSicuro("Agente: ");
    string risultato = ottieniInputSicuro("Risultato: ");
    
    Interazione nuovaInterazione(data, ora, tipo, descrizione, agente, risultato); // Crea la nuova interazione
    clienti[indice].aggiungiInterazione(nuovaInterazione); // Aggiunge l'interazione al cliente
    
    cout << "Interazione aggiunta con successo!\n";
}

// Metodo per visualizzare tutte le interazioni di un cliente specifico
void CRM::visualizzaInterazioniCliente() {
    if (mostraErrore(clienti.empty(), "Nessun cliente presente nel sistema.")) return; // Controllo presenza clienti
    
    cout << "\n=== VISUALIZZA INTERAZIONI CLIENTE ===\n";
    string codiceFiscale = ottieniInputSicuro("Inserisci il codice fiscale del cliente: ");
    
    int indice = controllaEsistenzaCliente(clienti, codiceFiscale); // Ricerca cliente
    if (indice == -1) return;
    
    clienti[indice].visualizzaInterazioni(); // Visualizza tutte le interazioni del cliente
}

// Metodo per cercare interazioni in tutti i clienti
void CRM::cercaInterazioni() {
    if (mostraErrore(clienti.empty(), "Nessun cliente presente nel sistema.")) return; // Controllo presenza clienti

    cout << "\n=== CERCA INTERAZIONI ===\n";
    string ricerca = ottieniInputSicuro("Inserisci il termine di ricerca: ");

    bool trovato = false; // Flag per verificare se sono state trovate interazioni
    // Scorre tutti i clienti e le loro interazioni
    for (size_t i = 0; i < clienti.size(); i++) {
        std::vector<Interazione> interazioni = clienti[i].getInterazioni(); // Ottiene tutte le interazioni del cliente
        for (size_t j = 0; j < interazioni.size(); j++) {
            if (interazioni[j].contieneStringa(ricerca)) {
                if (!trovato) {
                    cout << "\n=== RISULTATI RICERCA INTERAZIONI ===\n";
                    trovato = true;
                }
                cout << "\nCliente: " << clienti[i].getNomeCompleto() << "\n";
                cout << "Interazione #" << (j + 1) << ":\n";
                interazioni[j].stampaDettagli(); // Stampa dettagli interazione trovata
            }
        }
    }

    if (!trovato) {
        cout << "Nessuna interazione trovata con il termine '" << ricerca << "'.\n";
    }
}

// Metodo per salvare tutti i dati su file
bool CRM::salvaDati() {
    std::ofstream fileClienti(nomeFileClienti);
    std::ofstream fileInterazioni(nomeFileInterazioni);
    if (!fileClienti || !fileInterazioni) {
        std::cout << "Errore nell'apertura dei file di salvataggio!" << std::endl;
        return false;
    }
    for (size_t i = 0; i < clienti.size(); i++) {
        Cliente& cliente = clienti[i];
        fileClienti << cliente.getNome() << "|" << cliente.getCognome() << "|" << cliente.getEmail() << "|" << cliente.getTelefono() << "|" << cliente.getIndirizzo() << "|" << cliente.getCodiceFiscale() << "|" << cliente.getDataNascita() << "\n";
        std::vector<Interazione> interazioni = cliente.getInterazioni();
        for (size_t j = 0; j < interazioni.size(); j++) {
            Interazione& interazione = interazioni[j];
            fileInterazioni << cliente.getCodiceFiscale() << "|" << interazione.getData() << "|" << interazione.getOra() << "|" << interazione.getTipoStringa() << "|" << interazione.getDescrizione() << "|" << interazione.getAgente() << "|" << interazione.getRisultato() << "\n";
        }
    }
    return true;
}

// Metodo per caricare i dati dai file
bool CRM::caricaDati() {
    std::ifstream fileClienti(nomeFileClienti);         // Stream per il file clienti
    std::ifstream fileInterazioni(nomeFileInterazioni); // Stream per il file interazioni
    if (!fileClienti || !fileInterazioni) {
        return false;
    }

    clienti.clear(); // Pulisce il vettore prima del caricamento

    string linea; // Variabile per leggere le linee dai file
    while (getline(fileClienti, linea)) {
        if (linea.empty()) continue;
        std::vector<std::string> dati;
        std::string campo;
        for (size_t i = 0; i < linea.size(); i++) {
            if (linea[i] == '|') {
                dati.push_back(campo);
                campo = "";
            } else {
                campo += linea[i];
            }
        }
        dati.push_back(campo);
        if (dati.size() == 7) {
            Cliente cliente(dati[0], dati[1], dati[2], dati[3], dati[4], dati[5], dati[6]); // Ricostruisce il cliente
            clienti.push_back(cliente);
        }
    }

    while (getline(fileInterazioni, linea)) {
        if (linea.empty()) continue;
        std::vector<std::string> dati;
        std::string campo;
        for (size_t i = 0; i < linea.size(); i++) {
            if (linea[i] == '|') {
                dati.push_back(campo);
                campo = "";
            } else {
                campo += linea[i];
            }
        }
        dati.push_back(campo);
        if (dati.size() == 7) {
            std::string codiceFiscale = dati[0];
            TipoInterazione tipo = ALTRO;
            if (dati[3] == "Appuntamento") tipo = APPUNTAMENTO;
            else if (dati[3] == "Contratto") tipo = CONTRATTO;
            else if (dati[3] == "Telefonata") tipo = TELEFONATA;
            else if (dati[3] == "Email") tipo = EMAIL;
            else if (dati[3] == "Altro") tipo = ALTRO;
            Interazione interazione(dati[1], dati[2], tipo, dati[4], dati[5], dati[6]); // Ricostruisce interazione
            for (size_t i = 0; i < clienti.size(); i++) {
                if (clienti[i].getCodiceFiscale() == codiceFiscale) {
                    clienti[i].aggiungiInterazione(interazione);
                    break;
                }
            }
        }
    }
    return true;
}

// ==================== METODI DI UTILITÀ PRIVATI ====================

// Trova l'indice di un cliente tramite codice fiscale
int CRM::trovaCliente(string codiceFiscale) {
    for (size_t i = 0; i < clienti.size(); i++) {
        if (clienti[i].getCodiceFiscale() == codiceFiscale) {
            return (int)i;
        }
    }
    return -1;
}

// Trova l'indice di un cliente tramite nome e cognome
int CRM::trovaCliente(string nome, string cognome) {
    for (size_t i = 0; i < clienti.size(); i++) {
        if (clienti[i].getNome() == nome && clienti[i].getCognome() == cognome) {
            return (int)i;
        }
    }
    return -1;
}

// Metodo per stampare il menu per scegliere il tipo di interazione
void CRM::stampaMenuTipiInterazione() {
    cout << "Scegli il tipo di interazione:\n";
    cout << "1. Appuntamento\n";
    cout << "2. Contratto\n";
    cout << "3. Telefonata\n";
    cout << "4. Email\n";
    cout << "5. Altro\n";
    cout << "Scelta: ";
}

// Metodo per gestire la scelta del tipo di interazione
TipoInterazione CRM::scegliTipoInterazione() {
    int scelta;
    do {
        stampaMenuTipiInterazione(); // Mostra il menu
        // Ottiene l'input dell'utente
        cout << "Inserisci il numero corrispondente al tipo di interazione: ";
        cin >> scelta;
        if (!(cin >> scelta)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Input non valido. Riprova.\n";
            continue;
        }
        
        switch (scelta) {
            case 1: return APPUNTAMENTO;
            case 2: return CONTRATTO;
            case 3: return TELEFONATA;
            case 4: return EMAIL;
            case 5: return ALTRO;
            default:
                cout << "Scelta non valida!\n";
        }
    } while (true);
}

// Metodo per validare il formato della data (DD/MM/YYYY)
bool CRM::validaData(string data) {
    if (data.length() != 10) return false;
    if (data[2] != '/' || data[5] != '/') return false;
    
    // Controlli base sui numeri
    for (int i = 0; i < 10; i++) { // Scorre i caratteri della data
        if (i != 2 && i != 5 && !isdigit(data[i])) return false; // Controlla che siano tutti numeri tranne i separatori
    }
    
    return true;
}

// Metodo per validare il formato dell'ora (HH:MM)
bool CRM::validaOra(string ora) {
    if (ora.length() != 5) return false; 
    if (ora[2] != ':') return false;
    
    // Controlli base sui numeri
    for (int i = 0; i < 5; i++) { // Scorre i caratteri dell'ora
        if (i != 2 && !isdigit(ora[i])) return false; // Controlla che siano tutti numeri tranne il separatore
    }
    
    return true;
}

// Metodo per ottenere input sicuro dall'utente (IMPORTANTE)
string CRM::ottieniInputSicuro(string messaggio) {
    string input;
    cout << messaggio;
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Ignora eventuali caratteri residui nel buffer
    getline(cin, input);                                 // Legge l'input completo dell'utente
    return input;
}

/*
 * FUNZIONAMENTO:
 * Questo file implementa tutti i metodi della classe CRM:
 * - Gestione completa dei clienti (CRUD operations: Create, Read, Update, Delete)
 * - Gestione delle interazioni associate ai clienti
 * - Salvataggio e caricamento dati su file txt
 * - Ricerca in clienti e interazioni
 * - Validazione input utente e gestione errori centralizzata
 * - Interfaccia utente intuitiva con menu e conferme
 * - Parsing sicuro dei file di dati con controlli di integrità
 */