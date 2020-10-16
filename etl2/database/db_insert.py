import logging
import time
import sys


class InsertData:
    def __init__(self, db_engine, schema, is_verbose=False):
        self.db_engine = db_engine
        self.schema = schema

        if is_verbose:
            self.log_level = logging.DEBUG
        else:
            self.log_level = logging.INFO

        self.log = logging.getLogger(__name__)
        self.log.setLevel(self.log_level)

        log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.log_level)
        handler.setFormatter(log_format)
        self.log.addHandler(handler)

    def _list_table_columns(self, df):
        return [x for x in df.columns.values]

    def _create_schema_statement(self):
        statement = f"CREATE SCHEMA IF NOT EXISTS {self.schema};"
        return statement

    def _create_table_statement(self, table_name, df):
        columns = self._list_table_columns(df=df)
        create_statement = f'CREATE TABLE "{self.schema}"."{table_name}" ('
        for i, col in enumerate(columns):
            create_statement += f'"{col}" text'
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
                    .replace("nan", "")
                    .replace("&", "and")
                    .replace(";", "-")
                    .replace("%", "percent")
                )
                for x in row
            ]
            row = [f"'{str(x)}'" for x in row]
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

    def _add_missing_columns(self, table_name, col_diff):
        statement = f"ALTER TABLE {self.schema}.{table_name} "
        for i, col in enumerate(col_diff):
            statement += f'ADD COLUMN "{col}" text'
            if i + 1 < len(col_diff):
                statement += ","
        statement += ";"

        return statement

    def insert_data(self, table_name, df):

        t = time.process_time()

        self.log.info(f"inserting {table_name} into " f"database....")
        self.log.debug(df.sample(n=5).to_markdown())

        create_schema_statement = self._create_schema_statement()
        self.db_engine.execute(create_schema_statement)

        if self._check_table_exists(table_name=table_name):
            col_diff = self._check_columns_exist(table_name, df)
            if len(col_diff) > 0:
                add_missing_colums_statement = self._add_missing_columns(
                    table_name, col_diff
                )
                self.db_engine.execute(add_missing_colums_statement)
        else:
            create_table_statement = self._create_table_statement(
                table_name=table_name, df=df
            )
            self.db_engine.execute(create_table_statement)

        insert_statement = self._create_insert_statement(table_name=table_name, df=df)
        self.db_engine.execute(insert_statement)

        # inserted_count_statement = self._inserted_count_statement(table_name=table_name)
        #
        # inserted_count = self.db_engine.execute(inserted_count_statement).fetchall()[0][
        #     0
        # ]

        inserted_count = len(df)

        self.log.info(
            f"inserted {inserted_count} records into '{table_name}' "
            f"table in {round(time.process_time() - t, 2)} seconds\n==============\n\n"
        )
