import pandas as pd
from helpers import get_mapping_dict
from transform_data import transform
from utilities.generate_source_query import generate_select_string_from_mapping
import logging

from utilities.remove_empty_rows import remove_empty_rows
from utilities.standard_transformations import squash_columns

log = logging.getLogger("root")


def get_source_table(mapping_dict):
    source_table_list = [
        v["casrec_table"].lower()
        for k, v in mapping_dict.items()
        if v["casrec_table"] != ""
    ]
    no_dupes = list(set(source_table_list))
    if len(no_dupes) == 1:
        return list(set(source_table_list))[0]
    else:
        log.error("Multiple source tables")
        return ""


def get_basic_data_table(
    mapping_file_name, table_definition, db_config, chunk_details=None
):
    log.debug(f"Getting basic data using {mapping_file_name}")

    mapping_dict = get_mapping_dict(
        file_name=mapping_file_name, stage_name="transform_casrec"
    )

    source_table = get_source_table(mapping_dict=mapping_dict)

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    source_data_query = generate_select_string_from_mapping(
        mapping=mapping_dict,
        source_table_name=source_table,
        additional_columns=table_definition["source_table_additional_columns"],
        db_schema=db_config["source_schema"],
        chunk_details=chunk_details,
    )

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=db_config["db_connection_string"]
    )

    result_df = transform.perform_transformations(
        mapping_definitions=mapping_dict,
        table_definition=table_definition,
        source_data_df=source_data_df,
        db_conn_string=db_config["db_connection_string"],
        db_schema=db_config["target_schema"],
        sirius_details=sirius_details,
    )

    try:
        not_null_cols = table_definition.get(
            "source_not_null_cols", []
        ) + table_definition.get("destination_not_null_cols", [])
        log.debug(
            f"Removing rows where these fields are all null: {', '.join(not_null_cols)}"
        )

        result_df = remove_empty_rows(df=result_df, not_null_cols=not_null_cols)

    except KeyError:
        log.debug("Not removing any rows")
    except Exception as e:
        log.debug(f"prolems {e}")

    result_df["casrec_mapping_file_name"] = mapping_file_name
    result_df["casrec_table_name"] = source_table

    result_df = squash_columns(
        cols_to_squash=[
            "casrec_row_id",
            "casrec_mapping_file_name",
            "casrec_table_name",
        ],
        new_col="casrec_details",
        df=result_df,
        drop_original_cols=False,
        include_keys=True,
    )

    log.debug(f"Basic data for {mapping_file_name} has {len(result_df)} rows")

    return sirius_details, result_df
