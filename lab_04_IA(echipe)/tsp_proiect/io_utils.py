"""
Utility functions for reading and generating matrices for TSP.
"""

import random


def citeste_matrice(cale):
    """
    Read distance matrix from a file.
    
    File format:
    N
    D[0][0]  D[0][1]  ...  D[0][N-1]
    D[1][0]  D[1][1]  ...  D[1][N-1]
    ...
    
    Args:
        cale (str): Path to the input file.
    
    Returns:
        tuple: (N, matrice) where matrice is list of lists.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file format is invalid.
    """
    try:
        with open(cale, 'r') as f:
            lines = f.read().strip().split('\n')
        
        n = int(lines[0])
        matrice = []
        
        for i in range(1, n + 1):
            row = list(map(int, lines[i].split()))
            if len(row) != n:
                raise ValueError(f"Row {i} has {len(row)} elements, expected {n}")
            matrice.append(row)
        
        return n, matrice
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {cale}")
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid file format: {e}")


def genereaza_matrice_aleatorie(n, seed=None):
    """
    Generate a random symmetric distance matrix NxN with values in [1, 100].
    
    Args:
        n (int): Size of the matrix.
        seed (int, optional): Random seed for reproducibility.
    
    Returns:
        list: NxN distance matrix.
    """
    if seed is not None:
        random.seed(seed)
    
    matrice = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = random.randint(1, 100)
            matrice[i][j] = dist
            matrice[j][i] = dist
    
    return matrice


def citeste_sau_genereaza(cale=None, n=None, seed=None):
    """
    Read matrix from file or generate random matrix.
    
    Args:
        cale (str, optional): Path to input file.
        n (int, optional): Size for random matrix (used if cale is None).
        seed (int, optional): Random seed.
    
    Returns:
        tuple: (N, matrice).
    
    Raises:
        ValueError: If neither cale nor n is provided.
    """
    if cale is not None:
        return citeste_matrice(cale)
    elif n is not None:
        matrice = genereaza_matrice_aleatorie(n, seed)
        return n, matrice
    else:
        raise ValueError("Either 'cale' or 'n' must be provided")
