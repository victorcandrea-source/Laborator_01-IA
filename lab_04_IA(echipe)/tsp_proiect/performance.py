"""
Performance analysis and graphing for TSP algorithms.
"""

import random
import time
import matplotlib.pyplot as plt
import numpy as np
from io_utils import genereaza_matrice_aleatorie
from backtracking import rezolva_tsp_backtracking
from nearest_neighbor import rezolva_tsp_nn, rezolva_tsp_nn_multistart


def genereaza_matrice_aleatorie_local(n, seed=None):
    """Generate random distance matrix."""
    return genereaza_matrice_aleatorie(n, seed)


def masoara_timp_bt(n, matrice, mod, timp_max=None, y_max=None):
    """Measure execution time for backtracking."""
    result = rezolva_tsp_backtracking(n, matrice, mod=mod, timp_max=timp_max, y_max=y_max)
    return result['timp'], result['cost']


def masoara_timp_nn(n, matrice, multistart=False):
    """Measure execution time for Nearest Neighbor."""
    timp_start = time.perf_counter()
    
    if multistart:
        result = rezolva_tsp_nn_multistart(n, matrice)
    else:
        traseu, cost = rezolva_tsp_nn(n, matrice, start=0)
        result = {'cost': cost, 'traseu': traseu}
    
    timp_total = time.perf_counter() - timp_start
    
    return timp_total, result['cost']


def ruleaza_experiment():
    """
    Run comparative experiment for backtracking and NN algorithms.
    
    Measures execution times for different N values and stopping modes.
    """
    
    print("\n" + "="*70)
    print("TSP Performance Experiment")
    print("="*70 + "\n")
    
    valori_n_bt = [5, 8, 10, 12]
    valori_n_nn = [5, 8, 10, 12, 15, 20, 30, 50]
    
    random.seed(42)
    
    # Data collection
    timpi_bt_prima = []
    timpi_bt_toate = []
    timpi_nn_single = []
    timpi_nn_multistart = []
    
    costs_bt_prima = []
    costs_bt_toate = []
    costs_nn_single = []
    costs_nn_multistart = []
    
    print("Running experiments (this may take a while)...\n")
    
    # Backtracking - 'prima' mode
    print("BT (prima mode)...", end=" ", flush=True)
    for n in valori_n_bt:
        matrice = genereaza_matrice_aleatorie_local(n, seed=42+n)
        try:
            timp, cost = masoara_timp_bt(n, matrice, mod='prima')
            timpi_bt_prima.append(timp)
            costs_bt_prima.append(cost)
        except Exception as e:
            print(f"Error for N={n}: {e}")
            timpi_bt_prima.append(None)
            costs_bt_prima.append(None)
    print("Done")
    
    # Backtracking - 'toate' mode
    print("BT (toate mode)...", end=" ", flush=True)
    for n in valori_n_bt:
        matrice = genereaza_matrice_aleatorie_local(n, seed=42+n)
        try:
            timp, cost = masoara_timp_bt(n, matrice, mod='toate')
            timpi_bt_toate.append(timp)
            costs_bt_toate.append(cost)
        except Exception as e:
            print(f"Error for N={n}: {e}")
            timpi_bt_toate.append(None)
            costs_bt_toate.append(None)
    print("Done")
    
    # NN - single start
    print("NN (single start)...", end=" ", flush=True)
    for n in valori_n_nn:
        matrice = genereaza_matrice_aleatorie_local(n, seed=42+n)
        try:
            timp, cost = masoara_timp_nn(n, matrice, multistart=False)
            timpi_nn_single.append(timp)
            costs_nn_single.append(cost)
        except Exception as e:
            print(f"Error for N={n}: {e}")
            timpi_nn_single.append(None)
            costs_nn_single.append(None)
    print("Done")
    
    # NN - multistart
    print("NN (multistart)...", end=" ", flush=True)
    for n in valori_n_nn:
        matrice = genereaza_matrice_aleatorie_local(n, seed=42+n)
        try:
            timp, cost = masoara_timp_nn(n, matrice, multistart=True)
            timpi_nn_multistart.append(timp)
            costs_nn_multistart.append(cost)
        except Exception as e:
            print(f"Error for N={n}: {e}")
            timpi_nn_multistart.append(None)
            costs_nn_multistart.append(None)
    print("Done")
    
    # Display results
    print("\n" + "="*70)
    print("Execution Times (seconds):")
    print("="*70)
    print(f"{'N':<5} {'BT-prima':<15} {'BT-toate':<15} {'NN-single':<15} {'NN-multistart':<15}")
    print("-"*70)
    
    for i, n in enumerate(valori_n_bt):
        bt_prima = f"{timpi_bt_prima[i]:.6f}" if timpi_bt_prima[i] is not None else "Error"
        bt_toate = f"{timpi_bt_toate[i]:.6f}" if timpi_bt_toate[i] is not None else "Error"
        nn_single = f"{timpi_nn_single[i]:.6f}" if timpi_nn_single[i] is not None else "Error"
        nn_multi = f"{timpi_nn_multistart[i]:.6f}" if timpi_nn_multistart[i] is not None else "Error"
        print(f"{n:<5} {bt_prima:<15} {bt_toate:<15} {nn_single:<15} {nn_multi:<15}")
    
    for i in range(len(valori_n_bt), len(valori_n_nn)):
        n = valori_n_nn[i]
        nn_single = f"{timpi_nn_single[i]:.6f}" if timpi_nn_single[i] is not None else "Error"
        nn_multi = f"{timpi_nn_multistart[i]:.6f}" if timpi_nn_multistart[i] is not None else "Error"
        print(f"{n:<5} {'N/A':<15} {'N/A':<15} {nn_single:<15} {nn_multi:<15}")
    
    # Generate graphical output
    genereaza_grafic_timpi(valori_n_bt, valori_n_nn, timpi_bt_prima, timpi_bt_toate,
                          timpi_nn_single, timpi_nn_multistart)
    
    genereaza_grafic_calitate(valori_n_bt, costs_bt_toate, costs_nn_multistart)
    
    print("\n" + "="*70)
    print("Graphs saved as PNG files in current directory")
    print("="*70 + "\n")


