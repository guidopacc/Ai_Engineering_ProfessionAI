# Makefile

# Cartelle principali
SRC_DIR = src
INC_DIR = include
ERR_DIR = errors
DATA_DIR = data
BUILD_DIR = build

# Compilatore e flag
CXX = g++
CXXFLAGS = -std=c++11 -Wall -I$(INC_DIR) -I$(ERR_DIR)

# File sorgente
SOURCES = $(SRC_DIR)/main.cpp \
          $(SRC_DIR)/crm.cpp \
          $(SRC_DIR)/cliente.cpp \
          $(SRC_DIR)/interazione.cpp \
          $(ERR_DIR)/gestione_errori.cpp

# File oggetto corrispondenti
OBJECTS = $(BUILD_DIR)/main.o \
          $(BUILD_DIR)/crm.o \
          $(BUILD_DIR)/cliente.o \
          $(BUILD_DIR)/interazione.o \
          $(BUILD_DIR)/gestione_errori.o

# Nome dell'eseguibile
EXEC = $(BUILD_DIR)/insurapro_crm

# Regola principale
all: $(BUILD_DIR) $(DATA_DIR) $(EXEC)

# Crea la cartella build
$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

# Crea la cartella data
$(DATA_DIR):
	@mkdir -p $(DATA_DIR)

# Link finale
$(EXEC): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $(EXEC)

# Compila i .cpp in .o per i file in src
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Compila il modulo gestione_errori
$(BUILD_DIR)/gestione_errori.o: $(ERR_DIR)/gestione_errori.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Pulizia
clean:
	rm -rf $(BUILD_DIR) $(DATA_DIR)

.PHONY: all clean