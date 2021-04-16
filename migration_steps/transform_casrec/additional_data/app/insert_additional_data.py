import datetime
import json
import os
import sys
from pathlib import Path
import logging
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
from helpers import get_additional_data_dict, get_config

log = logging.getLogger("root")

DEFAULT_USER_ID = 2
DB_TABLE_COLS = {
    # "id": "int",
    "entity": "varchar(255)",
    "details": "json",
    "sirius_table": "text",
    "sirius_pk_column": "text",
    "sirius_pk_value": "int",
    "c_casrec_row_id": "int",
}


def format_details(df, cols):

    df = df.replace("", np.nan)
    df = df.dropna(subset=cols, thresh=1)
    df = df.replace(np.nan, "")

    details_dict = df[[x for x in cols]].to_dict("records")

    df["details"] = details_dict
    df["details"] = df["details"].apply(lambda x: json.dumps(x))

    df = df.drop(columns=cols)

    return df


def format_other_cols(df, mapping_details):
    df["entity"] = mapping_details["entity"]
    df["sirius_table"] = mapping_details["sirius_table"]
    df["sirius_pk_column"] = mapping_details["sirius_table_pk_column"]

    return df


def join_to_sirius_table(db_config, df, mapping_details):

    base_data_query = f"""
        SELECT id, cast(casrec_row_id as int)
        FROM {db_config['target_schema']}.{mapping_details['sirius_table']}
    """

    try:
        condition = " "
        for i, (column, value) in enumerate(mapping_details["conditions"].items()):
            if i == 0:
                condition += "WHERE "
            else:
                condition += "AND "
            condition += f"""{column} = '{value}'"""
        base_data_query += condition

    except KeyError:
        pass

    base_data_df = pd.read_sql_query(
        sql=base_data_query, con=db_config["db_connection_string"]
    )

    df_with_sirius_id = df.merge(
        base_data_df, how="left", left_on="casrec_row_id", right_on="casrec_row_id"
    )

    df_with_sirius_id = df_with_sirius_id.rename(
        columns={"id": "sirius_pk_value", "casrec_row_id": "c_casrec_row_id"}
    )

    return df_with_sirius_id


def create_table(additional_data_table_name, db_config, target_db):

    cols_to_create = [f"{k} {v}" for k, v in DB_TABLE_COLS.items()]

    create_additional_data_table_statement = f"""
        CREATE TABLE {db_config['target_schema']}.{additional_data_table_name} (
            id serial primary key,
            {', '.join(cols_to_create)}
               );
    """
    print(
        f"create_additional_data_table_statement: {create_additional_data_table_statement}"
    )

    try:
        with target_db.begin() as conn:
            conn.execute(create_additional_data_table_statement)

    except Exception as e:
        log.error(
            f"table {additional_data_table_name} could not be created (probably already exists)"
        )
        print(f"e: {e}")


def create_insert_statement(db_config, additional_data_table_name, df):
    cols = df.columns.tolist()
    insert_statement = f"""
        INSERT INTO {db_config['target_schema']}.{additional_data_table_name} ({', '.join(cols)})
        VALUES
    """

    for i, row in enumerate(df.values.tolist()):
        row = [str(x) for x in row]
        row = [
            str(
                x.replace("'", "''")
                .replace("NaT", "")
                .replace("nan", "")
                .replace("<NA>", "")
                .replace("&", "and")
                .replace(";", "-")
                .replace("%", "percent")
            )
            for x in row
        ]
        row = [f"'{str(x)}'" if str(x) != "" else "NULL" for x in row]
        single_row = ", ".join(row)

        insert_statement += f"({single_row})"

        if i + 1 < len(df):
            insert_statement += ",\n"
        else:
            insert_statement += ";\n\n\n"

    return insert_statement


def insert_additional_data_records(db_config, additional_data_file_name):

    config = get_config(env=os.environ.get("ENVIRONMENT"))
    allowed_entities = [k for k, v in config.ENABLED_ENTITIES.items() if v is True]
    additional_data_dict = get_additional_data_dict(file_name=additional_data_file_name)

    if not additional_data_dict["entity"] in allowed_entities:
        log.info(
            f"{additional_data_file_name} is party of entity '{additional_data_dict['entity']}'  which is not enabled, moving on"
        )
        return False

    additional_data_table_name = f"additional_data_{additional_data_dict['entity']}_{additional_data_dict['sirius_table']}"
    details_columns = [v for k, v in additional_data_dict["detail_cols"].items()]

    target_db_engine = create_engine(db_config["db_connection_string"])

    cols = ", ".join(
        f'"{col}" as "{alias}"'
        for col, alias in additional_data_dict["detail_cols"].items()
    )

    additional_data_data_query = f"""
        SELECT {cols}, casrec_row_id
        FROM {db_config['source_schema']}.{additional_data_dict['casrec_table']}
        ORDER BY casrec_row_id;
    """

    create_table(
        additional_data_table_name=additional_data_table_name,
        db_config=db_config,
        target_db=target_db_engine,
    )

    conn = target_db_engine.connect().execution_options(stream_results=True)

    for additional_data_df in pd.read_sql(
        additional_data_data_query, conn, chunksize=config.DEFAULT_CHUNK_SIZE
    ):
        additional_data_df = format_details(additional_data_df, details_columns)
        additional_data_df = format_other_cols(additional_data_df, additional_data_dict)
        additional_data_df = join_to_sirius_table(
            db_config, additional_data_df, additional_data_dict
        )

        insert_statement = create_insert_statement(
            db_config=db_config,
            additional_data_table_name=additional_data_table_name,
            df=additional_data_df,
        )

        try:

            with target_db_engine.begin() as conn:
                inserted = conn.execute(insert_statement)
                log.debug(
                    f"inserted {inserted.rowcount} rows into {additional_data_table_name}"
                )

        except Exception as e:
            log.error("TERRIBLE ERRORROROROR inserting into the table")
            print(f"e: {e}")