def genereaza_grafic_timpi(valori_n_bt, valori_n_nn, timpi_bt_prima, timpi_bt_toate,
                          timpi_nn_single, timpi_nn_multistart):
    """Generate performance comparison graphs."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Linear scale
    ax1.plot(valori_n_bt, timpi_bt_prima, 'o-', label='BT (prima)', linewidth=2, markersize=8)
    ax1.plot(valori_n_bt, timpi_bt_toate, 's-', label='BT (toate)', linewidth=2, markersize=8)
    ax1.plot(valori_n_nn, timpi_nn_single, '^-', label='NN (single)', linewidth=2, markersize=8)
    ax1.plot(valori_n_nn, timpi_nn_multistart, 'd-', label='NN (multistart)', linewidth=2, markersize=8)
    
    ax1.set_xlabel('Number of cities (N)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Execution time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('TSP Algorithm Performance - Linear Scale', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    
    # Logarithmic scale
    ax2.semilogy(valori_n_bt, timpi_bt_prima, 'o-', label='BT (prima)', linewidth=2, markersize=8)
    ax2.semilogy(valori_n_bt, timpi_bt_toate, 's-', label='BT (toate)', linewidth=2, markersize=8)
    ax2.semilogy(valori_n_nn, timpi_nn_single, '^-', label='NN (single)', linewidth=2, markersize=8)
    ax2.semilogy(valori_n_nn, timpi_nn_multistart, 'd-', label='NN (multistart)', linewidth=2, markersize=8)
    
    ax2.set_xlabel('Number of cities (N)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Execution time (seconds, log scale)', fontsize=12, fontweight='bold')
    ax2.set_title('TSP Algorithm Performance - Logarithmic Scale', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('comparare_performanta.png', dpi=150, bbox_inches='tight')
    print("Saved: comparare_performanta.png")
    plt.close()


def genereaza_grafic_calitate(valori_n, costs_bt, costs_nn):
    """Generate solution quality comparison graph."""
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use only values where both BT and NN have results
    x = np.arange(len(valori_n))
    width = 0.35
    
    # Filter costs to match lengths
    costs_bt_filtered = costs_bt[:len(valori_n)]
    costs_nn_filtered = costs_nn[:len(valori_n)]
    
    ax.bar(x - width/2, costs_bt_filtered, width, label='BT (optimal)', color='steelblue', alpha=0.8)
    ax.bar(x + width/2, costs_nn_filtered, width, label='NN (multistart)', color='coral', alpha=0.8)
    
    ax.set_xlabel('Number of cities (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Solution cost', fontsize=12, fontweight='bold')
    ax.set_title('Solution Quality: Backtracking vs Nearest Neighbor', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(valori_n)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('calitate_solutii.png', dpi=150, bbox_inches='tight')
    print("Saved: calitate_solutii.png")
    plt.close()


def genereaza_grafic_gap():
    """
    Generate gap% graph comparing NN vs optimal BT solutions.
    
    Gap% = (cost_NN - cost_BT_optimal) / cost_BT_optimal * 100
    """
    
    print("\nGenerating gap analysis...", end=" ", flush=True)
    
    valori_n = [5, 7, 8, 10, 12]
    gaps = []
    
    random.seed(42)
    
    for n in valori_n:
        matrice = genereaza_matrice_aleatorie_local(n, seed=42+n)
        
        # Get optimal solution with BT
        result_bt = rezolva_tsp_backtracking(n, matrice, mod='toate')
        cost_bt = result_bt['cost']
        
        # Get NN multistart solution
        result_nn = rezolva_tsp_nn_multistart(n, matrice)
        cost_nn = result_nn['cost']
        
        gap = ((cost_nn - cost_bt) / cost_bt) * 100 if cost_bt > 0 else 0
        gaps.append(gap)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['green' if g == 0 else 'orange' if g < 20 else 'red' for g in gaps]
    bars = ax.bar([str(n) for n in valori_n], gaps, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Number of cities (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Gap from optimal (%)', fontsize=12, fontweight='bold')
    ax.set_title('Nearest Neighbor vs Optimal (Backtracking) Solution', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, gap in zip(bars, gaps):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{gap:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('gap_analysis.png', dpi=150, bbox_inches='tight')
    print("Done")
    print("Saved: gap_analysis.png")
    plt.close()


if __name__ == '__main__':
    ruleaza_experiment()
    genereaza_grafic_gap()
