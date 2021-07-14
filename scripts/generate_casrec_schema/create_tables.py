import os
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option('display.max_colwidth', -1)

dir = "file_per_table"
sql_out = open("create_tables.sql", "w")
schema_name = "reference"

statement_start = (
    f"DROP SCHEMA IF EXISTS {schema_name} CASCADE; \n\n CREATE SCHEMA"
    f" {schema_name}; \n\n"
)

sql_out.write(statement_start)

for file in os.listdir(dir):
    table_name = file.split(".")[0]

    statement = f"CREATE TABLE {schema_name}.{table_name} ( \r\n"

    create_rows = pd.read_csv(os.path.join(dir, file))
    create_rows = create_rows[create_rows["Column Heading"].notna()]
    c = create_rows.groupby(["Column Heading"]).cumcount()
    c = c.replace(0, "").replace(1, ".1").astype(str)

    create_rows["Column Heading"] += c

    for i, row in create_rows.iterrows():
        column_name = row[0]
        datatype = row[8]

        column_row = f'    "{column_name}" {datatype}'

        # print(f"i: {i}")
        # print(len(create_rows))
        if i + 1 < len(create_rows):
            column_row += ", \r\n"
        else:
            column_row += "\r\n"

        statement += column_row

    statement += "); \r\n \r\n"

    # print(statement)

    sql_out.write(statement)

sql_out.close()
