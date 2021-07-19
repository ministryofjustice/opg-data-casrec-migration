import logging
import psycopg2
import os
import sys
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../../shared")
from helpers import format_error_message
from decorators import timer

log = logging.getLogger("root")


@timer
def match_existing_data(db_config, table_details):
    log.info("Matching existing data")
    """
    This is currently for CLIENTS only
    """
    default_indicator = "INSERT"
    match_indicator = "UPDATE"
    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    existing_records = get_records_to_match(
        schema=db_config["sirius_schema"],
        connection_string=db_config["sirius_db_connection_string"],
    )
    new_records = get_records_to_match(
        schema=db_config["source_schema"],
        connection_string=db_config["db_connection_string"],
        ignore_migrated_records=True,
    )
    matching_records = [x for x in new_records if x in existing_records]
    log.debug(f"Found {len(matching_records)} matching records")
    if len(matching_records) < len(new_records):
        log.error(
            f"All records should match, we're missing {len(new_records) - len(matching_records)} matches"
        )

    for table in table_details:
        log.debug(f"Setting method on {table} to default_value: '{default_indicator}'")
        query = f"""
            UPDATE {db_config['target_schema']}.{table}
            SET method = '{default_indicator}';
        """
        if table == "persons":
            log.debug(
                f"Setting method on {table} to match_indicator where casrecnumber in : {matching_records}"
            )
            if len(matching_records) > 0:
                query += f"""
                        UPDATE {db_config['target_schema']}.{table}
                        SET method = '{match_indicator}'
                        WHERE caserecnumber in ({', '.join([f"'{x}'" for x in matching_records])});
                    """

        try:
            cursor.execute(query)
        except Exception as e:
            log.error(f"There was an error: {e}", extra=format_error_message(e=e))

    cursor.close()
    conn.commit()


def get_records_to_match(schema, connection_string, ignore_migrated_records=False):

    query = f"""
        select caserecnumber from {schema}.persons where type = 'actor_client'
    """
    if not ignore_migrated_records:
        query += """
            and coalesce(clientsource, 'no data') != 'CASRECMIGRATION'
        """

    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    records_list = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        records_list = [x[0] for x in result]
    except Exception as e:
        log.error(e)

    return records_list
