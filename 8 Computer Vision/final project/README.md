# GreenTech Solutions – Classificazione Binaria di Fiori

**Autore:** Guido Pacciani  
**Azienda:** GreenTech Solutions  
**Corso di riferimento:** Computer Vision – Master in AI Engineering, ProfessionAI

---

## Descrizione

Questo progetto implementa un sistema di **classificazione binaria di immagini** per distinguere tra due tipi di fiori:
- **daisy** (margherita)
- **dandelion** (dente di leone)

Il sistema utilizza **Transfer Learning** con ResNet18 pre-addestrato su ImageNet, con una strategia di training a due fasi e tecniche di **Data Augmentation** per migliorare la generalizzazione del modello. Include inoltre **GradCAM** per l'explainability del modello.

---

## Obiettivi

1. Implementare un sistema di classificazione binaria di immagini con Transfer Learning
2. Applicare Data Augmentation per aumentare la varietà dei dati di training
3. Utilizzare un training industrializzato con checkpointing ed early stopping
4. Valutare il modello con metriche complete (Accuracy, F1-Score macro, Precision, Recall)
5. Visualizzare le predizioni e la heatmap GradCAM per l'interpretabilità del modello

---

## Dataset

- **URL:** [https://proai-datasets.s3.eu-west-3.amazonaws.com/progetto-finale-flowes.tar.gz](https://proai-datasets.s3.eu-west-3.amazonaws.com/progetto-finale-flowes.tar.gz)
- **Classi:** `daisy` (margherita), `dandelion` (dente di leone)
- **Suddivisione:** train / validation / test

Il dataset viene scaricato ed estratto automaticamente dal notebook.

---

## Struttura del progetto

```
final project/
├── GreenTech Solutions.ipynb   # Notebook principale
└── README.md                   # Questo file
```

### Contenuto del notebook

Il notebook è suddiviso nelle seguenti sezioni:

1. **Setup Ambiente** – Installazione dipendenze e configurazione del device (CPU/GPU)
2. **Download e Estrazione Dataset** – Download automatico e ispezione della struttura
3. **DataLoader con Data Augmentation** – Trasformazioni per training (augmentation aggressiva) e validation/test
4. **Modello: ResNet18 con Transfer Learning** – Caricamento ResNet18, congelamento backbone e adattamento al task binario
5. **Training Industrializzato** – Checkpointing, Early Stopping e tracciamento di loss/accuracy/F1-score
6. **Visualizzazione Training** – Grafici delle metriche durante il training
7. **Valutazione su Test Set** – Metriche complete con il best model
8. **Inference Demo** – Esempi di predizione su immagini del test set
9. **Explainability: GradCAM** – Heatmap per comprendere le regioni dell'immagine rilevanti per la predizione

---

## Tecniche utilizzate

### Transfer Learning (2 fasi)
1. **Fase 1 – Backbone congelato:** si allena solo il classificatore finale, con learning rate più alto (`3e-4`)
2. **Fase 2 – Fine-tuning:** si scongela l'intera rete e si riallena con learning rate più basso

### Data Augmentation
- `RandomResizedCrop`: simula zoom e crop casuali
- `RandomHorizontalFlip`: simmetria orizzontale
- `ColorJitter`: variazione di luminosità, contrasto e saturazione
- `RandomRotation`: rotazioni casuali

### Training industrializzato
- **Checkpointing:** salva il best model e gli ultimi 5 checkpoint con rotazione
- **Early Stopping:** interrompe il training se la metrica di validazione non migliora per `patience` epoch

### Explainability
- **GradCAM:** combina attivazioni e gradienti dell'ultimo layer convoluzionale per produrre una heatmap sulle regioni più rilevanti per la predizione

---

## Modello

| Parametro         | Valore                        |
|-------------------|-------------------------------|
| Architettura      | ResNet18                      |
| Pre-training      | ImageNet                      |
| Numero di classi  | 2 (daisy, dandelion)          |
| Input size        | 224×224 px                    |
| Batch size        | 32                            |
| Optimizer         | AdamW                         |
| Loss function     | CrossEntropyLoss              |
| Metrica principale| Macro F1-Score                |

---

## Come eseguire il progetto

### Opzione 1: Google Colab (consigliato)

1. Apri [Google Colab](https://colab.research.google.com/)
2. Carica il notebook `GreenTech Solutions.ipynb`
3. Abilita la GPU: `Runtime → Change runtime type → GPU`
4. Esegui tutte le celle in sequenza (`Runtime → Run all`)

### Opzione 2: Ambiente locale

#### Requisiti

- Python 3.8+
- PyTorch con supporto CUDA (opzionale)
- GPU consigliata per tempi di training ragionevoli

#### Installazione dipendenze

```bash
pip install torch torchvision timm numpy matplotlib scikit-learn
```

#### Esecuzione

1. Apri il notebook con Jupyter:
   ```bash
   jupyter notebook "GreenTech Solutions.ipynb"
   ```
2. Esegui tutte le celle in sequenza

---

## Requisiti

- Python 3.8+
- `torch` e `torchvision`
- `timm` (per il caricamento di ResNet18)
- `numpy`
- `matplotlib`
- `scikit-learn` (per le metriche)

Su Google Colab tutte le librerie (tranne `timm`) sono disponibili di default. Il notebook installa automaticamente `timm` se non presente.

---

## Licenza

Questo progetto è stato sviluppato esclusivamente per scopi didattici nell'ambito del **Master in AI Engineering** erogato da **ProfessionAI**.

---

**Sviluppato con ❤️ per il Master in AI Engineering – ProfessionAI**
