import logging
import os
from helpers import (
    get_config,
    format_error_message,
    get_mapping_dict,
    list_all_mapping_files,
)


log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")


config = get_config(env=environment)


def get_cols_to_convert():
    mapping_files = list_all_mapping_files()

    cols_to_convert = {}
    for file in mapping_files:
        file_name = file[:-5]
        mapping_dict = get_mapping_dict(file_name=file_name, stage_name="integration")

        for field, details in mapping_dict.items():
            if "convert_to_int" in details["business_rules"]:

                sirius_table = get_mapping_dict(
                    file_name=file_name, stage_name="sirius_details"
                )[field]["table_name"]

                if sirius_table in cols_to_convert:
                    cols_to_convert[cols_to_convert].append({field: "int"})
                else:
                    cols_to_convert[sirius_table] = [{field: "int"}]

    return cols_to_convert


def convert_single_col(db_config, db_engine, result_table, field_to_convert, datatype):
    map_sql_datatypes = {"int": "INTEGER"}
    update_statement = f"""
        ALTER TABLE {db_config['target_schema']}.{result_table}
        ALTER COLUMN {field_to_convert} TYPE {map_sql_datatypes[datatype]} USING ({field_to_convert}::{map_sql_datatypes[datatype]});"""

    try:
        print(f"update_statement: {update_statement}")
        db_engine.execute(update_statement)

    except Exception as e:

        log.error(
            f"Unable to convert {result_table}.{field_to_convert} to {datatype}: {e}",
            extra={
                "file_name": "",
                "error": format_error_message(e=e),
            },
        )


def convert_datatypes(db_engine, db_config):
    cols_to_convert = get_cols_to_convert()

    for col, details in cols_to_convert.items():
        sirius_table = col

        for field in details:

            for field_to_convert, datatype in field.items():
                convert_single_col(
                    db_config=db_config,
                    db_engine=db_engine,
                    result_table=sirius_table,
                    field_to_convert=field_to_convert,
                    datatype=datatype,
                )
