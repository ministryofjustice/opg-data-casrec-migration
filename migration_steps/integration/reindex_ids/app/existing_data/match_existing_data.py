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

    # create_matches(db_config)

    tables_to_match = get_tables_to_match(table_details=table_details)

    match_indicator = "UPDATE"
    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    for table, details in tables_to_match.items():

        existing_records = get_records_to_match(
            schema=db_config["sirius_schema"],
            connection_string=db_config["sirius_db_connection_string"],
            table_name=table,
            table_details=details,
        )
        new_records = get_records_to_match(
            schema=db_config["source_schema"],
            connection_string=db_config["db_connection_string"],
            table_name=table,
            table_details=details,
        )
        matching_records = [x for x in new_records if x in existing_records]
        log.debug(f"Found {len(matching_records)} matching records")

        if len(matching_records) < len(new_records):
            log.error(
                f"All records should match, we're missing {len(new_records) - len(matching_records)} matches"
            )

        log.debug(
            f"Setting method on {table} to {match_indicator} where {details['match_field']} on {len(matching_records)} records"
        )
        if len(matching_records) > 0:
            query = f"""
                    UPDATE {db_config['target_schema']}.{table}
                    SET method = '{match_indicator}'
                    WHERE {details['match_field']} in ({', '.join([f"'{x}'" for x in matching_records])});
                """

            try:
                cursor.execute(query)
            except Exception as e:
                log.error(f"There was an error: {e}", extra=format_error_message(e=e))

    cursor.close()
    conn.commit()


def get_tables_to_match(table_details):
    return {
        k: v["existing_data"] for k, v in table_details.items() if "existing_data" in v
    }


def format_conditions(conditions):
    conditions_list = []

    for condition in conditions:
        if condition["condition_type"] == "equal":
            conditions_list.append(f"{condition['field']} = '{condition['value']}'")

    result = ""
    for i, condition in enumerate(conditions_list):
        if i == 0:
            result += f" WHERE {condition}"
        else:
            result += f" AND {condition}"

    return result


def get_records_to_match(schema, connection_string, table_name, table_details):

    query = f"""
        select "{table_details['match_field']}" from {schema}.{table_name}
    """
    if "conditions" in table_details:
        conditions = format_conditions(conditions=table_details.get("conditions"))
        query += conditions

    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    records_list = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        records_list = [x[0] for x in result]
    except Exception as e:
        log.error(e)
    cursor.close()
    conn.commit()
    return records_list


def create_matches(db_config):
    """
    THIS IS TEMP FOR TESTING ONLY!!!!
    """

    log.warning("Creating fake match data FOR TESTING ONLY")

    import random

    existing_records = get_records_to_match(
        schema=db_config["sirius_schema"],
        connection_string=db_config["sirius_db_connection_string"],
    )
    new_records = get_records_to_match(
        schema=db_config["source_schema"],
        connection_string=db_config["db_connection_string"],
        ignore_migrated_records=True,
    )

    updated_caserefs = random.sample(list(set(new_records)), len(existing_records))
    print(f"updated_caserefs: {updated_caserefs}")

    query = ""
    for i, record in enumerate(existing_records):
        query += f"""
            update {db_config['sirius_schema']}.persons set caserecnumber = '{updated_caserefs[i]}' where caserecnumber = '{record}';
        """

    conn = psycopg2.connect(db_config["sirius_db_connection_string"])
    cursor = conn.cursor()

    print(f"query: {query}")
    try:
        cursor.execute(query)
        print(f"cursor.rowcount: {cursor.rowcount}")
    except Exception as e:
        log.error(e)

    cursor.close()
    conn.commit()
