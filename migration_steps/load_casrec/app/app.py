import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import pandas as pd
import io
import re
import time
from sqlalchemy import create_engine
import boto3
import custom_logger
from dotenv import load_dotenv
from helpers import get_config, log_title, get_s3_session
import logging
import click
from db_helpers import replace_with_sql_friendly_chars

env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

# Env variables
ci = os.getenv("CI")
account = os.environ["SIRIUS_ACCOUNT"]
path = os.environ["S3_PATH"]
environment = os.environ.get("ENVIRONMENT")
account_name = os.environ.get("ACCOUNT_NAME")

# Config
config = get_config(environment)
chunk_size = config.DEFAULT_CHUNK_SIZE
schema = config.schemas["pre_transform"]

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment, module_name="load casrec schema")
log = logging.getLogger("root")

# Orchestration table
progress_table = "migration_progress"
progress_table_cols = [
    "file",
    "state",
    "process",
]

# DB
db_conn_string = config.get_db_connection_string("migration")
engine = create_engine(db_conn_string)

# S3
s3_url = os.environ.get("S3_URL")
s3 = get_s3_session(environment, s3_url, ci=ci, account=account)
bucket_name = f"casrec-migration-{account_name.lower()}"


def get_list_of_files(bucket_name, s3, path, tables):
    log.info(f"Get files from {bucket_name}:")
    resp = s3.list_objects_v2(Bucket=bucket_name)
    files_in_bucket = []
    files_to_process = []

    for obj in resp["Contents"]:
        file_folder = obj["Key"]
        folder = file_folder.split("/")[0]
        file = file_folder.split("/")[1]
        if folder == path and len(file) > 1:
            ignore_list = []
            if any(word in file for word in ignore_list):
                log.info(f"ignoring {file} files for now...")
            else:
                if file.endswith(".csv") or file.endswith(".xlsx"):
                    log.info(file_folder)
                    files_in_bucket.append(file)

    if tables[0].lower() == "all":
        log.info("Will process all files")
        files_to_process.extend(files_in_bucket)
    else:
        log.info("Bring back specific entities")
        for bucket_file in files_in_bucket:
            if bucket_file.split(".")[0].lower() in tables:
                files_to_process.append(bucket_file)

    log.info(f"Total files returned: {len(files_in_bucket)}")
    return files_to_process


def get_remaining_files(table_name, schema_name, engine, status, process=None):

    if process is not None:
        remaining_files = f"""
            SELECT file
            FROM \"{schema_name}\".\"{table_name}\"
            WHERE state = '{status}'
            AND process = '{process}';
            """
    else:
        remaining_files = f"""
            SELECT file
            FROM \"{schema_name}\".\"{table_name}\"
            WHERE state = '{status}';
            """

    files = engine.execute(remaining_files)
    file_list = []
    for r in files:
        file_list.append(r.values()[0])
        return file_list
    return file_list


def update_progress(
    table_name, schema_name, engine, file, status="IN_PROGRESS", process=None
):
    file_left = file.split(".")[0]
    if status == "READY_TO_PROCESS" and file_left[-1].isdigit():
        regex = re.compile("[^a-zA-Z_]")
        file_left = regex.sub("", file_left)
        row_update = f"""
            UPDATE \"{schema_name}\".\"{table_name}\"
            SET state = '{status}', process = '{process}'
            WHERE file LIKE '{str(file_left)}%%'
            AND state = 'UNPROCESSED';
            """
    elif process is not None:
        row_update = f"""
            UPDATE \"{schema_name}\".\"{table_name}\"
            SET state = '{status}', process = '{process}'
            WHERE file = '{file}';
            """
    else:
        row_update = f"""
            UPDATE \"{schema_name}\".\"{table_name}\"
            SET state = '{status}'
            WHERE file = '{file}';
            """

    response = engine.execute(row_update)
    if response.rowcount > 0:
        log.info(f"Updated {file} to {status}")


def check_table_exists(table_name, schema_name, engine):
    check_exists_statement = f"""
    SELECT EXISTS (
       SELECT FROM information_schema.tables
       WHERE  table_schema = '{schema_name}'
       AND    table_name   = '{table_name}'
    );
    """

    check_exists_result = engine.execute(check_exists_statement)

    for r in check_exists_result:
        table_exists = r.values()[0]
        return table_exists


def check_table_multipart(table_name, tbl, schema_name, engine):
    check_exists_statement = f"""
        SELECT COUNT(*)
        FROM "{schema_name}"."{tbl}"
        WHERE file ~ \'^{table_name}\\d\'
        AND state IN ('COMPLETE');
    """
    log.info(check_exists_statement)

    check_exists_result = engine.execute(check_exists_statement)

    for r in check_exists_result:
        row_count = r.values()[0]
        log.info(f"row count: {row_count}")
    if row_count > 0:
        return True
    else:
        return False


