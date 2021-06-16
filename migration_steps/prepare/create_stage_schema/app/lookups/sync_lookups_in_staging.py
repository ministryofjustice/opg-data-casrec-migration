import logging
import os
import helpers
import pandas as pd
from lookups.utilities import get_lookups_to_sync

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")


config = helpers.get_config(env=environment)


def get_unique_val(val_name, dict):
    try:
        return list(set([v[val_name] for k, v in dict.items()]))[0]
    except Exception as e:
        print(f"e: {e}")


def get_sirius_data(db_config, table):

    sirius_statement = f"""select * from {db_config['sirius_schema']}.{table};"""

    lookup_data = pd.read_sql_query(
        sql=sirius_statement, con=db_config["sirius_db_connection_string"]
    )

    lookup_data = lookup_data.fillna("")

    return lookup_data


def generate_update_statement(db_config, table, df):

    insert_statement = f"""
        DELETE FROM {db_config['target_schema']}.{table};
        INSERT INTO {db_config['target_schema']}.{table} ({', '.join(df.columns.tolist())}) VALUES
    """

    for i, row in enumerate(df.values.tolist()):
        row = [str(x) for x in row]
        row = [f"'{str(x)}'" if str(x) != "" else "NULL" for x in row]
        single_row = ", ".join(row)

        insert_statement += f"({single_row})"

        if i + 1 < len(df):
            insert_statement += ",\n"
        else:
            insert_statement += ";\n\n\n"

    return insert_statement


def sync_single_lookup(
    db_engine,
    db_config,
    field_to_sync,
    sirius_lookup_table,
):

    log.info(f"Syncing staging schema table {sirius_lookup_table}")

    sirius_data_df = get_sirius_data(
        db_config=db_config,
        table=sirius_lookup_table,
    )

    insert_query = generate_update_statement(
        db_config=db_config, table=sirius_lookup_table, df=sirius_data_df
    )

    try:

        db_engine.execute(insert_query)

    except Exception as e:

        log.error(
            f"Unable to sync {field_to_sync} using lookup table {sirius_lookup_table}: {e}",
            extra={
                "file_name": "",
                "error": helpers.format_error_message(e=e),
            },
        )


def sync_lookups(db_engine, db_config):
    lookups_to_sync = get_lookups_to_sync()

    for lookup, details in lookups_to_sync.items():
        for field in details:
            for field_to_sync, lookup_table_def in field.items():
                sync_single_lookup(
                    db_config=db_config,
                    db_engine=db_engine,
                    field_to_sync=field_to_sync,
                    sirius_lookup_table=list(lookup_table_def.values())[0],
                )
