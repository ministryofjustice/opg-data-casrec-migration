import logging
import os

import psycopg2
import pandas as pd
import helpers
from helpers import get_mapping_dict, list_all_mapping_files, get_lookup_dict

parent_table = "bonds"
parent_match_col = "bond_provider_id"
lookup_table = "bond_providers"
lookup_result_col = "id"
lookup_match_col = "uid"

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")


config = helpers.get_config(env=environment)


def get_lookups_to_reindex():
    mapping_files = list_all_mapping_files()

    lookups_to_reindex = {}
    for file in mapping_files:
        file_name = file[:-5]
        mapping_dict = get_mapping_dict(file_name=file_name, stage_name="integration")

        for field, details in mapping_dict.items():
            if "reindex_lookup" in details["business_rules"]:
                lookup_def = get_mapping_dict(
                    file_name=file_name, stage_name="transform_casrec"
                )[field]["lookup_table"]
                sirius_table = get_mapping_dict(
                    file_name=file_name, stage_name="sirius_details"
                )[field]["table_name"]
                lookup_table = get_mapping_dict(
                    file_name=file_name, stage_name="sirius_details"
                )[field]["fk_parents"].split(":")[0]

                if sirius_table in lookups_to_reindex:
                    lookups_to_reindex[sirius_table].append(
                        {field: {lookup_def: lookup_table}}
                    )
                else:
                    lookups_to_reindex[sirius_table] = [
                        {field: {lookup_def: lookup_table}}
                    ]

    return lookups_to_reindex


def get_unique_val(val_name, dict):
    try:
        return list(set([v[val_name] for k, v in dict.items()]))[0]
    except Exception as e:
        print(f"e: {e}")


def get_sirius_lookup_data(db_config, fields_to_select, table):
    query = f"""select {', '.join(fields_to_select)} from {db_config['sirius_schema']}.{table};"""

    lookup_data = pd.read_sql_query(
        sql=query, con=db_config["sirius_db_connection_string"]
    )

    return lookup_data


def generate_sirius_lookup_remap(df, lookup_field, result_field):

    df = df.set_index(lookup_field)
    lookup_remap = {k: v[result_field] for k, v in df.to_dict("index").items()}

    return lookup_remap


def generate_updates(lookup_remap, schema, table, field_to_reindex):
    update_sirius_queries = []
    for old_val, new_val in lookup_remap.items():
        update_sirius_queries.append(
            f"UPDATE {schema}.{table} set {field_to_reindex} = {new_val} where {field_to_reindex} = '{old_val}';"
        )

        log.debug(
            f"Generating query to update {table}.{field_to_reindex} to {new_val} where {field_to_reindex} = {old_val} "
        )

    return update_sirius_queries


def reindex_single_lookup(
    db_engine,
    db_config,
    result_table,
    lookup_table_def,
    field_to_reindex,
    sirius_lookup_table,
):

    lookup_dict_with_sirius_details = get_lookup_dict(
        lookup_table_def, include_sirius_details=True
    )

    sirius_lookup_field = get_unique_val(
        val_name="sirius_lookup_field", dict=lookup_dict_with_sirius_details
    )
    sirius_result_field = get_unique_val(
        val_name="sirius_result_field", dict=lookup_dict_with_sirius_details
    )

    sirius_data_df = get_sirius_lookup_data(
        db_config=db_config,
        fields_to_select=[sirius_lookup_field, sirius_result_field],
        table=sirius_lookup_table,
    )
    sirius_lookup_remap = generate_sirius_lookup_remap(
        df=sirius_data_df,
        lookup_field=sirius_lookup_field,
        result_field=sirius_result_field,
    )
    update_statements = generate_updates(
        lookup_remap=sirius_lookup_remap,
        schema=db_config["target_schema"],
        table=result_table,
        field_to_reindex=field_to_reindex,
    )

    try:

        db_engine.execute(" ".join(update_statements))

    except Exception as e:

        log.error(
            f"Unable to reindex {field_to_reindex} using lookup table {sirius_lookup_table}: {e}",
            extra={
                "file_name": "",
                "error": helpers.format_error_message(e=e),
            },
        )


def reindex_lookups(db_engine, db_config):
    lookups_to_reindex = get_lookups_to_reindex()

    for lookup, details in lookups_to_reindex.items():
        sirius_result_table = lookup
        for field in details:
            for field_to_reindex, lookup_table_def in field.items():
                reindex_single_lookup(
                    db_config=db_config,
                    db_engine=db_engine,
                    result_table=sirius_result_table,
                    lookup_table_def=list(lookup_table_def.keys())[0],
                    field_to_reindex=field_to_reindex,
                    sirius_lookup_table=list(lookup_table_def.values())[0],
                )
