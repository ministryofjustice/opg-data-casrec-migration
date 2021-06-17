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


def count_rows(connection_string, destination_schema, enabled_entities, team=""):
    log.info(
        helpers.log_title(
            message=f"Checking row counts for schema '{destination_schema}',  team: '{team if team != '' else 'all'}'"
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
                        query_schema = query.replace("{schema}", destination_schema)
                        if team != "":
                            expected_row_count = query_details["row_counts"][
                                f"team_{team}"
                            ]
                        else:
                            expected_row_count = query_details["row_counts"]["all"]

                        try:
                            cursor.execute(query_schema)
                            row_count = cursor.fetchall()[0][0]

                            if row_count != expected_row_count:

                                raise IncorrectRowCount

                        except IncorrectRowCount:
                            log.error(
                                f"'{entity_name} {query_details['table_name']}' row counts do not match: "
                                f"expected {expected_row_count}, actual {row_count}"
                            )
                        except psycopg2.DatabaseError as e:
                            log.error(
                                f"error checking row counts for {entity_name} - table probably doesn't exist",
                                extra={"error": helpers.format_error_message(e=e)},
                            )
                        except (Exception) as e:
                            log.error(
                                e, extra={"error": helpers.format_error_message(e=e)}
                            )
        log.info("All row counts checked")
