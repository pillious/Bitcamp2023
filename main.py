import json
import pandas as pd

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
# LOOK AT THE OVERALL CONSTRAINTS IN THE README
###

# class Pool:
#     def __init__(maturity_date: int, loan_term: int, curr_states, loans_in_pool = []) -> None:
#         # [pool_class, maturity date, loan term, curr balance, curr state %, loans in pool, property type*]
#         # curr states can be an array of ints? MA/len(loans_in_pool) => pct
#         self.maturity_date = maturity_date
#         self.loan_term = loan_term
#         self.curr_state_pct = curr_state_pct
#         self.loans_in_pool = loans_in_pool

# def create_pool(maturity_date, loan_term, curr_state, loans_in_pool):
#     return []


def gen_datastructure():
    categories = {
        "1": {},
        "2": {},
        "3": {},
        "4": {},
        "5": {},
        "6": {},
        "7": {},
        "8": {},
        "9": {},
        "10": {}
    }

    df = pd.read_csv('fnma-dataset-classified.txt', sep='|')

    # first pass (create initial categories)
    for _, row in df.iterrows():
        if pd.notna(row['classes']):
            row_list = list(row)
            classes = row['classes'].split(',')
            try:
                key = f"{str(int(row['maturity_date']))}-{str(row['loan_term'])}"
                if (len(classes) > 1):
                    row_list[-1] = ",".join(classes[1:])
                elif(len(classes) == 1):
                    row_list[-1] = ""

                if categories.get(key) is None:
                    categories[classes[0]][key] = [row_list]
                else:
                    categories[classes[0]][key].append(row_list)
            except:
                pass

    with open('categories.json', 'w') as file:
        json.dump(categories, file)

def knapsack():
    categories = {}

    pools = []

    max_size = [20, 20, 20, 20, 20, 30, 30, 40, 40, 40]
    state_pct = [0.05, 0.05, 0.1, 0.05, 0.05, 0.15, 0.05, 0.05, 0.25]

    with open('categories.json', 'r') as file:
        categories = json.load(file)

    print(categories.keys())
    for pclass in range(1, 10):
        for k, v in categories[str(pclass)].items():
            # for each v -> array of loans --> run the alg
            # if enough loans

            cat = categories[str(pclass)][k]

            if (pclass == 1 or pclass == 2 or pclass == 4 or pclass == 5 or pclass == 7 or pclass == 8 or pclass == 9) and len(cat) <= 20:
                # redistribute
                pass
            elif pclass == 3 and len(cat) <= 10:
                # redistribute
                pass
            elif pclass == 6 and len(cat) <= 7:
                # redistribute
                pass
            elif pclass == 10 and len(cat) <= 4:
                # redistribute
                pass

            # algorithm here:

            # pool = [class, key (maturity_date, loan_term), curr_balance, curr_states_set, loans_in_pool)]

            pool = [pclass, k, 0, dict(), []]
            for loan in v:
                # print(loan)

                # pool size check
                if pool[2] + loan[1] <= max_size[pclass-1]:
                    # state % check 
                    if (pool[3].get(loan[-2], 0) + 1) / len(pool[4]) <= state_pct[pclass-1]:
                        pool[2] += loan[1]
                        pool[3][loan[-2]] = pool[3].get(loan[-2], 0) + 1
                        pool[4].append(loan)
                    else:
                        # redistribute
                        pass
                
                else:
                    # redistribute
                    pass


    # optimize categories:
    # flag = False
    # while not flag:
    #     updated = False
    #     for k in categories.keys():

    #         pclass = k.split('-')[0]

    #         # max 5%
    #         if (pclass == 1 or pclass == 2 or pclass == 4 or pclass == 5 or pclass == 7 or pclass == 8 or pclass == 9) and len(categories[k]) >= 20:
    #             pass
    #         elif pclass == 3 and len(categories[k]) >= 10:
    #             pass
    #         elif pclass == 6 and len(categories[k]) >= 7:
    #             pass
    #         elif pclass == 10 and len(categories[k]) >= 4:
    #             pass

    #         updated = True

    #         for loan in categories[k]:
    #             # redistribute the loan
    #             classes = loan[-1].split(',')
    #             key = f"{str(classes[0])}-{str(int(row['maturity_date']))}-{str(row['loan_term'])}"

    #     if updated:
    #         flag = True

    # DEBUG: prints
    # print(categories)
    # for k in categories.keys():
    #     print(f"{k}: {len(categories[k])}")

    # print(df.head())


if __name__ == '__main__':
    # only run once. (comment out when not in use)
    # gen_datastructure()
    # knapsack()
