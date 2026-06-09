# Cyber Security per la sanità tramite Reinforcement Learning

Progetto didattico per simulare e mitigare scenari di attacco/difesa in reti informatiche sanitarie usando Reinforcement Learning. L'ambiente è basato su `gym-idsgame` e il deliverable principale è un notebook Colab con SARSA tabulare e Double DQN.

## Requisiti
- Python 3.10+
- Dipendenze in `requirements.txt`

## Avvio rapido (locale)
```bash
python -m pip install -r requirements.txt
```
Apri il notebook `notebooks/DeepGuard_RL_CyberSecurity_Colab.ipynb` con Jupyter/VS Code oppure caricalo su Google Colab.

## Struttura del progetto
- `notebooks/DeepGuard_RL_CyberSecurity_Colab.ipynb`: notebook completo (setup, training, valutazione)
- `src/`: moduli Python (SARSA, DDQN, utilities, wrapper ambiente)
- `assets/`: immagini/grafici opzionali

## Consegna
Il deliverable richiesto è il notebook `notebooks/DeepGuard_RL_CyberSecurity_Colab.ipynb`, pronto per essere aperto ed eseguito in Google Colab.
