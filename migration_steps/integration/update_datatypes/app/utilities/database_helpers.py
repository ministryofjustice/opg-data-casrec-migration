import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
import helpers

environment = os.environ.get("ENVIRONMENT")
config = helpers.get_config(env=environment)

import logging
from typing import Dict

log = logging.getLogger("root")


def generate_select_string(mapping_details: Dict, schema: str, table_name: str) -> str:
    log.debug(f"Generating select statement for {schema} - {table_name}")
    cols = ", ".join(list(mapping_details.keys()))
    statement = f"SELECT {cols} from {schema}.{table_name};"
    log.log(config.VERBOSE, f"Statement: {statement}")
    return statement


# def generate_create_statement(
#     mapping_details: Dict, schema: str, table_name: str
# ) -> str:
#     log.debug(f"Generating table create statement for {table_name}")
#     statement = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} (\n"
#
#     pg_remap = {
#         'str': 'text',
#         'date': 'timestamp',
#         'datetime': 'timestamp',
#     }
#
#     columns = []
#     for col, details in mapping_details.items():
#         details['data_type']  = pg_remap[details['data_type']] if details['data_type'] in pg_remap else details['data_type']
#         columns.append(f"{col} {details['data_type']}")
#         if details["is_pk"] is True or details["fk_parents"] is not None:
#             columns.append(f"sirius_{col} {details['data_type']}")
#
#     statement += ", ".join(columns)
#
#     statement += ");"
#     log.log(config.VERBOSE, f"Table create statement: {statement}")
#     return statement


def generate_mapping_table_create(
    mapping_details: Dict, schema: str, table_name: str, entity_name: str
) -> str:
    log.debug(
        f"Generating mapping table create statement for {entity_name} -"
        f" {table_name}"
    )
    statement = (
        f"CREATE TABLE IF NOT EXISTS {schema}.sirius_map_{entity_name}"
        f"_{table_name} (\n"
    )

    columns = []
    for col, details in mapping_details.items():
        if col in ["caserecnumber"]:
            columns.append(f"{col} {details['data_type']}")
        if details["is_pk"] is True or len(details["fk_parents"]) > 0:
            columns.append(f"sirius_{col} {details['data_type']}")

    statement += ", ".join(columns)

    statement += ");"
    log.log(config.VERBOSE, f"Mapping table create statement: {statement}")
    return statement
