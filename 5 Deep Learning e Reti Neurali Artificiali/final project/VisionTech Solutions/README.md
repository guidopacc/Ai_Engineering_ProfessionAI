# VisionTech Solutions
## Riconoscimento di animali per auto a guida autonoma

---

## Descrizione

**VisionTech Solutions** è un progetto di Deep Learning che implementa un sistema di riconoscimento automatico di immagini per distinguere tra **veicoli** e **animali**. Il sistema è stato progettato nel contesto delle auto a guida autonoma, dove l'identificazione rapida e precisa degli ostacoli sulla strada è fondamentale per garantire la sicurezza.

Il progetto utilizza una **Rete Neurale Convoluzionale (CNN)** addestrata sul dataset CIFAR-10, riorganizzato in una classificazione binaria:
- **Animali**: bird, cat, deer, dog, frog, horse
- **Veicoli**: airplane, automobile, ship, truck

---

## Autore

**Guido Pacciani**  
Sviluppato per il **Master in AI Engineering** erogato da **ProfessionAI**

---

## Obiettivi del progetto

1. Implementare una CNN per classificazione binaria di immagini
2. Applicare tecniche di preprocessing
3. Utilizzare callback per ottimizzare l'addestramento (EarlyStopping)
4. Valutare il modello con metriche complete (Accuracy, Precision, Recall, F1-Score)
5. Analizzare qualitativamente le misclassificazioni

---

## Struttura del progetto

```
VisionTech Solutions/
│
├── Riconoscimento_animali_auto_guida_autonoma.ipynb    # Notebook principale
└── README.md                                           # Questo file
```

### Contenuto del notebook

Il notebook è suddiviso in sezioni logiche:

1. **Import e Configurazione** - Setup dell'ambiente con seed riproducibile
2. **Caricamento Dataset** - CIFAR-10 con visualizzazione campioni
3. **Preprocessing** - Conversione binaria e normalizzazione
4. **Architettura CNN** - Modello con 3 blocchi convoluzionali + batch normalization + dropout
5. **Addestramento** - Training con EarlyStopping e validation split
6. **Valutazione** - Metriche complete sul test set
7. **Analisi Errori** - Visualizzazione misclassificazioni

---

## Tecnologie utilizzate

### Librerie Python

- **TensorFlow/Keras** (2.x) - Framework per Deep Learning
- **NumPy** - Operazioni numeriche e manipolazione array
- **Matplotlib** - Visualizzazione grafici e immagini
- **Pandas** - Manipolazione dati tabulari

### Architettura del modello

```
Input (32x32x3)
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
Dense(1, sigmoid)
    ↓
Output (probabilità binaria)
```

---

## Come eseguire il progetto

### Opzione 1: Google Colab

1. Apri [Google Colab](https://colab.research.google.com/)
2. Carica il notebook `Riconoscimento_animali_auto_guida_autonoma.ipynb`
3. Esegui le celle in sequenza (Runtime → Run all)
4. Attendi il completamento del training (~5-10 minuti su GPU)

### Opzione 2: Ambiente Locale

#### Requisiti

- Python 3.8+
- GPU (opzionale, ma consigliata)

#### Installazione

```bash
# Clona o scarica il repository
cd "VisionTech Solutions"

# Crea un ambiente virtuale (opzionale ma consigliato)
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

# Installa le dipendenze
pip install tensorflow numpy matplotlib pandas jupyter

# Avvia Jupyter Notebook
jupyter notebook
```

#### Esecuzione

1. Apri il notebook `Riconoscimento_animali_auto_guida_autonoma.ipynb`
2. Esegui le celle in sequenza
3. I risultati verranno visualizzati inline

---

## Risultati Attesi

Il modello raggiunge performance nell'ordine di:

- **Accuracy**: ~88-92%
- **Precision**: ~88-93%
- **Recall**: ~87-91%
- **F1-Score**: ~88-92%

*Nota: I risultati possono variare leggermente in base al seed random e all'hardware utilizzato.*

### Esempi di Output

Il notebook produce:
- Visualizzazione di campioni dal dataset
- Grafici di training (loss e accuracy)
- Matrice di confusione
- Esempi di misclassificazioni (False Positive e False Negative)
- Esempi di predizioni corrette

---

## Concetti di Deep Learning applicati

Questo progetto implementa i seguenti concetti:

### Reti Neurali Convoluzionali (CNN)
- Layer convoluzionali per estrazione automatica di features
- Pooling per riduzione dimensionalità
- Filtri 3x3 con padding 'same'

### Tecniche di ottimizzazione
- **Optimizer**: Adam (learning_rate=0.001)
- **Loss Function**: Binary Crossentropy
- **Batch Size**: 64

### Regolarizzazione
- **Dropout** (40% e 30%) per prevenire overfitting
- **Batch Normalization** per stabilizzare il training
- **EarlyStopping** con patience=5

### Valutazione
- Matrice di confusione (TP, TN, FP, FN)
- Metriche: Accuracy, Precision, Recall, F1-Score
- Analisi qualitativa degli errori

---

## Riferimenti

- **Dataset**: [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) - Canadian Institute For Advanced Research
- **Framework**: [TensorFlow](https://www.tensorflow.org/) & [Keras](https://keras.io/)
- **Corso**: Master in AI Engineering - [ProfessionAI](https://profession.ai/)

---

## Licenza

Questo progetto **non ha una licenza** formale. È stato sviluppato esclusivamente per scopi didattici nell'ambito del Master in AI Engineering.

---

## Contatti

Per domande o suggerimenti sul progetto, contatta:

**Guido Pacciani**  
Studente Master AI Engineering - ProfessionAI

---

**Sviluppato con ❤️ per il Master in AI Engineering - ProfessionAI**

