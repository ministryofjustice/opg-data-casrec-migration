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
import random as rnd
import custom_logger
from dotenv import load_dotenv
from helpers import get_config, log_title
import logging
import click

environment = os.environ.get("ENVIRONMENT")
account_name = os.environ.get("ACCOUNT_NAME")
config = get_config(environment)
config.custom_log_level()
verbosity_levels = config.verbosity_levels
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())


def get_list_of_files(bucket_name, s3, path, tables):
    resp = s3.list_objects_v2(Bucket=bucket_name)
    files_in_bucket = []
    files_to_process = []

    for obj in resp["Contents"]:
        file_folder = obj["Key"]
        log.info(file_folder)
        folder = file_folder.split("/")[0]
        file = file_folder.split("/")[1]
        if folder == path and len(file) > 1:
            ignore_list = []
            if any(word in file for word in ignore_list):
                log.info(f"ignoring {file} files for now...")
            else:
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


def setup_logging(log, verbose, log_title, bucket_name):
    try:
        log.setLevel(verbosity_levels[verbose])
        log.info(f"{verbosity_levels[verbose]} logging enabled")
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")
        log.info(f"INFO logging enabled")

    log.info(log_title(message="Load CasRec: CSV to DB transfer"))
    log.info(log_title(message=f"s3 bucket: {bucket_name}"))
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")


def get_remaining_files(table_name, schema_name, engine, status, processor_id=None):

    if processor_id is not None:
        remaining_files = f"""
            SELECT file
            FROM \"{schema_name}\".\"{table_name}\"
            WHERE state = '{status}'
            AND processor_id = '{processor_id}';
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
    table_name, schema_name, engine, file, status="IN_PROGRESS", processor_id=None
):
    file_left = file.split(".")[0]
    if status == "READY_TO_PROCESS" and file_left[-1].isdigit():
        regex = re.compile("[^a-zA-Z_]")
        file_left = regex.sub("", file_left)
        row_update = f"""
            UPDATE \"{schema_name}\".\"{table_name}\"
            SET state = '{status}', processor_id = '{processor_id}'
            WHERE file LIKE '{str(file_left)}%%';
            """
    elif processor_id is not None:
        row_update = f"""
            UPDATE \"{schema_name}\".\"{table_name}\"
            SET state = '{status}', processor_id = '{processor_id}'
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


def table_exists_already(table_name, table_lookup, schema_name, engine):
    check_exists_statement = f"""
        SELECT COUNT(*)
        FROM "{schema_name}"."{table_lookup}"
        WHERE table_name = \'{table_name}\';
    """

    check_exists_result = engine.execute(check_exists_statement)
    for r in check_exists_result:
        row_count = r.values()[0]
    if row_count > 0:
        return True
    else:
        return False


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


def add_lookup_table_row(table_name, table_lookup, schema_name, engine):
    insert_statement = f"""
        INSERT INTO "{schema_name}"."{table_lookup}" (table_name) VALUES (\'{table_name}\');
    """
    engine.execute(insert_statement)


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
        row = [
            str(
                x.replace("'", "''")
                .replace("nan", "")
                .replace("&", "")
                .replace(";", "")
                .replace("%", "")
            )
            for x in row
        ]
        row = [f"'{str(x)}'" for x in row]
        single_row = ", ".join(row)

        insert_statement += f"({single_row})"

        if i + 1 < len(df):
            insert_statement += ",\n"
        else:
            insert_statement += ";\n\n\n"
    return insert_statement


def get_row_count(table_name, schema_name, engine, status=None, processor_id=None):
    get_count_statement = f"""
        SELECT COUNT(*) FROM {schema_name}.{table_name}
        """

    if status is not None:
        get_count_statement += f" WHERE state = '{status}'"
        if processor_id is not None:
            get_count_statement += f" AND processor_id = '{processor_id}'"

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


def get_s3_session(host, account, ci):
    s3_session = boto3.session.Session()
    if environment == "local":

        if host == "localhost":
            stack_host = "localhost"
        else:
            stack_host = "localstack"
        s3 = s3_session.client(
            "s3",
            endpoint_url=f"http://{stack_host}:4572",
            aws_access_key_id="fake",
            aws_secret_access_key="fake",
        )
    elif ci == "true":
        s3_session = sirius_session(account)
        s3 = s3_session.client("s3")
    else:
        s3 = s3_session.client("s3")

    return s3


def create_table(table, schema, engine, table_cols):
    if not check_table_exists(table, schema, engine):
        log.info(f"Creating {table} table")
        engine.execute(create_table_statement(table, schema, table_cols))
    else:
        log.info(f"{table} table exists")


def initialise_progress_table(
    progress_table, list_of_files, schema, engine, progress_table_cols, processor_id
):
    progress_df = pd.DataFrame(list_of_files)
    progress_df["state"] = "UNPROCESSED"
    progress_df["process"] = "None"
    progress_df.rename(index={0: "file"})

    if (
        get_row_count(progress_table, schema, engine) > 0
        and get_row_count(progress_table, schema, engine, "UNPROCESSED") == 0
        and get_row_count(progress_table, schema, engine, "READY_TO_PROCESS") == 0
    ):
        truncate_table(progress_table, schema, engine)

    if get_row_count(progress_table, schema, engine) < 1:
        engine.execute(
            create_insert_statement(
                progress_table, schema, progress_table_cols, progress_df
            )
        )

    while get_row_count(progress_table, schema, engine, status="UNPROCESSED") > 0:
        files = get_remaining_files(progress_table, schema, engine, "UNPROCESSED")
        if len(files) > 0:
            file_to_set = files[0]

            update_progress(
                progress_table,
                schema,
                engine,
                file_to_set,
                "READY_TO_PROCESS",
                processor_id,
            )
        # To allow multiple processes to get involved
        if environment == "local":
            secs = 0
        else:
            secs = rnd.uniform(3.00, 5.99)
        time.sleep(secs)


