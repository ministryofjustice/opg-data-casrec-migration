import logging
import os
import helpers
import pandas as pd
from lookups.utilities import get_lookups_to_sync

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")


config = helpers.get_config(env=environment)


def get_sirius_data(db_config, table):

    sirius_statement = f"""select * from {db_config['sirius_schema']}.{table};"""

    lookup_data = pd.read_sql_query(
        sql=sirius_statement, con=db_config["sirius_db_connection_string"]
    )

    lookup_data = lookup_data.fillna("")

    return lookup_data


def check_single_lookup(db_config, table, lookup_file_name):
    log.info(f"Checking mapping values for lookup def {lookup_file_name}")

    lookup_dict = helpers.get_lookup_dict(file_name=lookup_file_name)
    unique_vals = list(set([x for x in lookup_dict.values()]))

    sirius_data_df = get_sirius_data(
        db_config=db_config,
        table=table,
    )

    sirius_values = sirius_data_df["id"].tolist()
    log.debug(f"unique_vals: {unique_vals}")
    log.debug(f"sirius_values: {sirius_values}")

    if all(x in sirius_values for x in unique_vals):
        return True
    else:
        missing_in_sirius = [str(x) for x in unique_vals if x not in sirius_values]
        log.error(f"lookup values missing from sirius: {', '.join(missing_in_sirius)}")


def check_lookups(db_config):
    lookups_to_check = get_lookups_to_sync()

    for lookup, details in lookups_to_check.items():
        for field in details:
            for field_to_sync, lookup_table_def in field.items():
                lookup_file_name = list(lookup_table_def.keys())[0]
                sirius_lookup_table = list(lookup_table_def.values())[0]
                is_lookup_ok = check_single_lookup(
                    db_config=db_config,
                    table=sirius_lookup_table,
                    lookup_file_name=lookup_file_name,
                )

                if is_lookup_ok:
                    log.info(f"All lookup values in the {lookup_file_name} are OK")
                else:
                    log.error(
                        f"Lookup values in {lookup_file_name} do not match the destination, exiting"
                    )
                    os._exit(1)
