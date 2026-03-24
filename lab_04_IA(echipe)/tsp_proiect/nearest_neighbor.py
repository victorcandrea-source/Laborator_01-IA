"""
Nearest Neighbor algorithm for TSP - manual implementation.
"""

import time


def rezolva_tsp_nn(n, matrice, start=0):
    """
    Solve TSP using the Nearest Neighbor heuristic starting from a given city.
    
    Args:
        n (int): Number of cities.
        matrice (list): NxN distance matrix.
        start (int): Starting city (default 0).
    
    Returns:
        tuple: (traseu, cost) where traseu includes return to start.
    """
    
    vizitat = [False] * n
    traseu = [start]
    vizitat[start] = True
    cost = 0
    
    oras_curent = start
    
    # Construct the tour by visiting nearest unvisited city
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


def rezolva_tsp_nn_multistart(n, matrice):
    """
    Solve TSP using Nearest Neighbor with all possible starting cities.
    
    Args:
        n (int): Number of cities.
        matrice (list): NxN distance matrix.
    
    Returns:
        dict: {
            'traseu': best tour,
            'cost': minimum cost,
            'costs_all': list of costs for each starting city
        }
    """
    
    best_cost = float('inf')
    best_traseu = []
    all_costs = []
    
    # Try starting from each city
    for start in range(n):
        traseu, cost = rezolva_tsp_nn(n, matrice, start)
        all_costs.append(cost)
        
        if cost < best_cost:
            best_cost = cost
            best_traseu = traseu
    
    return {
        'traseu': best_traseu,
        'cost': best_cost,
        'costs_all': all_costs,
        'timp': 0
    }


def rezolva_tsp_nn_timp(n, matrice, timp_max):
    """
    Solve TSP using Nearest Neighbor multistart within a time limit.
    
    Args:
        n (int): Number of cities.
        matrice (list): NxN distance matrix.
        timp_max (float): Time limit in seconds.
    
    Returns:
        dict: {
            'traseu': best tour found,
            'cost': minimum cost,
            'nr_runs': number of NN runs completed,
            'timp': actual execution time
        }
    """
    
    timp_start = time.perf_counter()
    
    best_cost = float('inf')
    best_traseu = []
    nr_runs = 0
    
    start = 0
    while True:
        timp_curent = time.perf_counter() - timp_start
        if timp_curent >= timp_max:
            break
        
        traseu, cost = rezolva_tsp_nn(n, matrice, start)
        nr_runs += 1
        
        if cost < best_cost:
            best_cost = cost
            best_traseu = traseu
        
        start = (start + 1) % n
    
    timp_total = time.perf_counter() - timp_start
    
    return {
        'traseu': best_traseu,
        'cost': best_cost,
        'nr_runs': nr_runs,
        'timp': timp_total
    }
