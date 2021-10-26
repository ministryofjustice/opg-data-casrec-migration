import logging
import psycopg2
import os
import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../../shared")
from utilities.existing_data_helpers import format_conditions, get_tables_to_match

from reindex.reindex_foreign_keys import update_fks
from helpers import format_error_message
from decorators import timer

log = logging.getLogger("root")


@timer
def match_existing_data(db_config, table_details):
    log.info("Matching existing data")

    tables_to_match = get_tables_to_match(table_details=table_details)

    for table, details in tables_to_match.items():

        existing_data_details = details["existing_data"]

        create_temp_table(
            db_config=db_config, table_name=table, table_details=existing_data_details
        )
        get_existing_data(
            db_config=db_config, table_name=table, table_details=existing_data_details
        )
        update_casrec_rows(
            db_config=db_config, table_name=table, table_details=existing_data_details
        )

        if unmatched_check(
            db_config=db_config, table_name=table, table_details=existing_data_details
        ):
            log.debug(f"All rows matched for table {table}")
        else:
            log.error(f"Not all rows matched for table {table}")
            # os._exit(1)

        tables_with_fk_links_to_this_table = fks(
            table_details=table_details, parent_table=table
        )

        try:
            update_fks(
                db_config=db_config,
                table_details=tables_with_fk_links_to_this_table,
                match=True,
            )
        except Exception as e:
            log.error(f"{e}")


def fks(table_details, parent_table):
    child_tables = []
    for k, v in table_details.items():
        if len(v["fks"]) > 0:
            for x in v["fks"]:
                if x["parent_table"] == parent_table:
                    child_tables.append(k)

    tables_to_reindex_fks = {x: table_details[x] for x in child_tables}
    return tables_to_reindex_fks


def create_temp_table(db_config, table_name, table_details):

    query = f"""
        CREATE TABLE IF NOT EXISTS {db_config['target_schema']}.existing_{table_name}
        (existing_id integer,
        {table_details['match_field']} text);
    """

    try:
        conn = psycopg2.connect(db_config["db_connection_string"])
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
    except Exception as e:
        log.error(e)


def get_existing_data(db_config, table_name, table_details):
    target_db_engine = create_engine(db_config["db_connection_string"])
    chunk_size = db_config["chunk_size"]
    offset = 0

    while True:

        query = f"""
            select id, "{table_details['match_field']}" from {db_config['sirius_schema']}.{table_name}
        """
        if "conditions" in table_details:
            conditions = format_conditions(conditions=table_details.get("conditions"))
            query += conditions
        query += f" ORDER BY id LIMIT {chunk_size} OFFSET {offset};"

        existing_data = pd.read_sql_query(
            sql=query, con=db_config["sirius_db_connection_string"]
        )

        if len(existing_data.index) == 0:
            log.debug(f"empty offset {offset} for table {table_name}")
            break

        insert_statement = create_insert_into_temp_table(
            db_config=db_config,
            df=existing_data,
            table_name=table_name,
            table_details=table_details,
        )

        try:
            target_db_engine.execute(insert_statement)
        except Exception as e:
            log.error(e)
            log.error(
                f"There was an error inserting {len(existing_data)} rows "
                f"into {db_config['target_schema']}.{table_name}",
                extra={
                    "table_name": table_name,
                    "size": len(existing_data),
                    "action": "insert",
                    "error": format_error_message(e=e),
                },
            )
            os._exit(1)

        offset += chunk_size
        log.debug(f"doing offset {offset} for table {table_name}")
        if len(existing_data) < chunk_size:
            break


def create_insert_into_temp_table(db_config, df, table_name, table_details):

    statement = f"""
        INSERT INTO {db_config['target_schema']}.existing_{table_name} (existing_id, {table_details['match_field']}) VALUES
    """
    for i, row in enumerate(df.values.tolist()):
        single_row = f"({row[0]}, '{row[1]}')"
        if i + 1 < len(df):
            single_row += ", "
        else:
            single_row += "; "

        statement += single_row

    return statement


def update_casrec_rows(db_config, table_name, table_details):
    target_db_engine = create_engine(db_config["db_connection_string"])

    statement = f"""
        UPDATE {db_config['target_schema']}.{table_name}
        SET id = existing_id, migration_method='UPDATE'
        FROM {db_config['target_schema']}.existing_{table_name}
        WHERE {table_name}.{table_details['match_field']} = existing_{table_name}.{table_details['match_field']};

    """

    try:
        target_db_engine.execute(statement)
    except Exception as e:
        log.error(
            f"There was an error updating existing data from existing_{table_name} to {table_name} using {table_details['match_field']}",
            extra={
                "table_name": table_name,
                "error": format_error_message(e=e),
            },
        )
        os._exit(1)


def get_unmatched_rows(db_config, table_name, table_details):
    target_db_engine = create_engine(db_config["db_connection_string"])

    query = f"""
        SELECT count(*), migration_method FROM {db_config['target_schema']}.{table_name}
    """
    if "conditions" in table_details:
        conditions = format_conditions(conditions=table_details.get("conditions"))
        query += conditions

    query += f""" GROUP BY migration_method;"""

    try:
        result = target_db_engine.execute(query).fetchall()
        return result
    except Exception as e:
        log.error(e)


def unmatched_check(db_config, table_name, table_details):

    unmatched_rows = get_unmatched_rows(
        db_config=db_config, table_name=table_name, table_details=table_details
    )

    stats = {}
    for x in unmatched_rows:
        stats[x[1]] = x[0]
    try:
        if stats["INSERT"] > 0:
            log.error(f"matched {stats['UPDATE']}, unmatched {stats['INSERT']}")
            return False
        else:
            return True
    except KeyError:
        return True
