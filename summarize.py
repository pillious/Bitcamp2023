# import pandas as pd

# df = pd.read_csv('fnma-dataset-classified.txt', sep='|')

# ohe = []
# for _, row in df.iterrows():
#     if (not pd.isna(row['classes'])):
#         pool_classes = row['classes'].split(',')
#         int_arr = [int(p) for p in pool_classes]
#         row = []
#         for i in range(10):
#             if i in int_arr:
#                 row.append(1)
#             else:
#                 row.append(0)
#         ohe.append(row)

# cols = ['pool_1', 'pool_2', 'pool_3', 'pool_4', 'pool_5', 'pool_6', 'pool_7', 'pool_8', 'pool_9', 'pool_10']
# ohe_df = pd.DataFrame(ohe, columns=cols)

# print(ohe_df.head())
# for col in cols:
#     print(ohe_df[col].value_counts())

# # -----------------------------

# # import os

# # for filename in os.listdir(os.getcwd() + "/output"):
# #     df = pd.read_csv(os.path.join("output/" + filename), sep='|')
# #     if len(df.index) > 5:
# #         print(f"{len(df)} {filename}")