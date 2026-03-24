"""
Main entry point with command-line interface for TSP solving.
"""

import sys
import argparse
from io_utils import citeste_matrice, genereaza_matrice_aleatorie
from backtracking import rezolva_tsp_backtracking
from nearest_neighbor import (
    rezolva_tsp_nn,
    rezolva_tsp_nn_multistart,
    rezolva_tsp_nn_timp
)
from nn_aima import rezolva_tsp_nn_aima, rezolva_tsp_nn_aima_multistart


def format_traseu(traseu):
    """Format tour as string like '0 -> 1 -> 3 -> 2 -> 0'."""
    if not traseu:
        return "No tour found"
    return " -> ".join(map(str, traseu))


def solve_and_display(n, matrice, algoritm, mod, timp_max=None, y_max=None):
    """
    Solve TSP problem and display results.
    
    Args:
        n (int): Number of cities.
        matrice (list): Distance matrix.
        algoritm (str): Algorithm choice ('bt', 'nn', 'nn_aima').
        mod (str): Stopping mode for backtracking.
        timp_max (float): Time limit.
        y_max (int): Solution count limit.
    """
    
    print(f"\n{'='*60}")
    print(f"TSP Problem: N = {n} cities")
    print(f"Algorithm: {algoritm}")
    if mod:
        print(f"Mode: {mod}")
    if timp_max:
        print(f"Time limit: {timp_max} seconds")
    if y_max:
        print(f"Solution limit: {y_max}")
    print(f"{'='*60}\n")
    
    if algoritm == 'bt':
        result = rezolva_tsp_backtracking(n, matrice, mod=mod, timp_max=timp_max, y_max=y_max)
        
        print(f"Optimal tour (BT): {format_traseu(result['traseu'])}")
        print(f"Minimum cost:      {result['cost']}")
        print(f"Complete solutions found: {result['solutii']}")
        print(f"Execution time:    {result['timp']:.6f} seconds")
    
    elif algoritm == 'nn':
        if mod == 'prima':
            traseu, cost = rezolva_tsp_nn(n, matrice, start=0)
            print(f"NN tour (start=0): {format_traseu(traseu)}")
            print(f"Cost:              {cost}")
            print(f"Execution time:    <0.001 seconds")
        
        elif mod == 'y_solutii':
            result = rezolva_tsp_nn_multistart(n, matrice)
            print(f"NN tour (best):    {format_traseu(result['traseu'])}")
            print(f"Minimum cost:      {result['cost']}")
            print(f"Costs by starting city:")
            for start, cost in enumerate(result['costs_all']):
                print(f"  Start {start}: cost = {cost}")
            print(f"Execution time:    {result['timp']:.6f} seconds")
        
        elif mod == 'timp':
            result = rezolva_tsp_nn_timp(n, matrice, timp_max)
            print(f"NN tour (best):    {format_traseu(result['traseu'])}")
            print(f"Minimum cost:      {result['cost']}")
            print(f"NN runs completed: {result['nr_runs']}")
            print(f"Execution time:    {result['timp']:.6f} seconds")
    
    elif algoritm == 'nn_aima':
        if mod == 'prima':
            traseu, cost = rezolva_tsp_nn_aima(n, matrice, start=0)
            print(f"NN tour (aima3, start=0): {format_traseu(traseu)}")
            print(f"Cost:                     {cost}")
            print(f"Execution time:           <0.001 seconds")
        
        elif mod == 'y_solutii':
            result = rezolva_tsp_nn_aima_multistart(n, matrice)
            print(f"NN tour (aima3, best):    {format_traseu(result['traseu'])}")
            print(f"Minimum cost:             {result['cost']}")
            print(f"Costs by starting city:")
            for start, cost in enumerate(result['costs_all']):
                print(f"  Start {start}: cost = {cost}")
            print(f"Execution time:           {result['timp']:.6f} seconds")
    
    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='TSP Solver using Backtracking and Nearest Neighbor algorithms'
    )
    
    # Input specification
    parser.add_argument('input', nargs='?', help='Path to TSP input file (matrix)')
    parser.add_argument('-n', '--size', type=int, help='Generate random matrix of size N')
    parser.add_argument('-s', '--seed', type=int, default=42, help='Random seed (default 42)')
    
    # Algorithm selection
    parser.add_argument('-a', '--algoritm', choices=['bt', 'nn', 'nn_aima'], default='bt',
                        help='Algorithm choice: bt (Backtracking), nn (Nearest Neighbor), nn_aima (NN with aima3)')
    
    # Backtracking modes
    parser.add_argument('-m', '--mod', choices=['prima', 'toate', 'timp', 'y_solutii'],
                        help='Stopping mode for backtracking')
    parser.add_argument('--timp', type=float, help='Time limit in seconds (for timp mode)')
    parser.add_argument('--y', type=int, help='Solution count limit (for y_solutii mode)')
    
    args = parser.parse_args()
    
    # Load or generate matrix
    try:
        if args.input:
            n, matrice = citeste_matrice(args.input)
            print(f"Loaded matrix from {args.input}")
        elif args.size:
            n = args.size
            matrice = genereaza_matrice_aleatorie(n, seed=args.seed)
            print(f"Generated random matrix (N={n}, seed={args.seed})")
        else:
            parser.print_help()
            return
    except Exception as e:
        print(f"Error loading/generating matrix: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Set default mode based on algorithm
    mod = args.mod
    if not mod:
        if args.algoritm == 'bt':
            mod = 'toate'
        else:
            mod = 'prima'
    
    # Solve
    try:
        solve_and_display(
            n, matrice,
            algoritm=args.algoritm,
            mod=mod,
            timp_max=args.timp,
            y_max=args.y
        )
    except Exception as e:
        print(f"Error during solving: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
