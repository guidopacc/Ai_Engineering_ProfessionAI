# Classificazione Binaria di Fiori – GreenTech Solutions

Sistema di Computer Vision per la classificazione binaria di immagini di fiori utilizzando Transfer Learning con PyTorch.

**Autore:** Guido Pacciani  
**Contesto:** Progetto finale del corso *"Computer Vision"* – Master in AI Engineering, ProfessionAI

---

## Descrizione

Il progetto implementa un classificatore binario per distinguere automaticamente tra due tipi di fiori:

- **daisy** (margherita)
- **dandelion** (dente di leone)

Il sistema è basato su **ResNet18** pre-addestrato su ImageNet, adattato al task tramite Transfer Learning a due fasi, con Data Augmentation, Early Stopping, checkpointing del modello migliore ed explainability tramite **GradCAM**.

---

## Struttura del progetto

```
final project/
├── GreenTech Solutions.ipynb   # Notebook principale con tutto il codice
└── README.md                   # Questo file
```

### Contenuto del notebook

Il notebook è organizzato nelle seguenti sezioni:

| Sezione | Descrizione |
|---------|-------------|
| 1. Setup Ambiente | Import librerie, configurazione device (CPU/GPU), seed per riproducibilità |
| 2. Download e Estrazione Dataset | Download automatico del dataset e verifica della struttura |
| 3. DataLoader con Data Augmentation | Trasformazioni per training (augmentation) e validation/test |
| 4. Modello ResNet18 con Transfer Learning | Caricamento backbone e adattamento per classificazione binaria |
| 5. Training Industrializzato | Training con checkpointing, early stopping e metriche |
| 6. Visualizzazione Training | Grafici di loss, accuracy e F1-score per train e validation |
| 7. Valutazione su Test Set | Metriche complete (accuracy, F1, precision, recall) e matrice di confusione |
| 8. Inference Demo | Esempi visivi di predizione su immagini del test set |
| 9. Explainability: GradCAM | Heatmap che mostrano le regioni dell'immagine più rilevanti per la predizione |

---

## Dataset

Il dataset contiene immagini di due tipi di fiori:

- **Classi**: `daisy` (margherita) e `dandelion` (dente di leone)
- **Suddivisione**: train / validation / test

Il dataset viene scaricato ed estratto automaticamente all'interno del notebook.

---

## Tecnologie utilizzate

- **PyTorch** e **torchvision** – framework di Deep Learning e gestione dataset
- **timm** – libreria per modelli pre-addestrati avanzati
- **ResNet18** – backbone pre-addestrato su ImageNet
- **scikit-learn** – metriche di valutazione e matrice di confusione
- **matplotlib** – visualizzazione grafici e immagini

---

## Tecniche applicate

### Transfer Learning a due fasi
1. **Fase 1 – Feature Extraction**: il backbone ResNet18 viene congelato, si allena solo il classificatore finale
2. **Fase 2 – Fine-tuning**: si scongelano gli ultimi layer del backbone con un learning rate ridotto

### Data Augmentation (training)
- `RandomResizedCrop`
- `RandomHorizontalFlip`
- `RandomRotation`
- `ColorJitter` (luminosità, contrasto, saturazione)

### Training industrializzato
- **Checkpointing**: salva il modello migliore e gli ultimi checkpoint
- **Early Stopping**: interrompe il training se la metrica non migliora per `patience` epoche
- **Metrica principale**: Macro F1-Score (bilanciato tra le classi)

### Explainability – GradCAM
GradCAM (Gradient-weighted Class Activation Mapping) genera heatmap che evidenziano le regioni dell'immagine più rilevanti per la predizione del modello, combinando:
- Le attivazioni del layer convoluzionale finale
- I gradienti rispetto alla classe predetta

---

## Come eseguire il progetto

### Opzione 1: Google Colab (consigliato)

1. Apri [Google Colab](https://colab.research.google.com/)
2. Carica il notebook `GreenTech Solutions.ipynb`
3. Abilita la GPU: *Runtime → Change runtime type → GPU*
4. Esegui tutte le celle in sequenza (*Runtime → Run all*)
5. Il dataset verrà scaricato e il modello addestrato automaticamente

### Opzione 2: Ambiente locale

#### Requisiti
- Python 3.8+
- GPU (opzionale, ma consigliata per velocizzare il training)

#### Installazione

```bash
pip install torch torchvision timm numpy matplotlib scikit-learn seaborn
```

#### Esecuzione

```bash
jupyter notebook "GreenTech Solutions.ipynb"
```

Esegui le celle in sequenza dall'inizio alla fine.

---

## Risultati attesi

Il modello raggiunge performance tipicamente nell'ordine di:

- **Accuracy**: ~93–97%
- **Macro F1-Score**: ~93–97%
- **Precision / Recall**: ~93–97% per ciascuna classe

*I risultati possono variare leggermente in base all'hardware e al seed random.*

---

## Autore e Licenza

**Autore:** Guido Pacciani  
Questo progetto è stato sviluppato per scopi didattici nell'ambito del Master in AI Engineering erogato da **ProfessionAI**.

**Data di realizzazione:** 2025
