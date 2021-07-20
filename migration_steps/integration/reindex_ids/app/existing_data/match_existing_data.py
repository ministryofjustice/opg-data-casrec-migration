import logging
import psycopg2
import os
import sys
from pathlib import Path

from utilities.existing_data_helpers import format_conditions, get_tables_to_match

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../../shared")
from helpers import format_error_message
from decorators import timer

log = logging.getLogger("root")


@timer
def match_existing_data(db_config, table_details):
    log.info("Matching existing data")

    tables_to_match = get_tables_to_match(table_details=table_details)

    match_indicator = "UPDATE"
    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    if len(tables_to_match) == 0:
        log.error("Nothing to match, but there should be...")

    for table, details in tables_to_match.items():
        updates = []

        matching_data = get_matching_data(
            db_config=db_config, table_name=table, table_details=details
        )

        for match_col, match_ids in matching_data.items():

            update_query = f"""
                UPDATE {db_config['target_schema']}.{table}
                SET id = {match_ids['existing_id']},
                method = '{match_indicator}',
                pk_source = 'sirius'
                WHERE id = {match_ids['migration_id']}
                AND {details['match_field']} = '{match_col}';
            """

            updates.append(update_query)

        try:
            all_updates = " ".join(updates)
            cursor.execute(all_updates)
        except Exception as e:
            log.error(f"There was an error: {e}", extra=format_error_message(e=e))

        cursor.close()
        conn.commit()


def get_matching_data(db_config, table_name, table_details):

    existing_records = get_records_to_match(
        schema=db_config["sirius_schema"],
        connection_string=db_config["sirius_db_connection_string"],
        table_name=table_name,
        table_details=table_details,
    )
    new_records = get_records_to_match(
        schema=db_config["target_schema"],
        connection_string=db_config["db_connection_string"],
        table_name=table_name,
        table_details=table_details,
    )

    matching_records = {}
    for match_field, id in new_records.items():
        if match_field in existing_records:
            matching_records[match_field] = {
                "migration_id": id,
                "existing_id": existing_records.get(match_field),
            }

    log.debug(f"Found {len(matching_records)} matching records")

    if len(matching_records) < len(new_records):
        log.error(
            f"All records should match, we're missing {len(new_records) - len(matching_records)} matches"
        )

    return matching_records


def get_records_to_match(schema, connection_string, table_name, table_details):

    query = f"""
        select id, "{table_details['match_field']}" from {schema}.{table_name}
    """
    if "conditions" in table_details:
        conditions = format_conditions(conditions=table_details.get("conditions"))
        query += conditions

    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    records = {}
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        records = {x[1]: x[0] for x in result}
    except Exception as e:
        log.error(e)
    cursor.close()
    conn.commit()
    return records
