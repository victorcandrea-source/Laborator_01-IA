#!/usr/bin/env python3

from io_utils import citeste_matrice
from nearest_neighbor import rezolva_tsp_nn, rezolva_tsp_nn_multistart
from nn_aima import rezolva_tsp_nn_aima, rezolva_tsp_nn_aima_multistart

n, matrice = citeste_matrice('orase5.txt')

print("\n=== Comparing NN Manual vs AIMA3 ===\n")

# Single start
print("Single start (from city 0):")
traseu_mn, cost_mn = rezolva_tsp_nn(n, matrice, start=0)
traseu_aima, cost_aima = rezolva_tsp_nn_aima(n, matrice, start=0)
print(f"  Manual: {' -> '.join(map(str, traseu_mn))} (cost={cost_mn})")
print(f"  AIMA3:  {' -> '.join(map(str, traseu_aima))} (cost={cost_aima})")
print(f"  Match: {cost_mn == cost_aima}")

# Multistart
print("\nMultistart (all starting cities):")
result_mn = rezolva_tsp_nn_multistart(n, matrice)
result_aima = rezolva_tsp_nn_aima_multistart(n, matrice)
print(f"  Manual best cost: {result_mn['cost']}")
print(f"  AIMA3 best cost:  {result_aima['cost']}")
print(f"  Match: {result_mn['cost'] == result_aima['cost']}")

print("\n" + "="*50 + "\n")