@click.command()
@click.option("-e", "--entities", default="all", help="list of entities to load")
@click.option("-d", "--delay", default="0", help="delay in seconds for process")
@click.option("-v", "--verbose", count=True)
@click.option(
    "-s", "--skip_load", default="false", help="whether to skip the s3 load or not"
)
def main(entities, delay, verbose, skip_load):
    # We add this delay to let the first process get to create table first
    if skip_load == "true":
        log.info(f"Skipping the s3 load step as skip flag has been set")
    else:
        log.info(f"Starting copy of s3 tables into casrec_csv")
        time.sleep(int(delay))
        table_list = entities.split(",")
        chunk_size = config.DEFAULT_CHUNK_SIZE
        bucket_name = f"casrec-migration-{account_name.lower()}"
        setup_logging(log, verbose, log_title, bucket_name)
        env_path = current_path / "../../.env"
        load_dotenv(dotenv_path=env_path)
        host = os.environ.get("DB_HOST")

        account = os.environ["SIRIUS_ACCOUNT"]

        path = os.environ["S3_PATH"]
        progress_table = "migration_progress"
        progress_table_cols = [
            "file",
            "state",
            "processor_id",
        ]
        table_lookup = "table_list"
        table_lookup_cols = ["table_name"]

        ci = os.getenv("CI")

        processor_id = rnd.randint(0, 99999)

        db_conn_string = config.get_db_connection_string("migration")

        engine = create_engine(db_conn_string)

        s3 = get_s3_session(host, account, ci)

        schema = config.schemas["pre_transform"]

        log.info(f"Using bucket {bucket_name}")

        log.info(f"Creating schema {schema}")
        create_schema(schema, engine)

        create_table(progress_table, schema, engine, progress_table_cols)

        create_table(table_lookup, schema, engine, table_lookup_cols)

        list_of_files = get_list_of_files(bucket_name, s3, path, table_list)

        initialise_progress_table(
            progress_table,
            list_of_files,
            schema,
            engine,
            progress_table_cols,
            processor_id,
        )

        while (
            get_row_count(
                progress_table,
                schema,
                engine,
                status="READY_TO_PROCESS",
                processor_id=processor_id,
            )
            > 0
        ):

            file = get_remaining_files(
                progress_table,
                schema,
                engine,
                status="READY_TO_PROCESS",
                processor_id=processor_id,
            )[0]
            update_progress(progress_table, schema, engine, file, status="IN_PROGRESS")
            log.info(f"Processor {processor_id} has picked up {file}")

            file_key = f"{path}/{file}"
            log.info(f'Retrieving "{file_key}" from bucket')
            obj = s3.get_object(Bucket=bucket_name, Key=file_key)
            if file.split(".")[1] == "csv":
                df = pd.read_csv(io.BytesIO(obj["Body"].read()))
            elif file.split(".")[1] == "xlsx":
                df = pd.read_excel(io.BytesIO(obj["Body"].read()), index_col=0)
            else:
                log.info("Unknown file format")
                exit(1)

            table_name = file.split(".")[0].lower()

            df_renamed = df.rename(columns={"Unnamed: 0": "csv_record"})
            columns = [x for x in df_renamed.columns.values]

            # find the last digits
            if table_name[-1].isdigit():
                regex = re.compile("[^a-zA-Z_]")
                table_name = regex.sub("", table_name)

            if table_exists_already(table_name, table_lookup, schema, engine):
                log.info("Multipart file table detected")
            else:
                log.info(
                    f"Table {schema}.{table_name} doesn't exist. Creating table..."
                )
                engine.execute(create_table_statement(table_name, schema, columns))
                log.info(f"Table {schema}.{table_name} created")
                add_lookup_table_row(table_name, table_lookup, schema, engine)

            log.info(f'Inserting records into "{schema}"."{table_name}"')
            if len(df_renamed.index) > 0:
                try:
                    n = chunk_size  # chunk row size
                    list_df = [
                        df_renamed[i : i + n] for i in range(0, df_renamed.shape[0], n)
                    ]

                    for df_chunked in list_df:
                        engine.execute(
                            create_insert_statement(
                                table_name, schema, columns, df_chunked
                            )
                        )
                        log.info(
                            f'Rows inserted into "{schema}"."{table_name}": {get_row_count(table_name, schema, engine)}'
                        )
                    update_progress(
                        progress_table, schema, engine, file, "COMPLETE", processor_id
                    )
                    log.info(f"Processed {file}\n\n")
                except Exception as e:
                    update_progress(
                        progress_table,
                        schema,
                        engine,
                        file,
                        f"FAILED {e}",
                        processor_id,
                    )
                    log.info(f"Failed to process {file}\n\n")
            else:
                log.info(f"No rows to insert for table {table_name}")
                update_progress(
                    progress_table, schema, engine, file, "COMPLETE", processor_id
                )

        log.info(f"Processor {processor_id} has finished processing")


if __name__ == "__main__":
    main()
