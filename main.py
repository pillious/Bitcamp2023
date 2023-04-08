# EXAMPLE: Read in data from file
# import pandas as pd

# pool_df = pd.read_csv('pools.txt', sep='|')
# data_df = pd.read_csv('fnma-dataset-00.txt', sep='|')

# print(data_df.head())
# print(pool_df)
# ---------------------

# THE GENERAL PROBLEM: multiple knapsack problem with multiple constraints:

# --> Approach for multiple constraints:
# combine the multiple constraints into a single constraint
# http://hjemmesider.diku.dk/~pisinger/95-1.pdf (pg. 15)

# --> Approach for multiple knapsacks:
# ????

###
### LOOK AT THE OVERALL CONSTRAINTS IN THE README
###

import pandas as pd

import numpy as np

def multiple_knapsack(weights, profits, capacities):
    n = len(weights) # number of items
    m = len(capacities) # number of knapsacks
    
    # Initialize solution vector
    x = np.zeros((n, m), dtype=int)
    z = 0 # objective value
    
    # Sort items by non-increasing weight-to-profit ratio
    ratios = profits / weights
    indices = np.argsort(-ratios)
    
    # Assign items to knapsacks using a greedy approach
    for j in indices:
        i = np.argmax(capacities >= weights[j])
        if i != m:
            x[j, i] = 1
            z += profits[j]
            capacities[i] -= weights[j]
    
    # Improve solution using a branch-and-bound approach
    def branch_and_bound(h, P, W, c):
        nonlocal x, z
        
        # Solve relaxed problem
        u = (profits @ x.sum(axis=1)).max()
        if P <= u:
            return
        
        # Check if solution is feasible
        if (c >= weights.sum(axis=0)).all():
            x_best = x.copy()
            z = P
            return
        
        # Choose branching item with largest profit-to-weight ratio
        j = np.argmax(profits / weights * (x.sum(axis=1) < c))
        for i in range(m):
            if capacities[i] < weights[j]:
                continue
            x[j, i] = 1
            capacities[i] -= weights[j]
            branch_and_bound(h+1, (P-profits[j]), (W-weights[j]), capacities)
            x[j, i] = 0
            capacities[i] += weights[j]
    
    # Run branch-and-bound algorithm to improve solution
    x_best = x.copy()
    branch_and_bound(0, z, weights.sum(), capacities)
    x = x_best
    
    return x, z

def knapsack(pool_class = 1):
    loans = [] # len 50
    n = len(loans)


    for i in range(n):
        for i2 in range(len(loans)):
            # does loan[i2] fit in pool 1?
            pass

    pass

if __name__ == '__main__':
    # knapsack(1)

    knapsack(1)

    # pass
