from typing import Dict

import psycopg2
import sys
import os
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from decorators import timer
import logging
import time
import helpers
import pandas as pd

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


class InsertData:
    def __init__(self, db_engine, schema):
        self.db_engine = db_engine
        self.schema = schema
        self.datatype_remap = {
            "str": "text",
            "date": "date",
            "datetime": "date",
            "dict": "json",
        }

    def _list_table_columns(self, df):
        return [x for x in df.columns.values]

    def _create_schema_statement(self):
        statement = f"CREATE SCHEMA IF NOT EXISTS {self.schema};"
        return statement

    @timer
    def _create_table_statement_with_datatype(
        self, df: pd.DataFrame, mapping_details: Dict, table_name: str
    ) -> str:
        log.debug(f"Generating table create statement for {table_name}")
        statement = f"CREATE TABLE IF NOT EXISTS {self.schema}.{table_name} (\n"

        columns = []
        for col, details in mapping_details.items():
            details["data_type"] = (
                self.datatype_remap[details["data_type"].lower()]
                if details["data_type"] in self.datatype_remap
                else details["data_type"]
            )
            columns.append(f"{col} {details['data_type']}")

        columns_from_df = self._list_table_columns(df=df)
        columns_from_mapping = mapping_details.keys()
        temp_colums = list(set(columns_from_df) - set(columns_from_mapping))
        for col in temp_colums:
            columns.append(f"{col} text")

        statement += ", ".join(columns)

        statement += ");"
        log.log(config.VERBOSE, f"Table create statement: {statement}")
        return statement

    def _create_table_statement(self, table_name, df):
        columns = self._list_table_columns(df=df)
        create_statement = f'CREATE TABLE "{self.schema}"."{table_name}" ('
        for i, col in enumerate(columns):
            if col == "id":
                datatype = "int"
            else:
                datatype = "text"
            create_statement += f'"{col}" {datatype}'
            if i + 1 < len(columns):
                create_statement += ","
        create_statement += ");"

        return create_statement

    def _truncate_table_statement(self, table_name):
        return f'TRUNCATE TABLE "{self.schema}"."{table_name}"'

    def _check_table_exists_statement(self, table_name):
        return f"""
        SELECT EXISTS (
           SELECT FROM information_schema.tables
           WHERE  table_schema = '{self.schema}'
           AND    table_name   = '{table_name}'
        );
        """

    def _check_table_exists(self, table_name):

        check_table_exists_statement = self._check_table_exists_statement(
            table_name=table_name
        )
        check_exists_result = self.db_engine.execute(check_table_exists_statement)

        for r in check_exists_result:
            table_exists = r.values()[0]

            return table_exists

    def _create_insert_statement(self, table_name, df):
        columns = self._list_table_columns(df=df)
        insert_statement = f'INSERT INTO "{self.schema}"."{table_name}" ('
        for i, col in enumerate(columns):
            insert_statement += f'"{col}"'
            if i + 1 < len(columns):
                insert_statement += ","

        insert_statement += ") \n VALUES \n"

        for i, row in enumerate(df.values.tolist()):

            row = [str(x) for x in row]
            row = [
                str(
                    x.replace("'", "''")
                    .replace("NaT", "")
                    .replace("nan", "")
                    .replace("<NA>", "")
                    .replace("&", "and")
                    .replace(";", "-")
                    .replace("%", "percent")
                )
                for x in row
            ]
            row = [f"'{str(x)}'" if str(x) != "" else "NULL" for x in row]

            single_row = ", ".join(row)

            insert_statement += f"({single_row})"

            if i + 1 < len(df):
                insert_statement += ",\n"
            else:
                insert_statement += ";\n\n\n"
        return insert_statement

    def _inserted_count_statement(self, table_name):
        return f"select count(*) from {self.schema}.{table_name};"

    def _check_columns_exist(self, table_name, df):
        columns = self._list_table_columns(df=df)

        existing_cols_statement = (
            f"SELECT column_name FROM "
            f"information_schema.columns "
            f"WHERE  table_schema = '{self.schema}'"
            f"AND    table_name   = '{table_name}';"
        )

        existing_cols = self.db_engine.execute(existing_cols_statement)
        existing_cols_list = [row[0] for row in existing_cols]

        col_diff = [i for i in columns if i not in existing_cols_list]

        return col_diff

    def _add_missing_columns_with_datatypes(
        self, table_name, col_diff, mapping_details
    ):

        statement = f"ALTER TABLE {self.schema}.{table_name} "
        for i, col in enumerate(col_diff):
            if col[:2] == "c_":
                data_type = "text"
            else:

                data_type = (
                    self.datatype_remap[mapping_details[col]["data_type"]]
                    if mapping_details[col]["data_type"] in self.datatype_remap
                    else mapping_details[col]["data_type"]
                )
            statement += f'ADD COLUMN "{col}" {data_type}'
            if i + 1 < len(col_diff):
                statement += ","
        statement += ";"
        return statement

    def _add_missing_columns(self, table_name, col_diff):
        statement = f"ALTER TABLE {self.schema}.{table_name} "
        for i, col in enumerate(col_diff):
            statement += f'ADD COLUMN "{col}" text'
            if i + 1 < len(col_diff):
                statement += ","
        statement += ";"

        return statement

    def _check_datatypes(self, mapping_details, df):

        pandas_to_db_map = {
            "text": ["object"],
            "int": ["Int64", "Int32"],
            "numeric": ["float64"],
        }

        for column_name, df_datatype in df.dtypes.items():

            try:
                expected_datatype = mapping_details[column_name]["data_type"]
                if df_datatype in pandas_to_db_map[expected_datatype]:
                    match = True
                else:
                    log.debug(
                        f"column '{column_name}' should be '{expected_datatype}' but is actually '{df_datatype}'"
                    )
                    match = False
            except KeyError:
                pass

        return match

    @timer
    def insert_data(self, table_name, df, sirius_details=None, chunk_no=None):

        if chunk_no:
            log.debug(f"inserting {table_name} - chunk {chunk_no} into database....")
        else:
            log.debug(f"inserting {table_name} into database....")
        log.log(config.DATA, f"\n{df.sample(n=config.row_limit).to_markdown()}")

        create_schema_statement = self._create_schema_statement()
        self.db_engine.execute(create_schema_statement)

        if self._check_table_exists(table_name=table_name):
            col_diff = self._check_columns_exist(table_name, df)
            if len(col_diff) > 0:

                add_missing_colums_statement = self._add_missing_columns_with_datatypes(
                    table_name, col_diff, mapping_details=sirius_details
                )

                self.db_engine.execute(add_missing_colums_statement)
        else:

            create_table_statement = self._create_table_statement_with_datatype(
                table_name=table_name, mapping_details=sirius_details, df=df
            )
            self.db_engine.execute(create_table_statement)

        insert_statement = self._create_insert_statement(table_name=table_name, df=df)
        if self._check_datatypes(mapping_details=sirius_details, df=df):
            try:
                self.db_engine.execute(insert_statement)
            except Exception:
                log.error(f"There was a problem inserting into {table_name}")
                os._exit(1)
            inserted_count = len(df)

            log.info(f"Inserted {inserted_count} records into '{table_name}' table")

        else:
            log.error(f"Datatypes do not match for table {table_name}")
            os._exit(1)
