import os

import psycopg2

conn = psycopg2.connect(
    "host=localhost port=6666 dbname=casrec user=casrec " "password=casrec"
)
cur = conn.cursor()

anon_data_dir = "../../anon_data"

for file in os.listdir(anon_data_dir):

    file_name = file.split(".")[0]

    with open(os.path.join(anon_data_dir, file), "r") as f:

        next(f)
        cur.copy_from(f, f'"{file_name}"', sep=",")

    conn.commit()
