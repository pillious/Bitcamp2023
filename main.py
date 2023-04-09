import json
import csv
import pandas as pd

MULTIPLIER = 1000000

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
    # df = pd.read_csv('fnma-dataset-classified2.txt', sep='|')

    print("START ITER")
    # first pass (create initial categories)
    for _, row in df.iterrows():
        # Checks if row classes is NaN
        if pd.notna(row['classes']):
            row_list = list(row)
            classes = row['classes'].split(',')
            try:
                key = f"{str(int(row['maturity_date']))}-{str(row['loan_term'])}"

                if (len(classes) > 1):
                    row_list[-1] = ",".join(classes[1:])
                elif(len(classes) == 1):
                    row_list[-1] = ""
                else:
                    raise Exception("Invalid classes")

                if categories[classes[0]].get(key) is None:
                    categories[classes[0]][key] = [row_list]
                else:
                    categories[classes[0]][key].append(row_list)
            except:
                # occurs when maturity date is nan
                continue
    print("DONE... dumping to file...")

    with open('categories.json', 'w') as file:
        json.dump(categories, file)


def knapsack():
    categories = {}

    pools = []

    max_size = [20, 20, 20, 20, 20, 30, 30, 40, 40, 40]
    state_pct = [0.05, 0.05, 0.1, 0.05, 0.05, 0.15, 0.05, 0.05, 0.25]

    with open('categories.json', 'r') as file:
        categories = json.load(file)

    for pclass in range(1, 11):
        for k, v in list(categories[str(pclass)].items()):
            # for each v -> array of loans --> run the alg
            # if enough loans

            if (
                ((pclass == 1 or pclass == 2 or pclass == 4 or pclass ==
                 5 or pclass == 7 or pclass == 8 or pclass == 9) and len(v) < 20)
                or (pclass == 3 and len(v) < 10)
                or (pclass == 6 and len(v) < 7)
            ):
                # redistribute
                for loan in v:
                    if len(loan[-1]) > 0:
                        clses = loan[-1].split(',')
                        new_classes = ""
                        # If can redistribute loan, then redistributes
                        if len(clses) > 1:
                            new_classes = ",".join(clses[1:])
                            loan[-1] = new_classes
                        else:
                            loan[-1] = new_classes


                        # Creates new category if it doesn't exist
                        if categories[clses[0]].get(k) is None:
                            categories[clses[0]][k] = [loan]
                        # Key already exists, so add to the value list
                        else:
                            # print(clses)
                            categories[clses[0]][k].append(loan)

                # Remove the category from the original pool class
                del categories[str(pclass)][k]
                continue
            elif pclass == 10 and len(v) <= 4:
                # not possible to redistribute anymore, just remove from original pool class
                del categories[str(pclass)][k]
                continue
            else:
                # algorithm here:
                # pool = [class, key (maturity_date, loan_term), curr_balance, curr_states_set, loans_in_pool)]

                pool = [pclass, k, 0, dict(), []]
                # sset = set()

                # TODO: make it work for all pools
                if len(v) < 20:
                    continue

                states = {} # dict from state to list of loans

                # For a loan in a category, v, of (classes, maturity_date, and loan_term)
                for loan in v:
                    if states.get(loan[6]) is None:
                        states[loan[6]] = [loan]
                    else:
                        states[loan[6]].append(loan)

                min_state_loans = 100000
                if len(states.keys()) < 20:
                    continue

                for state in states.keys():
                    # sort loans by loan amount
                    states[state].sort(key=lambda x: x[1], reverse=True)
                    if len(states[state]) < min_state_loans:
                        min_state_loans = len(states[state])

                while min_state_loans > 0:
                    for state in states.keys():
                        if len(states[state]) > 0:
                            pool[2] += states[state][0][1]
                            pool[3][state] = pool[3].get(state, 0) + 1
                            pool[4].append(states[state][0])
                            states[state].pop(0)
                    min_state_loans -= 1

                # if len(pool[4]) >= 20:
                #     pools.append(pool)
                # else:
                #     print(pool[4])

                pools.append(pool)


                # pool size check
                # if pool[2] + loan[1] <= max_size[pclass-1] * MULTIPLIER:
                #     # state % check
                #     if loan[6] not in sset:
                #         sset.add(loan[6])
                #         pool[2] += loan[1]
                #         pool[3][loan[6]] = pool[3].get(loan[6], 0) + 1
                #         pool[4].append(loan)

                # else:
                #     # redistribute
                #     pass

                # else:
                #     # redistribute
                #     pass

                    # if (pool[3].get(loan[-2], 0) + 1) / len(pool[4]) <= state_pct[pclass-1]:


            # validate pool
            # if valid, append to pools
            # if not valid, redistribute or skip




    # filter out pools with 0 balance
    # soln = []
    # for pool in pools:
    #     if pool[2] > 0:
    #         soln.append(pool)

    # dump output for debugging
    # with open("solution.json", "w") as file:
    #     json.dump(soln, file)

    # follow output guidelines
    count = 0
    for pool in pools:
        # num_loans = len(pool[4])

        with open(f"output/class{pool[0]}_{count}.txt", "w", encoding="UTF-8") as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(["loan_id", "upb", "note_rate", "borrower_fico", "coborrower_fico",
                            "combined_fico", "state", "dti", "ltv", "maturity_date", "loan_term", "property_type"])
            for ele in pool[4]:
                del ele[-1]
            writer.writerows(pool[4])
        count += 1

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
    knapsack()
