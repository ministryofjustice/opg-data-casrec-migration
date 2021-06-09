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
                lookup_table = get_mapping_dict(
                    file_name=file_name, stage_name="transform_casrec"
                )[field]["lookup_table"]
                sirius_table = get_mapping_dict(
                    file_name=file_name, stage_name="sirius_details"
                )[field]["table_name"]

                if sirius_table in lookups_to_reindex:
                    lookups_to_reindex[sirius_table].append({field: lookup_table})
                else:
                    lookups_to_reindex[sirius_table] = [{field: lookup_table}]

    # print(f"lookups_to_reindex: {lookups_to_reindex}")
    return lookups_to_reindex


def get_unique_val(val_name, dict):
    try:
        return list(set([v[val_name] for k, v in dict.items()]))[0]
    except Exception as e:
        print(f"e: {e}")


def get_sirius_data(query):
    pass

    # try:
    #     # sirius_data =pd.read_sql_query(sirius_query, sirius_db_connection_string)
    #     connection_string = con
    #     conn = psycopg2.connect(connection_string)
    #     cursor = conn.cursor()
    #     cursor.execute(sirius_query)
    #     max_vals = cursor.fetchall()
    #     print(f"max_vals: {max_vals}")
    #
    # except Exception as e:
    #     print(f"e: {e}")


def reindex_single_lookup():
    sirius_table = "bonds"
    field_to_reindex = "bond_provider_id"
    lookup_table = "bond_provider_lookup"

    lookup_dict_with_sirius_details = get_lookup_dict(
        lookup_table, include_sirius_details=True
    )

    sirius_lookup_field = get_unique_val(
        val_name="sirius_lookup_field", dict=lookup_dict_with_sirius_details
    )
    sirius_result_field = get_unique_val(
        val_name="sirius_result_field", dict=lookup_dict_with_sirius_details
    )

    sirius_schema = "blah"
    sirius_query = f"""select {sirius_result_field}, {sirius_lookup_field} from {sirius_schema}.{sirius_table};"""

    sirius_data = get_sirius_data(query=sirius_query)

    sirius_data_df = pd.DataFrame(sirius_data, columns=[x for x in sirius_data])
    sirius_data_df = sirius_data_df.set_index(sirius_lookup_field)
    sirius_lookup_remap = {
        k: v[sirius_result_field] for k, v in sirius_data_df.to_dict("index").items()
    }

    print(f"sirius_lookup_remap: {sirius_lookup_remap}")

    update_sirius_queries = []
    for old_val, new_val in sirius_lookup_remap.items():
        update_sirius_queries.append(
            f"UPDATE {sirius_table} set {field_to_reindex} = {new_val} where {field_to_reindex} = '{old_val}';"
        )

    print(f"update_sirius_query: {update_sirius_queries}")
