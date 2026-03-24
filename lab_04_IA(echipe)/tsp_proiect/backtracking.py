"""
Backtracking algorithm for TSP with 4 configurable stopping modes.
"""

import time
import sys


def rezolva_tsp_backtracking(n, matrice, mod='toate', timp_max=None, y_max=None):
    """
    Solve TSP using backtracking with configurable stopping modes.
    
    Stopping modes:
    - 'prima': Stop at first complete solution.
    - 'toate': Explore entire solution space (exhaustive, optimal guarantee).
    - 'timp': Stop after timp_max seconds, return best solution so far.
    - 'y_solutii': Stop after finding y_max complete solutions.
    
    Args:
        n (int): Number of cities.
        matrice (list): NxN distance matrix.
        mod (str): Stopping mode ('prima', 'toate', 'timp', 'y_solutii').
        timp_max (float, optional): Time limit in seconds (for 'timp' mode).
        y_max (int, optional): Solution count limit (for 'y_solutii' mode).
    
    Returns:
        dict: {
            'traseu': list of cities in order,
            'cost': total cost,
            'solutii': number of complete solutions found,
            'timp': execution time in seconds
        }
    """
    
    if mod not in ['prima', 'toate', 'timp', 'y_solutii']:
        raise ValueError(f"Invalid stopping mode: {mod}")
    
    timp_start = time.perf_counter()
    
    # Shared state
    state = {
        'cost_minim': float('inf'),
        'traseu_optim': [],
        'nr_solutii': 0,
        'oprire': False,
        'timp_start': timp_start
    }
    
    def backtrack(oras_curent, vizitat, traseu, cost):
        # Check stopping conditions
        if state['oprire']:
            return
        
        # Check time limit
        if mod == 'timp' and timp_max is not None:
            timp_curent = time.perf_counter() - timp_start
            if timp_curent >= timp_max:
                state['oprire'] = True
                return
        
        # Base case: all cities visited
        if len(traseu) == n:
            cost_total = cost + matrice[oras_curent][traseu[0]]
            state['nr_solutii'] += 1
            
            if cost_total < state['cost_minim']:
                state['cost_minim'] = cost_total
                state['traseu_optim'] = traseu[:]
            
            # Check stopping conditions after finding a solution
            if mod == 'prima':
                state['oprire'] = True
            elif mod == 'y_solutii' and y_max is not None:
                if state['nr_solutii'] >= y_max:
                    state['oprire'] = True
            
            return
        
        # Try extending the tour
        for urmator in range(n):
            if state['oprire']:
                return
            
            if vizitat[urmator]:
                continue
            
            cost_nou = cost + matrice[oras_curent][urmator]
            
            # Branch and bound pruning (for modes that guarantee optimality)
            if mod in ['toate', 'prima', 'y_solutii'] and cost_nou >= state['cost_minim']:
                continue
            
            vizitat[urmator] = True
            traseu.append(urmator)
            
            backtrack(urmator, vizitat, traseu, cost_nou)
            
            traseu.pop()
            vizitat[urmator] = False
    
    # Start backtracking from city 0
    vizitat = [False] * n
    traseu = [0]
    vizitat[0] = True
    
    backtrack(0, vizitat, traseu, 0)
    
    timp_total = time.perf_counter() - timp_start
    
    # Build final tour
    if state['traseu_optim']:
        tour = state['traseu_optim'] + [state['traseu_optim'][0]]
    else:
        tour = []
    
    return {
        'traseu': tour,
        'cost': state['cost_minim'],
        'solutii': state['nr_solutii'],
        'timp': timp_total
    }
