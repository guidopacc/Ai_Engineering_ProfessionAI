# GreenTech Solutions — Classificazione binaria di fiori
## Computer Vision con Transfer Learning e GradCAM in PyTorch

---

## Descrizione

GreenTech Solutions è un progetto di computer vision per la classificazione binaria di immagini floreali: il sistema distingue tra **margherite** (*daisy*) e **denti di leone** (*dandelion*). Il modello usa ResNet18 con transfer learning da ImageNet, addestrato in due fasi con data augmentation e fine-tuning.

Il progetto include anche un'analisi di **explainability** tramite **GradCAM**, che permette di visualizzare quali regioni dell'immagine hanno influenzato la decisione del modello.

---

## Autore e contesto

**Autore:** Guido Pacciani  
Sviluppato come progetto finale del modulo *"Computer Vision"* del **Master Professionale in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

---

## Struttura del progetto

```
8 Computer Vision/final project/
├── GreenTech Solutions.ipynb    # Notebook principale
└── README.md
```

### Sezioni del notebook

1. **Setup Ambiente** — installazione dipendenze, configurazione device
2. **Download e Estrazione Dataset** — download automatico, verifica struttura cartelle
3. **DataLoader con Data Augmentation** — trasformazioni differenziate per train e validation/test
4. **Modello: ResNet18 con Transfer Learning** — caricamento modello pre-addestrato, adattamento al task binario
5. **Training Industrializzato** — training con checkpointing, early stopping e metriche per epoca
6. **Visualizzazione Training** — grafici di loss, accuracy e F1-score
7. **Valutazione su Test Set** — caricamento del best model, metriche complete
8. **Inference Demo** — esempi di predizione su immagini del test set
9. **Explainability: GradCAM** — heatmap delle regioni attivate dal modello

---

## Tecnologie utilizzate

- **PyTorch + torchvision** — framework deep learning e ResNet18 pre-addestrata
- **PIL (Pillow)** — caricamento e manipolazione immagini
- **matplotlib** — visualizzazione grafici e heatmap GradCAM
- **NumPy** — operazioni numeriche
- **scikit-learn** — metriche di valutazione (F1-score, confusion matrix)

Tutte disponibili di default su Google Colab. Per installazione locale:
```bash
pip install torch torchvision pillow matplotlib numpy scikit-learn
```

---

## Dataset

Il dataset contiene immagini di due categorie di fiori:
- **daisy** (margherita)
- **dandelion** (dente di leone)

Il download avviene automaticamente all'interno del notebook. Il codice gestisce automaticamente la struttura delle cartelle.

---

## Come eseguire

### Su Google Colab (consigliato)

1. Apri il notebook `GreenTech Solutions.ipynb` su [Google Colab](https://colab.research.google.com/)
2. Imposta il runtime su GPU: Runtime → Change runtime type → GPU
3. Esegui tutte le celle in sequenza

### In locale

```bash
pip install torch torchvision pillow matplotlib numpy scikit-learn jupyter
jupyter notebook "GreenTech Solutions.ipynb"
```

---

## Risultati attesi

Il notebook produce:
- Grafici di loss, accuracy e macro F1-score per ogni epoca (train e validation)
- Matrice di confusione sul test set
- Esempi di predizioni corrette e misclassificazioni
- Heatmap GradCAM che evidenziano le regioni rilevanti per la classificazione

---

## Approfondimento tecnico

### Transfer Learning: strategia a due fasi

**Fase 1 — Backbone congelato**: si addestra solo il classificatore finale (un layer lineare adattato al task binario). Il backbone ResNet18 rimane fisso, usando le feature rappresentazionali apprese su ImageNet. Questa fase converge rapidamente con pochi parametri aggiornabili.

**Fase 2 — Fine-tuning**: si sblocca il backbone e si riaddestra l'intera rete con un learning rate più basso. Questo permette di adattare le feature di basso livello al dominio specifico (immagini floreali), migliorando le performance rispetto al solo trasferimento di feature.

### Data Augmentation

Per il training set vengono applicate trasformazioni casuali che aumentano la varietà dei dati:
- Crop casuale e resize a 224×224
- Flip orizzontale
- Rotazione casuale
- Variazione di colore (luminosità, contrasto, saturazione)

Per validation e test set si usa solo resize + center crop, per garantire una valutazione stabile.

### Addestramento industrializzato

Il training loop implementa:
- **Checkpointing**: salva il miglior modello (per macro F1-score sulla validation) e mantiene gli ultimi 5 checkpoint
- **Early Stopping**: interrompe il training se la validation F1 non migliora per N epoche consecutive
- **Logging per epoca**: loss, accuracy e macro F1-score su training e validation set

La metrica principale è il **macro F1-score** anziché l'accuracy: in presenza di classi potenzialmente sbilanciate, il macro F1 dà lo stesso peso a entrambe le classi, evitando risultati fuorvianti.

### GradCAM (Gradient-weighted Class Activation Mapping)

GradCAM è una tecnica di explainability che genera una heatmap sovrapposta all'immagine originale, indicando le regioni che hanno maggiormente contribuito alla predizione. Il calcolo combina:
- Le **attivazioni** dell'ultimo layer convoluzionale (quali feature ha estratto la rete)
- I **gradienti** rispetto alla classe predetta (quanto ogni attivazione ha influenzato l'output)

Il risultato è una mappa di rilevanza normalizzata, utile per verificare che il modello si focalizzi sulle parti semanticamente rilevanti dell'immagine (la corolla del fiore) e non su artefatti o sfondo.

---

## Riferimenti

- [PyTorch — Transfer Learning tutorial](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
- [GradCAM — Selvaraju et al. (2017)](https://arxiv.org/abs/1610.02391)
- [torchvision — ResNet18](https://pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html)

---

## Licenza

Rilasciato con licenza **MIT** — libero per uso personale, studio o sviluppo. Clona e modifica liberamente.
