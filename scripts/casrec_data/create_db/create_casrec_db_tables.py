import os
import pandas as pd

anon_data_dir = "../../anon_data"
sql_out = open("create_tables.sql", "w")

for file in os.listdir(anon_data_dir):

    file_name = file.split(".")[0]

    df = pd.read_csv(os.path.join(anon_data_dir, file))
    df_renamed = df.rename(columns={"Unnamed: 0": "Record"})

    columns = [x for x in df_renamed.columns.values]

    statement = f'CREATE TABLE "{file_name}" ('
    for i, col in enumerate(columns):
        statement += f'"{col}" text'
        if i + 1 < len(columns):
            statement += ","

    statement += "); \n\n\n"
    sql_out.write(statement)

sql_out.close()
