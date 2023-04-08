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

def knapsack(pool_class = 1):
    loans = [] # len 50
    n = len(loans)


    for i in range(n):
        for i2 in range(len(loans)):
            # does loan[i2] fit in pool 1?



    pass

if __name__ == '__main__':
    knapsack(1)
    pass