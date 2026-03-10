#!/bin/zsh
# ===============================================
# Setup ambiente Python per Deep Learning su macOS (Apple Silicon)
# ===============================================

# 1. Crea un ambiente virtuale chiamato .venv
python3 -m venv .venv

# 2. Attiva l'ambiente virtuale
source .venv/bin/activate

# 3. Aggiorna pip e strumenti base
python -m pip install -U pip setuptools wheel ipykernel

# 4. Installa le librerie scientifiche
python -m pip install numpy pandas matplotlib

# 5. Installa TensorFlow ottimizzato per Apple Silicon
python -m pip install tensorflow-macos tensorflow-metal

# 6. (Facoltativo) Installa Jupyter per aprire direttamente i .ipynb
python -m pip install notebook jupyterlab

# 7. Registra il kernel per Jupyter/VS Code
python -m ipykernel install --user --name proj-dl --display-name "Python (proj-dl)"

# 8. Messaggio finale
echo "Setup completato!"
echo "   - Ambiente virtuale creato in .venv"
echo "   - Kernel registrato come: Python (proj-dl)"
echo "   - In VS Code seleziona: Jupyter → Select Notebook Kernel → Python (proj-dl)"

alias workon='source .venv/bin/activate'