def check_columns_exist(table_name, schema, csv_cols, engine):
    existing_cols_statement = (
        f"SELECT column_name FROM "
        f"information_schema.columns "
        f"WHERE  table_schema = '{schema}'"
        f"AND    table_name   = '{table_name}';"
    )

    existing_cols = engine.execute(existing_cols_statement)
    existing_cols_list = [row[0] for row in existing_cols]

    if len(existing_cols_list) != len(csv_cols):
        log.warning("There is a column difference between multipart files")

    col_diff = [i for i in csv_cols if i not in existing_cols_list]

    return col_diff


def add_missing_columns_statement(table, schema, col_diff):

    log.info(
        f"Adding columns to existing table due to column difference \"{', '.join(col_diff)}\""
    )

    statement = f"""
        ALTER TABLE "{schema}"."{table}"
        """
    for i, col in enumerate(col_diff):
        statement += f'ADD COLUMN "{col}" text'
        if i + 1 < len(col_diff):
            statement += ","
    statement += ";"

    return statement


def create_table_statement(table_name, schema, columns):
    create_statement = f"""
        CREATE TABLE IF NOT EXISTS "{schema}"."{table_name}"
        ("casrec_row_id" INT GENERATED ALWAYS AS IDENTITY,
        """
    for i, col in enumerate(columns):
        create_statement += f'"{col}" text'
        if i + 1 < len(columns):
            create_statement += ","
    create_statement += "); \n\n\n"

    return create_statement


def truncate_table(table_name, schema, engine):
    log.info(f"Truncating table {schema}.{table_name}")
    truncate_statement = f'TRUNCATE TABLE "{schema}"."{table_name}"'
    engine.execute(truncate_statement)


def create_insert_statement(table_name, schema, columns, df):
    insert_statement = f'INSERT INTO "{schema}"."{table_name}" ('
    for i, col in enumerate(columns):
        insert_statement += f'"{col}"'
        if i + 1 < len(columns):
            insert_statement += ","

    insert_statement += ") \n VALUES \n"

    for i, row in enumerate(df.values.tolist()):
        row = [str(x) for x in row]
        row = replace_with_sql_friendly_chars(row_as_list=row)
        row = [f"'{str(x)}'" for x in row]
        single_row = ", ".join(row)

        insert_statement += f"({single_row})"

        if i + 1 < len(df):
            insert_statement += ",\n"
        else:
            insert_statement += ";\n\n\n"

    return insert_statement


def get_row_count(table_name, schema_name, engine, status=None, process=None):
    get_count_statement = f"""
        SELECT COUNT(*) FROM {schema_name}.{table_name}
        """

    if status is not None:
        get_count_statement += f" WHERE state = '{status}'"
        if process is not None:
            get_count_statement += f" AND process = '{process}'"

    get_count_result = engine.execute(get_count_statement)
    for r in get_count_result:
        count = r.values()[0]
        return count


def create_schema(schema, engine):
    schema_exist_statement = f"""
    SELECT
    EXISTS(SELECT
    1
    FROM
    information_schema.schemata
    WHERE
    schema_name = '{schema}');
    """

    schema_exists_result = engine.execute(schema_exist_statement)
    for r in schema_exists_result:
        exists = r.values()[0]

    if not exists:
        log.info(f"Creating schema {schema}...")
        create_schema_sql = f"CREATE SCHEMA {schema} AUTHORIZATION casrec;"
        engine.execute(create_schema_sql)
        log.info(f"Schema {schema} created\n\n")
    else:
        log.info(f"Schema {schema} already exists\n\n")


def sirius_session(account):

    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]
    log.info(f"Current users account: {account_id}")

    role_to_assume = f"arn:aws:iam::{account}:role/migrations-ci"
    response = client.assume_role(
        RoleArn=role_to_assume, RoleSessionName="assumed_role"
    )

    session = boto3.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )

    return session


def create_table(table, schema, engine, table_cols):
    if not check_table_exists(table, schema, engine):
        log.info(f"Creating {table} table")
        engine.execute(create_table_statement(table, schema, table_cols))
    else:
        log.info(f"{table} table exists")


def get_df_from_file(file):
    file_key = f"{path}/{file}"
    log.info(f'Retrieving "{file_key}" from bucket')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    if file.split(".")[1] == "csv":
        df = pd.read_csv(
            io.BytesIO(obj["Body"].read()), keep_default_na=False, dtype=str
        )
    elif file.split(".")[1] == "xlsx":
        df = pd.read_excel(
            io.BytesIO(obj["Body"].read()),
            engine="openpyxl",
            keep_default_na=False,
            dtype=str,
        )
    else:
        log.info("Unknown file format")
        exit(1)
    df_renamed = df.rename(columns={"Unnamed: 0": "csv_record"})

    return df_renamed


