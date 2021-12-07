import json
import logging

import psycopg2
import os
import sys
from pathlib import Path

from custom_errors import IncorrectRowCount

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

import helpers

log = logging.getLogger("root")


environment = os.environ.get("ENVIRONMENT")
config = helpers.get_config(env=environment)


def get_current_directory():
    dirname = os.path.dirname(__file__)
    return dirname


def count_rows(connection_string, destination_schema, enabled_entities, correfs):
    # feature_flag row-counts
    if "row-counts" not in config.enabled_feature_flags(env=environment):
        return False

    log.info(
        helpers.log_title(
            message=f"Checking row counts for schema '{destination_schema}', Correfs: '{', '.join(correfs) if correfs else 'all'}'"
        )
    )

    current_dir = get_current_directory()

    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    with open(f"{current_dir}/dev_row_counts.json", "r") as row_count_json:
        row_count_dict = json.load(row_count_json)

        for item in row_count_dict:
            for entity_name, entity_details in item.items():
                if entity_name in enabled_entities:

                    for query_details in entity_details:
                        query = query_details["query"]
                        casrec_query = query_details["casrec_query"]

                        query_schema = query.replace("{schema}", destination_schema)
                        casrec_query = casrec_query.replace(
                            "{schema}", destination_schema
                        )

                        try:
                            cursor.execute(query_schema)
                            row_count = cursor.fetchall()[0][0]

                            cursor.execute(casrec_query)
                            expected_row_count = cursor.fetchall()[0][0]

                            if row_count != expected_row_count:
                                raise IncorrectRowCount
                            # else:
                            #     log.debug(f"{entity_name} - {query_details['table_name']} row counts match")

                        except IncorrectRowCount:
                            log.error(
                                f"'{entity_name} {query_details['table_name']}' row counts do not match: "
                                f"expected {expected_row_count}, actual {row_count}"
                            )
                        except psycopg2.DatabaseError as e:
                            log.error(e)
                        except (Exception) as e:
                            log.error(e)
        log.info("All row counts checked")
