
# TSP Solver - Laborator 04 (Euristica celui mai apropiat vecin)

Implementare completa pentru rezolvarea Problemei Comis-Voiajorului (TSP) folosind:
- **Backtracking** cu 4 moduri de oprire configurabile
- **Nearest Neighbor (NN)** - implementare manuala
- **Nearest Neighbor cu aima3** - wrapper peste biblioteca AIMA3
- **Analiza de performanta** cu grafice comparative

## Structura Proiectului

```
tsp_proiect/
├── main.py               # CLI entry point
├── io_utils.py           # File I/O and matrix generation
├── backtracking.py       # Backtracking algorithm with 4 stopping modes
├── nearest_neighbor.py   # Manual NN implementation
├── nn_aima.py           # NN using aima3 library
├── performance.py        # Performance analysis and graphing
├── orase.txt            # Sample input (4 cities)
├── orase5.txt           # Sample input (5 cities)
└── README.md
```

## Instalare si Pregatire

```bash
# Activate virtual environment
cd /Users/candreavictor/IA
source .venv/bin/activate

# Navigate to project
cd lab_04_IA\(echipe\)/tsp_proiect

# Requirements are already installed (aima3, matplotlib)
pip install aima3 matplotlib
```

## Utilizare

### Sarcina A - Backtracking cu 4 Moduri

```bash
# Modul 'prima' - prima solutie gasita
python main.py orase.txt --algoritm bt --mod prima

# Modul 'toate' - solutie optima garantata (exhaustiv)
python main.py orase.txt --algoritm bt --mod toate

# Modul 'timp' - cea mai buna solutie dupa T secunde
python main.py orase.txt --algoritm bt --mod timp --timp 2

# Modul 'y_solutii' - cea mai buna din primele Y solutii
python main.py orase.txt --algoritm bt --mod y_solutii --y 10

# Cu o matrice aleatorie (N=10)
python main.py -n 10 --algoritm bt --mod toate
```

### Sarcina B - Nearest Neighbor

```bash
# NN manual - varianta de baza (start din oras 0)
python main.py orase.txt --algoritm nn --mod prima

# NN manual - multistart (incerca din toate orasele)
python main.py orase.txt --algoritm nn --mod y_solutii --y 5

# NN cu aima3 - varianta de baza
python main.py orase.txt --algoritm nn_aima --mod prima

# NN cu aima3 - multistart
python main.py orase.txt --algoritm nn_aima --mod y_solutii
```

### Sarcina C - Grafice de Performanta

```bash
# Ruleaza experimentul complet si genereaza grafice
python performance.py
```

Genereaza 3 grafice PNG:
- **comparare_performanta.png** - Timpi de executie (scala liniara + logaritmica)
- **calitate_solutii.png** - Cost al solutiilor BT vs NN
- **gap_analysis.png** - Gap% dintre NN si optim

## Exemple de Output

### Backtracking (BT)
```
Loaded matrix from orase.txt

============================================================
TSP Problem: N = 4 cities
Algorithm: bt
Mode: toate
============================================================

Optimal tour (BT): 0 -> 1 -> 3 -> 2 -> 0
Minimum cost:      80
Complete solutions found: 4
Execution time:    0.000012 seconds
```

### Nearest Neighbor (NN)
```
Loaded matrix from orase5.txt

============================================================
TSP Problem: N = 5 cities
Algorithm: nn
Mode: y_solutii
Solution limit: 5
============================================================

NN tour (best):    1 -> 3 -> 4 -> 2 -> 0 -> 1
Minimum cost:      14
Costs by starting city:
  Start 0: cost = 17
  Start 1: cost = 14
  Start 2: cost = 14
  Start 3: cost = 17
  Start 4: cost = 17
Execution time:    0.000104 seconds
```

## Rezultate Experimentale

### Timpi de Executie (pentru orase aleatoare, seed=42)

| N  | BT-prima | BT-toate | NN-single | NN-multistart |
|---|----------|----------|-----------|---------------|
| 5  | 0.000006 | 0.000019 | 0.000005  | 0.000012      |
| 8  | 0.000005 | 0.000944 | 0.000005  | 0.000026      |
| 10 | 0.000005 | 0.009112 | 0.000005  | 0.000043      |
| 12 | 0.000006 | 0.054216 | 0.000006  | 0.000075      |

### Observatii Cheie

1. **Backtracking exhaustiv (modul 'toate')**:
   - Garanteaza optimalitate
   - Complexitate exponentiala O((N-1)!)
   - Prohibitiv pentru N > 12-13
   - Prunerea branch-and-bound optimizeaza cautarea

2. **Nearest Neighbor**:
   - Complexitate O(N^2) - foarte rapid
   - Nu garanteaza optimalitate
   - Gap tipic: 0-30% fata de optim
   - Ideal pentru probleme mari (N > 100)

3. **Moduri de Oprire BT**:
   - **prima**: Instantaneu, calitate imprevizibila
   - **toate**: Optim garantat, timp exponential
   - **timp**: Compromis: rulare limitata, imbunatatire progresiva
   - **y_solutii**: Se opeste dupa Y solutii; utila pentru comparatie cu NN multistart

## Docstrings si Cod

Toate functiile publice includ docstrings in stil Google cu sectiunile:
- `Args`: Parametri de intrare
- `Returns`: Valori returnate
- `Raises`: Exceptii posibile (daca aplicabil)

Comentariile din cod nu contin diacritice (conform cerinte).

## Teste

```bash
# Test individual module
python -c "from nearest_neighbor import rezolva_tsp_nn; n, mat = 4, [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]; print(rezolva_tsp_nn(n, mat))"

# Compara NN manual vs NN aima3
python test_comparison.py
```

## Note Importante

- Program-ul accepta atat fisiere input cat si generare aleatorie (-n option)
- Seed-ul pentru aleatorie este setat la 42 pentru reproductibilitate
- Matricile de distante trebuie simetrice (D[i][j] = D[j][i])
- Diagonala matricei trebuie sa fie 0 (distanta unui oras la el insusi)

## Cerinte Laborator

✓ Sarcina A - Backtracking cu 4 moduri de oprire  
✓ Sarcina B - NN manual + NN cu aima3 in acelasi proiect  
✓ Sarcina C - Grafice de performanta (3 grafice generate)  
