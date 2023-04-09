import pandas as pd
import csv

df = pd.read_csv('../fnma-dataset-complete.txt', sep='|')

class_one = df.query("640 <= combined_fico <= 745 and 5.0 <= note_rate <= 7.0 and 45 <= dti <= 50 and 75 <= ltv <=85")

one_group = class_one.groupby(['maturity_date', 'loan_term'])

possible_pools = []

for name, group in one_group:
    if len(group) >= 20:
        maturity_date, loan_term = name
        possible_pools.append((maturity_date, loan_term))

results = []

for md, lt in possible_pools:
    res = class_one.query(f"maturity_date == {md} and loan_term == {lt}")
    if len(res["state"].unique()) > 20:
        results.append(res)

test = results[0]

pool = []
balance = 0
states = set()
for idx, loan in test.iterrows():
    if loan["state"] not in states:
        print(loan["sta"])
        pool.append(loan)
        states.add(loan["state"])
        balance += loan["upb"]

print(pool)
print(balance)
print(len(states))

with open("pool1.txt", "w") as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerow(["loan_id", "upb", "note_rate", "borrower_fico", "coborrower_fico",
                    "combined_fico", "state", "dti", "ltv", "maturity_date", "loan_term", "property_type"])
    writer.writerows(pool)