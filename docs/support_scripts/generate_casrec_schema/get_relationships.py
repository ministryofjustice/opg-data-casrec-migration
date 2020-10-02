import pandas as pd
from table_definitions import map_col_names
# print(map_col_names['CFOLOAD'])


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


df = pd.read_csv("casrec_dd - Relationship.csv")
df = df[df['Target file'].notna()]

df['counter'] = (df['Target file'].astype(str).str[:11] == "Source file").cumsum()
df.groupby('counter').apply(lambda df: df.iloc[0])

sql_out = open('create_tables.sql', "a+")
schema_name = "reference"

uniques = []
fks = []

for idx, group in df.groupby(df['counter']):
    source_table = group.iloc[0]['Target file'][14:]

    # if source_table.lower() == 'deputyship':
    for i, row in group.iterrows():

        join_table = row['Target file']
        old_join_col = row['Relationship']
        # join_col = map_col_names[join_table][old_join_col]

        if "Source file" not in join_table:
            if str(":") not in str(old_join_col):
                try:
                    source_join_col = map_col_names[source_table][old_join_col]
                    join_col = map_col_names[join_table][old_join_col]


                    unique_constraint = f'ALTER TABLE {schema_name}.{source_table.lower()} ' \
                                        f'ADD CONSTRAINT unique_{source_table.lower()}_{join_col.lower().replace(" ","_")} ' \
                                        f'UNIQUE ("{source_join_col}");'
                    # print(unique_constraint)
                    uniques.append(unique_constraint)

                    statement = f'ALTER TABLE {schema_name}.{join_table.lower()} \r\n' \
                                f'    ADD CONSTRAINT fk_' \
                                f'{join_table.lower()}_{source_table.lower()} ' \
                                f'FOREIGN KEY ("{join_col}") ' \
                                f'REFERENCES {schema_name}.{source_table.lower()} ("{source_join_col}"); ' \
                                f'\r\n\r\n'

                    # print(statement)
                except:
                    pass
                fks.append(statement)
                # sql_out.write(statement)
all_unique_constraints = []
[all_unique_constraints.append(x) for x in uniques if x not in
                          all_unique_constraints]
all_fk_constraints = []
[all_fk_constraints.append(x) for x in fks if x not in
                          all_fk_constraints]


sql_out.write('\r\n'.join(all_unique_constraints))
sql_out.write('\r\n\r\n')
sql_out.write('\r\n'.join(all_fk_constraints))

sql_out.close()
