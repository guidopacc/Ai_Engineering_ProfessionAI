/*
 * main.cpp - File principale
 * Gestisce il menu principale e coordina tutte le operazioni del sistema
 * Punto di ingresso dell'applicazione
 */

#include "gestione_errori.h"
#include "crm.h"

#include <iostream>
#include <limits>
#include <sys/stat.h>
#include <unistd.h>

using namespace std;

// Menu principale
void mostraMenuPrincipale() {
    cout << "\n=== MENU PRINCIPALE ===\n";
    cout << "--------------------------------\n";
    cout << "Seleziona un'opzione:\n";
    cout << "--------------------------------\n";
    cout << "1. Aggiungi nuovo cliente\n";
    cout << "2. Visualizza tutti i clienti\n";
    cout << "3. Modifica cliente\n";
    cout << "4. Elimina cliente\n";
    cout << "5. Cerca cliente\n";
    cout << "6. Gestisci interazioni\n";
    cout << "7. Salva dati\n";
    cout << "8. Carica dati\n";
    cout << "0. Esci\n";
    cout << "Scelta: ";
}

// Menu delle interazioni
void mostraMenuInterazioni() {
    cout << "\n=== GESTIONE INTERAZIONI ===\n";
    cout << "1. Aggiungi interazione\n";
    cout << "2. Visualizza interazioni cliente\n";
    cout << "3. Cerca interazioni\n";
    cout << "0. Torna al menu principale\n";
    cout << "Scelta: ";
}

int main() {
    // Fallback: crea "data" e "build" se mancanti
    // Utile se l'eseguibile viene lanciato senza passare dal Makefile (che le crea automaticamente)
    // NOTA: 'const' garantisce che le stringhe "data" e "build" NON vengano modificate dal programma.
    const char* dirs[] = {"data", "build"};
    for (const char* dir : dirs) {
        struct stat st = {0};
        if (stat(dir, &st) == -1)
            mkdir(dir, 0755);
    }

    CRM crm;
    int scelta = -1;

    cout << "Benvenuto in InsuraPro Solutions CRM!\n";

    // Caricamento dati
    if (crm.caricaDati())
        cout << "Dati caricati con successo!\n";
    else
        cout << "Nessun dato esistente trovato. Inizia ad aggiungere clienti.\n";

    // Loop principale
    while (scelta != 0) {
        mostraMenuPrincipale();
        if (!(cin >> scelta)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            stampaErroreUtente("Input non valido. Riprova.");
            continue;
        }

        switch (scelta) {
            case 1: crm.aggiungiCliente(); break;
            case 2: crm.visualizzaClienti(); break;
            case 3: crm.modificaCliente(); break;
            case 4: crm.eliminaCliente(); break;
            case 5: crm.cercaCliente(); break;
            case 6: {
                int sceltaInterazioni = -1;
                while (sceltaInterazioni != 0) {
                    mostraMenuInterazioni();
                    if (!(cin >> sceltaInterazioni)) {
                        cin.clear();
                        cin.ignore(numeric_limits<streamsize>::max(), '\n');
                        stampaErroreUtente("Input non valido. Riprova.");
                        continue;
                    }
                    switch (sceltaInterazioni) {
                        case 1: crm.aggiungiInterazione(); break;
                        case 2: crm.visualizzaInterazioniCliente(); break;
                        case 3: crm.cercaInterazioni(); break;
                        case 0: break;
                        default: stampaErroreUtente("Scelta non valida!");
                    }
                }
                break;
            }
            case 7:
                if (crm.salvaDati())
                    cout << "Dati salvati con successo!\n";
                else
                    stampaErroreSistema("Errore nel salvataggio dei dati.");
                break;
            case 8:
                if (crm.caricaDati())
                    cout << "Dati caricati con successo!\n";
                else
                    stampaErroreSistema("Errore nel caricamento dei dati.");
                break;
            case 0:
                cout << "Salvataggio automatico dei dati...\n";
                crm.salvaDati();
                cout << "Grazie per aver usato InsuraPro Solutions CRM!\n";
                break;
            default:
                stampaErroreUtente("Scelta non valida!");
        }
    }

    return 0;
}