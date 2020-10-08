import pandas as pd
import re

class SourceData():

    def generate_select_string(self, mapping, source_table_name, limit=None):
        cols = mapping[mapping['casrec_column_name'].notna()]

        cols = cols[cols['casrec_table'].str.lower() == source_table_name][[
            'casrec_column_name', 'alias']]

        col_names_with_alias = cols.to_dict(orient="records")

        statement = "SELECT "
        for i, col in enumerate(col_names_with_alias):
            if ',' in col['casrec_column_name']:

                statement += re.sub(r'(\w+)', r'"\1"', col['casrec_column_name'])
            else:
                statement += f"\"{col['casrec_column_name']}\" as \"{col['alias']}\""
            if i + 1 < len(col_names_with_alias):
                statement += ', '
            else:
                statement += ' '
        statement += f"FROM etl1.{source_table_name} "
        if limit:
            statement += f"LIMIT {limit}"
        return f"{statement};"

    def get_source_data(self, query, db_conn):

        df = pd.read_sql_query(query, db_conn)

        return df
