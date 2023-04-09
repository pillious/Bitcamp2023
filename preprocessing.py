# 000128090409|171000.00|2.990|808|814|811|NY|47|48|102051|360|SF|
# convert to
# 000128090409|171000.00|2.990|808|814|811|NY|47|48|102051|360|SF|1,3,10
# note: the last column is the list of indices of the pools that the loan can fit in

# read in the pools from pools.txt
# read in the loan data from fnam-dataset-complete.txt (you can test on fnma-dataset-00.txt)

# write to an output file as you go.

# FILTER BY THESE COLUMNS
# determine pools column based on pools.txt (upper bound of pool size, FICO, DTI, LTV)

# import pandas as pd
# will likely be useful for reading data & stuff. (example of reading in data in main.py)

import pandas as pd
import csv

POOLS = None
DATA = None


def read_data():
    global POOLS
    global DATA
    print('Reading in data...')
    POOLS = pd.read_csv('pools.txt', sep='|')

    # DATA = pd.read_csv('fnma-dataset-complete.txt', sep='|')
    DATA = pd.read_csv('true.txt', sep='|')

    print('Done reading in data.')


def classify(row) -> 'str':
    '''
    given a row of data, return all classes it fits in. 
    return example: "1,3,10"
    '''

    indices = ""
    for i, pool in POOLS.iterrows():
        if (int(row[1]['upb']) <= int(pool['U_Size']) * 1000000 and 
            int(row[1]['combined_fico']) >= int(pool['L_FICO']) and 
            int(row[1]['combined_fico']) <= int(pool['U_FICO']) and 
            float(row[1]['note_rate']) >= float(pool['L_NoteRate']) and 
            float(row[1]['note_rate']) <= float(pool['U_NoteRate']) and 
            not pd.isna(row[1]['dti']) and 
            int(row[1]['dti']) >= int(pool['L_DTI']) and 
            int(row[1]['dti']) <= int(pool['U_DTI']) and 
            int(row[1]['ltv']) >= int(pool['L_LTV']) and 
            int(row[1]['ltv'] <= int(pool['U_LTV']))):
            indices += str(i+1) + ','

    return indices.rstrip(',')


def main():
    print('Begin preprocessing...')
    buffer = []
    buffer_max_rows = 250000

    with open("fnma-dataset-classified.txt", "w", encoding="UTF-8") as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerow(list(DATA.columns) + ['classes'])
        if DATA is not None:
            for row in DATA.iterrows():
                row_list = row[1].tolist()
                row_list.append(classify(row))
                buffer.append(row_list)
                if len(buffer) >= buffer_max_rows:
                    print(f"Writing {buffer_max_rows} rows to file...")
                    writer.writerows(buffer)
                    buffer = []
            if len(buffer) > 0:
                print(f"Writing {len(buffer)} rows to file...")
                writer.writerows(buffer)

    print('Done preprocessing. Output file: fnma-dataset-classified.txt')


if __name__ == '__main__':
    read_data()
    main()
