from helpers import get_mapping_dict
import logging
import json
import pandas as pd

from utilities.datatypes import apply_datatypes

from utilities.database_helpers import (
    generate_mapping_table_create,
    generate_select_string,
)

log = logging.getLogger("root")


# temp - these could easily be in a shared json def
entity_name = "client"
entity_def = [
    {"mapping_defs": "client_persons", "sirius_table": "persons"},
    {"mapping_defs": "client_addresses", "sirius_table": "addresses"},
    {"mapping_defs": "client_phonenumbers", "sirius_table": "phonenumbers"},
]


def update_client_data_types(config, source_schema, target_schema, db):

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

        select_statement = generate_select_string(
            mapping_details=sirius_data, schema=source_schema, table_name=table_name
        )

        log.log(config.VERBOSE, f"select statement: {select_statement}")

        table_df = pd.read_sql_query(sql=select_statement, con=connection_string)

        table_df = apply_datatypes(mapping_details=sirius_data, df=table_df)

        log.log(config.VERBOSE, f"\n{table_df.info()}")

        # insert data into table
        db.insert_data(table_name=table_name, df=table_df, mapping_details=sirius_data)

        # create the mapping table
        mapping_table_create = generate_mapping_table_create(
            mapping_details=sirius_data,
            schema=target_schema,
            table_name=table_name,
            entity_name=entity_name,
        )
        log.log(config.VERBOSE, f"mapping_table_create: {mapping_table_create}")
        db.run_create_table_statement(
            table_name=table_name, statement=mapping_table_create
        )
