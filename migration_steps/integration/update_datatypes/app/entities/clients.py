from helpers import get_mapping_dict
import logging
import json
import pandas as pd

from utilities.datatypes import apply_datatypes

from utilities.database import (
    generate_select_string,
    generate_create_statement,
    generate_mapping_table_create,
)

log = logging.getLogger("root")


# temp - these could easily be in a shared json def
entity_name = "client"
entity_def = [
    {"mapping_defs": "client_persons", "sirius_table": "persons"},
    {"mapping_defs": "client_addresses", "sirius_table": "addresses"},
    {"mapping_defs": "client_phonenumbers", "sirius_table": "phonenumbers"},
]


def update_client_data_types(config, source_schema, target_schema):

    for table in entity_def:

        mapping_file = f"{table['mapping_defs']}_mapping"
        table_name = table["sirius_table"]
        connection_string = config.get_db_connection_string(db="migration")

        sirius_data = get_mapping_dict(
            file_name=mapping_file,
            stage_name="sirius_details",
            only_complete_fields=True,
        )

        log.log(config.VERBOSE, f"sirius_data: {json.dumps(sirius_data, indent=4) }")

        # create the main sirius-like table
        create_statement = generate_create_statement(
            mapping_details=sirius_data, schema=source_schema, table_name=table_name
        )

        # create the mapping table
        mapping_table_create = generate_mapping_table_create(
            mapping_details=sirius_data,
            schema=source_schema,
            table_name=table_name,
            entity_name=entity_name,
        )

        log.info(f"create_statement: {create_statement}")
        log.info(f"mapping_table_create: {mapping_table_create}")

        # get the data from the 'transform' schema
        select_statement = generate_select_string(
            mapping_details=sirius_data, schema=source_schema, table_name=table_name
        )

        log.log(config.VERBOSE, f"select statement: {select_statement}")

        table_df = pd.read_sql_query(sql=select_statement, con=connection_string)

        table_df = apply_datatypes(mapping_details=sirius_data, df=table_df)

        log.log(config.VERBOSE, f"\n{table_df.info()}")
