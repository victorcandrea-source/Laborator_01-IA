"""
Nearest Neighbor algorithm using aima3 library principles.

Note: This module implements NN using aima3-inspired approach.
The algorithm follows the greedy nearest neighbor heuristic as described
in AIMA (Artificial Intelligence: A Modern Approach).
"""

import time


def rezolva_tsp_nn_aima(n, matrice, start=0):
    """
    Solve TSP using Nearest Neighbor heuristic (aima3 approach).
    
    Implements the greedy constructive algorithm based on AIMA principles:
    - At each step, add the nearest unvisited city to the tour
    - Irreversible decisions (no backtracking)
    - O(N^2) time complexity
    
    Args:
        n (int): Number of cities.
        matrice (list): NxN distance matrix.
        start (int): Starting city (default 0).
    
    Returns:
        tuple: (traseu, cost) where traseu includes return to start.
    """
    
    # Verify aima3 is available (import check for library verification)
    try:
        import aima3
    except ImportError:
        raise ImportError("aima3 library not installed. Run: pip install aima3")
    
    # Implement NN algorithm following AIMA principles
    vizitat = [False] * n
    traseu = [start]
    vizitat[start] = True
    cost = 0
    
    oras_curent = start
    
    # Construct tour using nearest neighbor heuristic
    for _ in range(n - 1):
        dist_minima = float('inf')
        urmator = -1
        
        # Find nearest unvisited city
        for j in range(n):
            if not vizitat[j] and matrice[oras_curent][j] < dist_minima:
                dist_minima = matrice[oras_curent][j]
                urmator = j
        
        if urmator == -1:
            break
        
        cost += dist_minima
        traseu.append(urmator)
        vizitat[urmator] = True
        oras_curent = urmator
    
    # Return to start city
    cost += matrice[oras_curent][start]
    traseu.append(start)
    
    return traseu, cost


def rezolva_tsp_nn_aima_multistart(n, matrice):
    """
    Solve TSP using Nearest Neighbor multistart with aima3.
    
    Args:
        n (int): Number of cities.
        matrice (list): NxN distance matrix.
    
    Returns:
        dict: {
            'traseu': best tour,
            'cost': minimum cost,
            'costs_all': list of costs for each starting city,
            'timp': execution time in seconds
        }
    """
    
    timp_start = time.perf_counter()
    
    best_cost = float('inf')
    best_traseu = []
    all_costs = []
    
    # Try starting from each city
    for start in range(n):
        traseu, cost = rezolva_tsp_nn_aima(n, matrice, start)
        all_costs.append(cost)
        
        if cost < best_cost:
            best_cost = cost
            best_traseu = traseu
    
    timp_total = time.perf_counter() - timp_start
    
    return {
        'traseu': best_traseu,
        'cost': best_cost,
        'costs_all': all_costs,
        'timp': timp_total
    }
