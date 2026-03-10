# VisionTech Solutions
## Riconoscimento di animali per sistemi di guida autonoma

---

## Descrizione

VisionTech Solutions è un progetto di deep learning che implementa un classificatore binario per distinguere **animali** da **veicoli** nelle immagini. Il contesto applicativo è quello dei sistemi di guida autonoma, dove identificare rapidamente la categoria di un ostacolo è rilevante per la sicurezza.

Il modello è una **Rete Neurale Convoluzionale (CNN)** addestrata sul dataset CIFAR-10, con le classi riorganizzate in due categorie:
- **Animali**: bird, cat, deer, dog, frog, horse
- **Veicoli**: airplane, automobile, ship, truck

---

## Autore e contesto

**Autore:** Guido Pacciani  
Sviluppato come progetto finale del modulo *"Deep Learning e Reti Neurali Artificiali"* del **Master Professionale in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

---

## Struttura del progetto

```
VisionTech Solutions/
├── Riconoscimento_animali_auto_guida_autonoma.ipynb    # Notebook principale
└── README.md
```

### Contenuto del notebook

1. **Import e configurazione** — setup dell'ambiente, seed fisso per riproducibilità
2. **Caricamento dataset** — CIFAR-10 con visualizzazione campioni
3. **Preprocessing** — riorganizzazione in classi binarie e normalizzazione
4. **Architettura CNN** — 3 blocchi convoluzionali con batch normalization e dropout
5. **Addestramento** — training con EarlyStopping e validation split
6. **Valutazione** — metriche complete sul test set
7. **Analisi errori** — visualizzazione delle misclassificazioni

---

## Tecnologie utilizzate

- **TensorFlow/Keras** (2.x) — framework per deep learning
- **NumPy** — operazioni numeriche e manipolazione array
- **Matplotlib** — visualizzazione grafici e immagini
- **Pandas** — manipolazione dati tabulari

---

## Come eseguire

### Opzione 1: Google Colab (consigliato)

1. Apri [Google Colab](https://colab.research.google.com/)
2. Carica il notebook `Riconoscimento_animali_auto_guida_autonoma.ipynb`
3. Esegui tutte le celle in sequenza (Runtime → Run all)
4. Il training richiede circa 5–10 minuti su GPU

### Opzione 2: Ambiente locale

**Requisiti:** Python 3.8+, GPU opzionale ma consigliata

```bash
cd "VisionTech Solutions"
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install tensorflow numpy matplotlib pandas jupyter
jupyter notebook
```

Apri il notebook e esegui le celle in sequenza.

---

## Risultati attesi

| Metrica   | Range atteso |
|-----------|-------------|
| Accuracy  | 88–92%      |
| Precision | 88–93%      |
| Recall    | 87–91%      |
| F1-Score  | 88–92%      |

*I valori possono variare in base al seed random e all'hardware.*

Il notebook produce: grafici di training, matrice di confusione, esempi di misclassificazioni e predizioni corrette.

---

## Approfondimento tecnico

### Architettura CNN

```
Input (32×32×3)
    ↓
Conv2D(32) + BatchNorm + MaxPool
    ↓
Conv2D(64) + BatchNorm + MaxPool
    ↓
Conv2D(128) + BatchNorm + MaxPool
    ↓
Flatten
    ↓
Dense(128) + Dropout(0.4)
    ↓
Dense(64) + Dropout(0.3)
    ↓
Dense(1, sigmoid)   → probabilità binaria
```

### Scelte progettuali

- **Filtri 3×3 con padding `same`**: mantengono le dimensioni spaziali e catturano pattern locali
- **Batch Normalization**: normalizza le attivazioni a ogni layer, stabilizzando e accelerando il training
- **Dropout (40% e 30%)**: regolarizzazione per ridurre l'overfitting, disattivando casualmente neuroni durante il training
- **EarlyStopping (patience=5)**: interrompe il training se la validation loss non migliora, evitando overfitting e riducendo i tempi
- **Optimizer Adam (lr=0.001)** + **Binary Crossentropy**: standard per problemi di classificazione binaria
- **Batch size 64**: bilanciamento tra stabilità del gradiente e velocità di aggiornamento

### Valutazione

Oltre all'accuracy, vengono calcolate precision, recall e F1-score — metriche più informative in presenza di classi sbilanciate. La matrice di confusione evidenzia i falsi positivi e falsi negativi per analizzare qualitativamente gli errori del modello.

---

## Riferimenti

- **Dataset**: [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) — Canadian Institute For Advanced Research
- **Framework**: [TensorFlow](https://www.tensorflow.org/) & [Keras](https://keras.io/)

---

## Licenza

Rilasciato con licenza **MIT** — libero per uso personale, studio o sviluppo. Clona e modifica liberamente.
