# GourmetAI Inc. — Classificazione di immagini di cibo
## Transfer learning con ResNet18 e PyTorch

---

## Descrizione

GourmetAI Inc. è un progetto di classificazione di immagini nel settore food, implementato con PyTorch. Il modello riconosce 14 categorie di cibo a partire da immagini, sfruttando il transfer learning da un modello pre-addestrato su ImageNet.

Il processo è diviso in due fasi:
1. **Baseline**: si allena solo il classificatore finale, con il backbone ResNet18 congelato
2. **Fine-tuning**: si scongelano gli ultimi layer convoluzionali e si riallena con learning rate ridotto

---

## Autore e contesto

**Autore:** Guido Pacciani  
Sviluppato come progetto finale del modulo *"Deep Learning applicato con PyTorch"* del **Master Professionale in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

---

## Struttura del progetto

```
GourmetAI Inc./
├── food_classification.ipynb    # Notebook principale
└── README.md
```

### Sezioni del notebook

1. **Environment Setup** — import librerie, configurazione device (CPU/GPU), download dataset
2. **Data Exploration** — analisi e visualizzazione dataset, conteggio immagini per classe
3. **Data Augmentation** — trasformazioni per il training (crop, flip, rotazione, color jitter)
4. **Dataset & DataLoader** — suddivisione train/val/test (70%/15%/15%), DataLoader
5. **Transfer Learning** — caricamento ResNet18, congelamento backbone
6. **Baseline Training** — training del solo classificatore
7. **Fine-tuning & Regularization** — scongelamento layer, dropout, weight decay
8. **Model Evaluation** — valutazione sul test set, matrice di confusione
9. **Conclusions** — confronto baseline vs fine-tuned

---

## Dataset

**Food Classification Dataset** — scaricato e estratto automaticamente all'interno del notebook:
```
https://proai-datasets.s3.eu-west-3.amazonaws.com/dataset_food_classification.zip
```
14 classi di cibo, suddivise in train (70%), validation (15%), test (15%).

---

## Tecnologie utilizzate

- **PyTorch + torchvision** — framework per deep learning e modelli pre-addestrati
- **PIL (Pillow)** — caricamento immagini
- **matplotlib** — visualizzazioni
- **NumPy** — operazioni numeriche
- **scikit-learn** — metriche (confusion matrix)
- **seaborn** — visualizzazioni avanzate

Tutte disponibili di default su Google Colab. Per installazione locale:
```bash
pip install torch torchvision pillow matplotlib numpy scikit-learn seaborn
```

---

## Come eseguire

### Su Google Colab (consigliato)

1. Apri il notebook `food_classification.ipynb` su [Google Colab](https://colab.research.google.com/)
2. Imposta il runtime su GPU: Runtime → Change runtime type → GPU
3. Esegui tutte le celle in sequenza
4. Il dataset viene scaricato automaticamente

**Nota sui tempi di training:** il training completo (20 epoche baseline + 20 fine-tuning) richiede diverse ore su CPU. Per verifiche rapide, riduci `num_epochs` e `num_epochs_ft` a 5–8. Il notebook usa early stopping (patience=5), quindi si ferma prima se la validation loss smette di migliorare.

### In locale

```bash
pip install torch torchvision pillow matplotlib numpy scikit-learn seaborn jupyter
jupyter notebook food_classification.ipynb
```

---

## Risultati attesi

Il notebook produce:
- Grafici di training (loss e accuracy per ogni epoca)
- Matrice di confusione sul test set
- Confronto baseline vs fine-tuned sulle metriche principali

---

## Approfondimento tecnico

### Transfer learning con ResNet18

ResNet18 è una rete convoluzionale residuale con 18 layer, pre-addestrata su ImageNet (1.2M immagini, 1000 classi). L'idea del transfer learning è che le feature apprese su ImageNet — bordi, texture, pattern — siano generalizzabili ad altri domini visivi, incluso il food.

La strategia a due fasi:
1. **Fase 1 (baseline)**: il backbone è congelato (`requires_grad=False`). Si allena solo il layer lineare finale, adattandolo alle 14 classi del dataset. Richiede pochi parametri e converge velocemente.
2. **Fase 2 (fine-tuning)**: si scongelano `layer4` e `layer3` del backbone. Si usa un learning rate più basso (0.0001 vs 0.001) per aggiornare i pesi pre-addestrati senza distruggerli.

### Data Augmentation

Le trasformazioni applicate al training set:
- `RandomResizedCrop(224)`: crop casuale e ridimensionamento
- `RandomHorizontalFlip(p=0.5)`: flip orizzontale
- `RandomRotation(15°)`: rotazione casuale
- `ColorJitter`: variazione di luminosità, contrasto, saturazione e tonalità

Sul validation/test set si usa solo `Resize + CenterCrop`, senza augmentation, per una valutazione pulita.

### Regolarizzazione

- **Dropout (0.5)** nel classificatore: disattiva casualmente neuroni durante il training per ridurre l'overfitting
- **Weight Decay (1e-4)**: regolarizzazione L2 nell'optimizer Adam, penalizza pesi grandi
- **Early Stopping (patience=5)**: interrompe il training se la validation loss non migliora per 5 epoche consecutive

### Parametri del modello

- **Architettura**: ResNet18 pre-addestrata (`IMAGENET1K_V1`)
- **Input size**: 224×224 pixel
- **Batch size**: 32
- **Parametri allenabili (baseline)**: ~7.182 (0.06% del totale)
- **Optimizer baseline**: Adam, lr=0.001
- **Optimizer fine-tuning**: Adam, lr=0.0001
- **Loss**: CrossEntropyLoss

---

## Riferimenti

- [PyTorch — Transfer Learning tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [torchvision — ResNet](https://pytorch.org/vision/stable/models/resnet.html)

---

## Licenza

Rilasciato con licenza **MIT** — libero per uso personale, studio o sviluppo. Clona e modifica liberamente.