def initialise_progress_table(
    progress_table,
    list_of_files,
    schema,
    engine,
    progress_table_cols,
    process,
    process_total,
):
    if process == 1:
        progress_df = pd.DataFrame(list_of_files)
        progress_df["state"] = "UNPROCESSED"
        progress_df["process"] = "None"
        progress_df.rename(index={0: "file"})
        truncate_table(progress_table, schema, engine)

        engine.execute(
            create_insert_statement(
                progress_table, schema, progress_table_cols, progress_df
            )
        )

        while get_row_count(progress_table, schema, engine, status="UNPROCESSED") > 0:
            files = get_remaining_files(progress_table, schema, engine, "UNPROCESSED")
            if len(files) > 0:
                file_to_set = files[0]

                # Increment process for each loop until we get to max then reset
                process += 1
                if process > process_total:
                    process = 1

                update_progress(
                    progress_table,
                    schema,
                    engine,
                    file_to_set,
                    "READY_TO_PROCESS",
                    process,
                )
    else:
        while not check_table_exists(progress_table, schema, engine):
            time.sleep(2)
        while True:
            if (
                get_row_count(progress_table, schema, engine, "UNPROCESSED") == 0
                and get_row_count(progress_table, schema, engine, "READY_TO_PROCESS")
                > 1
            ):
                break
            else:
                time.sleep(2)


def get_table_name(file):
    table_name = file.split(".")[0].lower()
    if table_name[-1].isdigit():
        regex = re.compile("[^a-zA-Z_]")
        table_name = regex.sub("", table_name)

    return table_name


def create_or_update_table_from_csv(table_name, columns):
    if check_table_multipart(table_name, progress_table, schema, engine):
        log.info("Multipart file table detected")

        col_diff = check_columns_exist(
            table_name=table_name,
            schema=schema,
            csv_cols=columns,
            engine=engine,
        )
        if len(col_diff) != 0:
            add_cols_statement = add_missing_columns_statement(
                table=table_name, schema=schema, col_diff=col_diff
            )
            engine.execute(add_cols_statement)
    else:
        log.info(f"Table {schema}.{table_name} doesn't exist. Creating table...")
        engine.execute(create_table_statement(table_name, schema, columns))
        log.info(f"Table {schema}.{table_name} created")


def insert_rows_from_dataframe(df, table_name, columns, process, file):
    if len(df.index) > 0:
        try:
            n = chunk_size  # chunk row size
            list_df = [df[i : i + n] for i in range(0, df.shape[0], n)]

            for df_chunked in list_df:
                engine.execute(
                    create_insert_statement(table_name, schema, columns, df_chunked)
                )
                log.info(
                    f'Rows inserted into "{schema}"."{table_name}": {get_row_count(table_name, schema, engine)}'
                )
            update_progress(progress_table, schema, engine, file, "COMPLETE", process)
            log.info(f"Processed {file}\n\n")
        except Exception as e:
            update_progress(
                progress_table,
                schema,
                engine,
                file,
                f"FAILED {e}",
                process,
            )
            log.info(f"Failed to process {file}\n\n")
    else:
        log.info(f"No rows to insert for table {table_name}")
        update_progress(progress_table, schema, engine, file, "COMPLETE", process)


@click.command()
@click.option("-p", "--process", default="1", help="process being used")
@click.option("-t", "--process_total", default="1", help="total processes")
@click.option("-e", "--entities", default="all", help="list of entities to load")
def main(process, process_total, entities):
    table_list = entities.split(",")
    process = int(process)
    process_total = int(process_total)
    if process == 1:
        create_schema(schema, engine)
        create_table(progress_table, schema, engine, progress_table_cols)
    list_of_files = get_list_of_files(bucket_name, s3, path, table_list)

    initialise_progress_table(
        progress_table,
        list_of_files,
        schema,
        engine,
        progress_table_cols,
        process,
        process_total,
    )

    while (
        get_row_count(
            progress_table,
            schema,
            engine,
            status="READY_TO_PROCESS",
            process=process,
        )
        > 0
    ):

        file = get_remaining_files(
            progress_table,
            schema,
            engine,
            status="READY_TO_PROCESS",
            process=process,
        )[0]

        log.info(f"Processor {process} has picked up {file}")
        update_progress(progress_table, schema, engine, file, status="IN_PROGRESS")

        table_name = get_table_name(file)
        df = get_df_from_file(file)
        columns = [x for x in df.columns.values]

        create_or_update_table_from_csv(table_name, columns)

        log.info(f'Inserting records into "{schema}"."{table_name}"')
        insert_rows_from_dataframe(df, table_name, columns, process, file)

    log.info(f"Processor {process} has finished processing")


if __name__ == "__main__":
    main()
