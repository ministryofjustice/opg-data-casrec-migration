import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
import pandas as pd
import time
import sqlalchemy
from db_helpers import create_schema
from table_helpers import get_pk

environment = os.environ.get("ENVIRONMENT")
import helpers

config = helpers.get_config(env=environment)


def copy_table(
    engine_from, engine_to, schema_from, schema_to, table_from, table_to, pk, log
):
    log.info(f"Copying {table_from}")
    chunk_size = config.DEFAULT_CHUNK_SIZE
    offset = 0
    while True:
        select_table_statement = f"""
                SELECT *
                FROM {schema_from}.{table_from}
                ORDER BY {pk}
                LIMIT {chunk_size} OFFSET {offset}
                """

        df = pd.read_sql(select_table_statement, engine_from)
        df.to_sql(
            name=table_to,
            schema=schema_to,
            con=engine_to,
            if_exists="replace",
            index=False,
            dtype={col_name: sqlalchemy.types.TEXT for col_name in df},
        )

        log.info(f"Copied {offset + len(df)} rows")
        offset += int(chunk_size)
        if len(df) < int(chunk_size):
            break


def get_update_rows_statement(audit_value, schema, table, pk, log):
    if audit_value == "current":
        new_audit_value = "new"
    elif audit_value == "previous":
        new_audit_value = "deleted"
    else:
        log.error("Incorrect audit value")
        exit(1)

    update_rows_statement = f"""
        update {schema}.{table} set audit_value = '{new_audit_value}'
        where {pk} in
        (select mt.{pk}
        from {schema}.{table} mt
        inner join
        (select {pk}, count(*)
        from {schema}.{table}
        group by {pk}
        having count(*) = 1) as st
        on mt.{pk} = st.{pk}
        where mt.audit_value = '{audit_value}')
    """
    return update_rows_statement


def get_change_statement(schema, table, from_src):
    select_change = f"""
        SELECT *
        FROM {schema}.{table}_{'before' if from_src else 'after'}
        EXCEPT
        SELECT *
        FROM {schema}.{table}_{'after' if from_src else 'before'};
        """
    return select_change


def diff_old_new(engine, schema, table, pk, log):
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    df_from = pd.read_sql(get_change_statement(schema, table, True), engine)
    df_from.insert(loc=0, column="audit_value", value="previous")
    df_from.insert(loc=0, column="mig_timestamp", value=ts)

    df_to = pd.read_sql(get_change_statement(schema, table, False), engine)
    df_to.insert(loc=0, column="audit_value", value="current")
    df_to.insert(loc=0, column="mig_timestamp", value=ts)

    df_combined = df_from.append(df_to)
    df_combined.to_sql(
        name=table,
        schema=schema,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=10000,
    )

    response = engine.execute(
        get_update_rows_statement("previous", schema, table, pk, log)
    )
    if response.rowcount > 0:
        log.info(f"Audit - Updated {table} statuses for deleted rows")
    response = engine.execute(
        get_update_rows_statement("current", schema, table, pk, log)
    )
    if response.rowcount > 0:
        log.info(f"Audit - Updated {table} statuses for new rows")


def clear_up(engine, schema, table, log):
    for direction in ["before", "after"]:
        drop_statement = f"DROP TABLE {schema}.{table}_{direction}"
        response = engine.execute(drop_statement)
        if response.rowcount > 0:
            log.debug(f"Dropped {schema}.{table}_{direction}")


def run_audit(sirius_engine, casrec_engine, command, log, tables_list):
    casrec_schema = "audit"
    sirius_schema = "public"
    create_schema(log, casrec_engine, casrec_schema)

    if command == "before":
        for table in tables_list:
            pk = get_pk(sirius_engine, sirius_schema, table)
            copy_table(
                sirius_engine,
                casrec_engine,
                sirius_schema,
                casrec_schema,
                table,
                f"{table}_before",
                pk,
                log,
            )
            log.info(f"Audit - Copied {table} before update to {table}_before")
    elif command == "after":
        for table in tables_list:
            pk = get_pk(sirius_engine, sirius_schema, table)
            copy_table(
                sirius_engine,
                casrec_engine,
                sirius_schema,
                casrec_schema,
                table,
                f"{table}_after",
                pk,
                log,
            )
            log.info(f"Audit - Copied {table} after update to {table}_after")
            diff_old_new(casrec_engine, casrec_schema, table, pk, log)
            clear_up(casrec_engine, casrec_schema, table, log)
    else:
        log.error(f"ERROR Invalid command")
        exit(1)
