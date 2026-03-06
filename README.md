# AI Engineering – ProfessionAI

Raccolta di progetti sviluppati durante il **Master professionalizzante in AI Engineering** erogato da [ProfessionAI](https://profession.ai/).

**Autore:** Guido Pacciani

---

## Struttura del repository

Il repository è organizzato in moduli tematici, ognuno corrispondente a un corso del master:

| # | Modulo | Descrizione | Progetto finale |
|---|--------|-------------|-----------------|
| 1 | [Python Programming](#1-python-programming) | Programmazione Python con architettura modulare | ContactEase – gestore contatti CLI |
| 2 | [C++ Programming](#2-c-programming) | Programmazione avanzata in C++ | InsuraPro – CRM per assicurazioni |
| 3 | [Machine Learning Fundamentals](#3-machine-learning-fundamentals) | Algoritmi di ML e tecniche di regressione regolarizzata | RealEstateAI – previsione prezzi immobiliari |
| 4 | [Machine Learning: Modelli e Algoritmi](#4-machine-learning-modelli-e-algoritmi) | Classificazione con KNN e pipeline scikit-learn | TropicTaste – classificazione frutti esotici |
| 5 | [Deep Learning e Reti Neurali Artificiali](#5-deep-learning-e-reti-neurali-artificiali) | CNN con Keras/TensorFlow per classificazione binaria | VisionTech Solutions – riconoscimento animali vs veicoli |
| 6 | [MLOps e Machine Learning in Produzione](#6-mlops-e-machine-learning-in-produzione) | Pipeline MLOps, API REST, monitoring e CI/CD | MachineInnovators Inc – sentiment reputation monitoring |
| 7 | [Deep Learning applicato con PyTorch](#7-deep-learning-applicato-con-pytorch) | Transfer learning e fine-tuning con PyTorch | GourmetAI Inc – classificazione immagini di cibo |
| 8 | [Computer Vision](#8-computer-vision) | Computer Vision con Transfer Learning e GradCAM | GreenTech Solutions – classificazione binaria di fiori |

---

## 1. Python Programming

**Progetto:** [ContactEase](./1%20Python%20Programming/Contactease%20Software/)

Gestore di contatti da riga di comando (CLI) sviluppato in Python con architettura modulare (MVC). Permette di aggiungere, modificare, eliminare e cercare contatti, salvati persistentemente in un file JSON.

**Tecnologie:** Python 3.10+

---

## 2. C++ Programming

**Progetto:** [InsuraPro Solutions CRM](./2%20C%2B%2B%20Programming/insurapro/)

Sistema CRM (Customer Relationship Management) da terminale sviluppato in C++, pensato per imprese assicurative. Gestisce clienti, appuntamenti, contratti, telefonate ed email con persistenza su file di testo.

**Tecnologie:** C++11, g++/clang++, Makefile

---

## 3. Machine Learning Fundamentals

**Progetto:** [RealEstateAI](./3_Machine_Learning_Fundamentals/realestateAI/)

Modello di previsione del prezzo degli immobili basato su tecniche di regressione lineare regolarizzata (Ridge, Lasso, Elastic Net). Il progetto confronta i tre modelli e seleziona il migliore tramite ricerca degli iperparametri e validazione incrociata.

**Tecnologie:** Python, scikit-learn, numpy, pandas, matplotlib

---

## 4. Machine Learning: Modelli e Algoritmi

**Progetto:** [TropicTaste Inc.](./4_Machine_Learning_Modelli_e_Algoritmi/TropicTaste%20Inc./)

Sistema di classificazione automatica di frutti esotici tramite l'algoritmo **K-Nearest Neighbors (KNN)**. Utilizza caratteristiche numeriche (peso, diametro, dolcezza, ecc.) per predire il tipo di frutto.

**Tecnologie:** Python, scikit-learn, pandas, matplotlib, seaborn

---

## 5. Deep Learning e Reti Neurali Artificiali

**Progetto:** [VisionTech Solutions](./5%20Deep%20Learning%20e%20Reti%20Neurali%20Artificiali/final%20project/VisionTech%20Solutions/)

Rete Neurale Convoluzionale (CNN) per la classificazione binaria di immagini del dataset CIFAR-10, riorganizzato in **animali** vs **veicoli**. Il sistema è progettato per applicazioni di auto a guida autonoma.

**Tecnologie:** Python, TensorFlow/Keras, numpy, matplotlib

---

## 6. MLOps e Machine Learning in Produzione

**Progetto:** [MachineInnovators Inc.](./6%20MLOps%20e%20Machine%20Learning%20in%20Produzione/final%20project/MachineInnovators%20Inc/)

Pipeline MLOps end-to-end per il monitoraggio della reputazione online tramite **sentiment analysis** su testi social. Include un'API REST (FastAPI), monitoring con Prometheus/Grafana, CI/CD con GitHub Actions, rilevamento del concept drift e retraining automatico.

**Tecnologie:** Python, FastAPI, Transformers (HuggingFace), PyTorch, Docker, Prometheus, Grafana, GitHub Actions

---

## 7. Deep Learning applicato con PyTorch

**Progetto:** [GourmetAI Inc.](./7%20Deep%20Learning%20applicato%20con%20PyTorch/final%20project/GourmetAI%20Inc./)

Sistema di classificazione di immagini di cibo su 14 categorie, utilizzando **Transfer Learning** con ResNet18 pre-addestrato su ImageNet. Il progetto applica data augmentation, fine-tuning e tecniche di regolarizzazione (dropout, weight decay).

**Tecnologie:** Python, PyTorch, torchvision, matplotlib, scikit-learn

---

## 8. Computer Vision

**Progetto:** [GreenTech Solutions](./8%20Computer%20Vision/final%20project/)

Sistema di **classificazione binaria di immagini** per distinguere tra margherite (daisy) e denti di leone (dandelion), utilizzando Transfer Learning con ResNet18 in una strategia a due fasi. Include Data Augmentation avanzata, checkpointing, early stopping e **GradCAM** per l'explainability del modello.

**Tecnologie:** Python, PyTorch, timm, torchvision, matplotlib, scikit-learn

---

## Corso di riferimento

**Master in AI Engineering** – [ProfessionAI](https://profession.ai/)

---

## Licenza

Tutti i progetti sono stati sviluppati esclusivamente per scopi didattici nell'ambito del Master in AI Engineering erogato da ProfessionAI.
