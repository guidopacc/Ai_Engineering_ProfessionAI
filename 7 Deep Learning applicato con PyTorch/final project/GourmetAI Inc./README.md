# Ottimizzazione delle prestazioni di una rete neurale per il settore food

Progetto di classificazione di immagini nel settore food utilizzando tecniche di deep learning con PyTorch.

## Descrizione

Il progetto implementa un sistema completo di classificazione di immagini di cibo utilizzando tecniche avanzate di deep learning. Il modello utilizza transfer learning con ResNet18 pre-addestrato su ImageNet, applicando data augmentation, fine tuning e tecniche di regularizzazione per ottimizzare le performance.

## Dataset

Il dataset utilizzato è il **Food Classification Dataset**, disponibile al seguente link:
- https://proai-datasets.s3.eu-west-3.amazonaws.com/dataset_food_classification.zip

Il dataset viene scaricato e estratto automaticamente all'interno del notebook.

## Struttura del Codice

Il notebook è organizzato nelle seguenti sezioni:

1. **Environment Setup**: Import delle librerie, configurazione device (CPU/GPU) e download del dataset
2. **Data Exploration**: Analisi e visualizzazione del dataset, conteggio immagini per classe
3. **Data Augmentation**: Implementazione di tecniche di augmentation per il training (random crop, flip, rotation, color jitter)
4. **Dataset & DataLoader**: Creazione di dataset personalizzati, suddivisione train/val/test (70%/15%/15%) e DataLoader
5. **Transfer Learning**: Caricamento e configurazione di ResNet18 pre-addestrato su ImageNet, congelamento del backbone
6. **Baseline Training**: Training iniziale con backbone congelato, solo il classificatore viene allenato
7. **Fine-tuning & Regularization**: Ottimizzazione del modello con fine tuning (scongelamento layer), dropout e weight decay
8. **Model Evaluation**: Valutazione finale del modello sul test set con matrice di confusione e visualizzazioni
9. **Conclusions & Results Summary**: Analisi dei risultati ottenuti e confronto baseline vs fine-tuned

## Come Eseguire

1. Aprire il notebook `food_classification.ipynb` su Google Colab o in un ambiente locale con PyTorch installato
2. Eseguire tutte le celle in sequenza dall'inizio alla fine
3. Il dataset verrà scaricato e estratto automaticamente nella sezione "Environment Setup"
4. **⚠️ IMPORTANTE - Tempi di Training**: Il training completo con 20 epoche per baseline e 20 epoche per fine-tuning è **molto lungo** (può richiedere diverse ore su CPU). Per test rapidi e verifiche del codice, si consiglia di modificare i valori `num_epochs` e `num_epochs_ft` nelle celle 18 e 24, riducendoli a **5-8 epoche** ciascuno. Il notebook è configurato con early stopping (patience=5), quindi il training si fermerà automaticamente se non migliora.
5. Per il training completo, è fortemente consigliato l'uso di GPU su Google Colab (Runtime → Change runtime type → GPU) per tempi molto più rapidi
6. Il notebook è compatibile con Windows, Mac e Linux (gestisce automaticamente `num_workers` per i DataLoader)

## Tecniche Utilizzate

- **Data Augmentation**: RandomResizedCrop, RandomHorizontalFlip (p=0.5), RandomRotation (15°), ColorJitter (brightness, contrast, saturation, hue)
- **Transfer Learning**: ResNet18 pre-addestrato su ImageNet con weights `IMAGENET1K_V1`
- **Fine Tuning**: Scongelamento selettivo degli ultimi 2 layer convolutivi (layer4 e layer3) del backbone
- **Regularizzazione**: 
  - Dropout (0.5) nel classifier head
  - Weight Decay (L2 regularization, 1e-4) nell'optimizer
- **Early Stopping**: Implementazione manuale con patience=5 epoche per prevenire overfitting
- **Validazione**: Suddivisione del dataset in train (70%), validation (15%), test (15%) con `random_split`
- **Optimizer**: Adam con learning rate 0.001 (baseline) e 0.0001 (fine-tuning)
- **Loss Function**: CrossEntropyLoss per classificazione multi-classe

## Requisiti

- Python 3.7+
- PyTorch (con supporto CUDA opzionale per GPU)
- torchvision (con modelli pre-addestrati)
- PIL (Pillow) per il caricamento delle immagini
- matplotlib per visualizzazioni
- numpy per operazioni numeriche
- scikit-learn per metriche (confusion matrix)
- seaborn per visualizzazioni avanzate

Tutte le librerie sono disponibili di default su Google Colab. Per installazione locale:
```bash
pip install torch torchvision pillow matplotlib numpy scikit-learn seaborn
```

## Caratteristiche del Modello

- **Architettura**: ResNet18
- **Numero di classi**: 14 classi di cibo
- **Input size**: 224x224 pixel (dopo resize e crop)
- **Batch size**: 32
- **Epoche**: Fino a 20 per baseline e fine-tuning (con early stopping). **Nota**: Il training completo con 20 epoche è molto lungo; per test rapidi si consiglia di ridurre a 5-8 epoche modificando `num_epochs` e `num_epochs_ft` nel notebook
- **Parametri allenabili (baseline)**: ~7,182 (0.06% del totale)
- **Parametri allenabili (fine-tuning)**: Aumentati dopo scongelamento layer

## Autore

**Guido Pacciani**

## Corso di Riferimento

"Deep Learning applicato con PyTorch" - ProfessionAI

## Licenza

Uso esclusivo a scopo formativo.

