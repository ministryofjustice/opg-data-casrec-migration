import os
import time
import pandas as pd
start = time.time()


import csv
import psycopg2
conn = psycopg2.connect("host=localhost port=6666 dbname=casrec user=casrec "
                        "password=casrec")
cur = conn.cursor()

anon_data_dir = '../anon_data'

for file in os.listdir(anon_data_dir):

    file_name = file.split('.')[0]


    df = pd.read_csv(os.path.join(anon_data_dir, file))
    df_renamed = df.rename(columns ={'Unnamed: 0': "Record"})

    columns = [x for x in df_renamed.columns.values]

    statement = f"CREATE TABLE \"{file_name}\" ("
    for i, col in enumerate(columns):
        statement += f"\"{col}\" text"
        if i+1 < len(columns):
            statement += ","

    statement += "); \n\n\n"

    cur.execute(statement)


conn.commit()
