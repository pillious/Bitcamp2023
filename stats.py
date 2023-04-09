import json
import pandas as pd
import csv

df = pd.read_csv('fnma-dataset-classified.txt', sep='|')

print(df.head())

print(len(df.query("640 <= combined_fico <= 745 and 5.0 <= note_rate <= 7.0 and 45 <= dti <= 50 and 75 <= ltv <=85")))
# print(df[(df.note_rate >= 5) & (df.note_rate <= 7) & (df.combined_fico >= 640) & (df.combined_fico)])

# df[df]
