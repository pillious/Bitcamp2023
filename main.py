import json
import csv
import pandas as pd
import numpy as np

MULTIPLIER = 1000000

file_idx = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


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


def find_max_pos(batches, threshold=None):
    # print(batches)
    pos = (0, 0)

    for r in range(len(batches)):
        for c in range(len(batches[r])):
            if batches[r][c][1] > batches[pos[0]][pos[1]][1] and threshold and batches[r][c][1] < threshold:
                r = r
                c = c

    return pos


def knapsack():
    global file_idx

    categories = {}

    pools = []

    max_size = [20, 20, 20, 20, 20, 30, 30, 40, 40, 40]
    min_state = [20, 20, 10, 20, 20, 7, 20, 20, 20, 4]
    state_pct = [0.05, 0.05, 0.1, 0.05, 0.05, 0.15, 0.05, 0.05, 0.05, 0.25]

    # with open('smalltest-copy copy copy.json', 'r') as file:
    with open('categories.json', 'r') as file:
        categories = json.load(file)

    for pclass in range(1, 11):
        for k, v in list(categories[str(pclass)].items()):
            for loan in v:
                if loan[-2].isdigit():
                    loan.pop(-2)

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
                            categories[clses[0]][k].append(loan)

                # Remove the category from the original pool class
                del categories[str(pclass)][k]
                continue
            elif pclass == 10 and len(v) <= 4:
                # not possible to redistribute anymore, just remove from original pool class
                del categories[str(pclass)][k]
                continue
            # algorithm here:
            # pool = [class, key (maturity_date, loan_term), curr_balance, curr_states_set, loans_in_pool)]

            pool = [pclass, k, 0, dict(), []]
            # sset = set()

            # TODO: make it work for all pools
            if len(v) < min_state[pclass-1]:
                continue

            states = {}  # dict from state to list of loans

            # For a loan in a category, v, of (classes, maturity_date, and loan_term)

            # state => MD: ([used loans], [unused loans])
            for loan in v:
                if states.get(loan[6]) is None:
                    states[loan[6]] = ([], [loan])
                else:
                    states[loan[6]][1].append(loan)

            # Sort the loans in each state's unused loans
            for _, tup in states.items():
                tup[1].sort(key=lambda x: x[1], reverse=True)

            #
            # start new algorithm:
            #

            # if # states < threhold -> skip
            if len(states.keys()) < min_state[pclass-1]:
                continue

            # make first batch (will work for sure b/c of if above)
            batches = [[[]]]
            batch_bals = [0]
            for _, tup in states.items():
                if len(tup[1]) > 0:
                    first = tup[1].pop(0)
                    tup[0].append(first)
                    batches[-1][0].append(first)
                    batch_bals[0] += first[1]

            # check if batch < max_size
            while batch_bals[-1] < max_size[pclass-1] * MULTIPLIER:
                # Initialize new batch
                prev = batches[-1]
                prev.append([])
                batches.append(prev)
                batch_bals.append(batch_bals[-1])  # initializes to prev balance

                # add another batch
                for _, tup in states.items():
                    if len(tup[1]) > 0:
                        first = tup[1].pop(0)
                        tup[0].append(first)
                        batches[-1][-1].append(first)
                        batch_bals[-1] += first[1]

                # checks new batch state percentage is still valid (exit case)
                if len(batches[-1][-2]) == min_state[pclass-1] and len(batches[-1][-1]) < min_state[pclass-1]:
                    # batch[-2] is the solution
                    batch_bals.pop()
                    if len(batches[-1][-1]) > 0:
                        batches[-1][-1].pop()  # just left with batches[:-2]
                    else:
                        batches[-1].pop()
                    break

                if len(batches[-1][-1]) == 0:  # (exit case)
                    batch_bals.pop()
                    batches[-1].pop()
                    break

            # Replacement alg if balance greater than threshold
            prev_max = float('inf')
            num_states = len(batches[0])
            tested_states = 0
            while batch_bals[-1] > max_size[pclass-1] * MULTIPLIER and tested_states < num_states:
                # find max of maxs
                max_r, max_c = find_max_pos(batches[-1], prev_max)
                max_state = batches[-1][max_r][max_c][6]
                prev_max = batches[-1][max_r][max_c][1]

                #  replace max value with next best
                if len(states[max_state][1]) > 0:
                    temp = batches[-1][max_r][max_c]
                    batches[-1][max_r][max_c] = states[max_state][1][0]
                    states[max_state][1][0] = temp
                    # update balance
                    batch_bals[-1] += batches[-1][max_r][max_c][1] - temp[1]

                tested_states += 1

            # Removal alg if balance still greater than threshold
            prev_max = float('inf')
            while batch_bals[-1] > max_size[pclass-1] * MULTIPLIER:
                # find max of maxs
                max_r, max_c = find_max_pos(batches[-1], prev_max)
                max_state = batches[-1][max_r][max_c][6]
                states[max_state][1].insert(0, batches[-1][max_r][max_c])
                prev_max = batches[-1][max_r][max_c][1]
                # update balance
                batch_bals[-1] -= batches[-1][max_r][max_c][1]
                #  remove max value
                batches[-1][max_r].pop(max_c)

            # check if soln still adheres to state percentage requirement
            num_loans = 0
            for batch in batches[-1]:
                num_loans += len(batch)

            for _, tup in states.items():
                if len(tup[0])/num_loans > state_pct[pclass-1]:
                    # state percentage req not met, revert to previous batch/soln
                    batches.pop()
                    break

            #
            # End new algorithm
            #

            soln = []
            for b in batches[-1]:
                soln += b
            pool[-1] = soln
            pools.append(pool)

    # follow output guidelines
    for pool in pools:
        count = file_idx[pool[0]-1]
        file_idx[pool[0]-1] += 1
        with open(f"output/pool-{pool[0]}-{count}.txt", "w", encoding="UTF-8") as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(["loan_id", "upb", "note_rate", "borrower_fico", "coborrower_fico",
                            "combined_fico", "state", "dti", "ltv", "maturity_date", "loan_term", "property_type"])
            for i, l in enumerate(pool[4]):
                pool[4][i] = l[:12]
            writer.writerows(pool[4])


if __name__ == '__main__':
    # only run once. (comment out when not in use)
    # gen_datastructure()
    knapsack()
