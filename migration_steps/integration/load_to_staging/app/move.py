import json
import os
import sys
import logging

import psycopg2
from psycopg2 import errors

log = logging.getLogger("root")


completed_tables = []


def get_columns_query(table, schema):
    return f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_name = '{table}';
        """


def add_missing_columns_query(table, schema, columns):

    query = f"ALTER TABLE {schema}.{table} "
    for i, col in enumerate(columns):
        query += f"ADD COLUMN IF NOT EXISTS {col} TEXT"
        if i + 1 < len(columns):
            query += ", "
    query += ";"

    return query


def create_missing_extra_tables(db_config, db_engine, extra_tables):
    tables_to_create = [v["sirius_target_table"] for k, v in extra_tables.items()]

    for table in tables_to_create:
        query = f"""
            CREATE TABLE IF NOT EXISTS {db_config['target_schema']}.{table} (
            id serial primary key,
            entity varchar(255),
            details json,
            sirius_table text,
            sirius_pk_column text,
            sirius_pk_value int
               );
        """

        try:
            with db_engine.begin() as conn:
                log.debug(
                    f"Creating extra table {table} in {db_config['target_schema']}"
                )
                conn.execute(query)

        except Exception as e:
            log.error(
                f"There was an error creating {table} in {db_config['target_schema']}"
            )
            log.debug(e)
            os._exit(1)


def generate_inserts(
    db_config, db_engine, tables, extra_tables=None, tables_copied_from_sirius=None
):

    if extra_tables:
        create_missing_extra_tables(
            db_config=db_config, db_engine=db_engine, extra_tables=extra_tables
        )
    else:
        extra_tables = {}

    if not tables_copied_from_sirius:
        tables_copied_from_sirius = {}

    tables_list = {**tables_copied_from_sirius, **tables, **extra_tables}

    extra_cols_to_move_to_staging = ["migration_method", "casrec_details"]

    for i, (table, details) in enumerate(tables_list.items()):
        try:
            destination_table = details["sirius_target_table"]
            source_table = table
        except KeyError:
            source_table = table
            destination_table = table

        log.info(f"Inserting {source_table} into {db_config['target_schema']}")

        log.debug(f"This is table number {i+1}")

        get_source_cols_query = get_columns_query(
            table=source_table, schema=db_config["source_schema"]
        )
        get_target_cols_query = get_columns_query(
            table=destination_table, schema=db_config["target_schema"]
        )

        source_columns = [
            x[0] for x in db_engine.execute(get_source_cols_query).fetchall()
        ]
        target_columns = [
            x[0] for x in db_engine.execute(get_target_cols_query).fetchall()
        ]
        extra_columns = (
            extra_cols_to_move_to_staging
            if table not in tables_copied_from_sirius.keys()
            else []
        )

        cols_to_move = list(
            set([x for x in source_columns if x in target_columns] + extra_columns)
        )

        if len(extra_columns) > 0:
            alter_target_query = add_missing_columns_query(
                table=destination_table,
                schema=db_config["target_schema"],
                columns=extra_columns,
            )

            db_engine.execute(alter_target_query)

        query = f"""
        INSERT INTO {db_config["target_schema"]}.{destination_table} ({', '.join(cols_to_move)})
        SELECT {', '.join(cols_to_move)} FROM {db_config["source_schema"]}.{source_table};
        """

        try:
            with db_engine.begin() as conn:
                conn.execute(query)

            global completed_tables
            completed_tables.append(source_table)
            log.info(
                f"{len(completed_tables)}/{len(tables_list)} tables have been completed"
            )
            log.debug(f"Completed tables: {', '.join(completed_tables)}")
            log.debug(
                f"Not completed tables: {', '.join(list(set(tables_list) - set(completed_tables)))}"
            )
        except Exception as e:
            print(e)
            log.error(
                f"There was an error inserting {source_table} into {db_config['target_schema']}"
            )
            log.debug(e)
            os._exit(1)
