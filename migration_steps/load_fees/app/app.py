import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import pandas as pd
import io
from sqlalchemy import create_engine
import boto3
import custom_logger
from dotenv import load_dotenv
from helpers import get_config, log_title
import logging

environment = os.environ.get("ENVIRONMENT")
account_name = os.environ.get("ACCOUNT_NAME")
config = get_config(environment)
config.custom_log_level()
verbosity_levels = config.verbosity_levels
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())
bucket_name = f"casrec-migration-{account_name.lower()}"
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)
host = os.environ.get("DB_HOST")
account = os.environ["SIRIUS_ACCOUNT"]
s3_path = "fees"
ci = os.getenv("CI")
schema = "fees"
verbose = True
chunk_size = 5000


def get_list_of_files(bucket_name, s3, path):
    resp = s3.list_objects_v2(Bucket=bucket_name)
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
                files_to_process.append(file)

    log.info(f"Total files returned: {len(files_to_process)}")
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

    role_to_assume = f"arn:aws:iam::{account}:role/sirius-ci"
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


def main():
    setup_logging(log, verbose, log_title, bucket_name)
    log.info(f"Starting copy of fees s3 csvs into fees schema")

    db_conn_string = config.get_db_connection_string("migration")
    engine = create_engine(db_conn_string)
    s3 = get_s3_session(host, account, ci)

    log.info(f"Using bucket {bucket_name}")

    log.info(f"Creating schema {schema}")
    create_schema(schema, engine)

    log.info(f"Getting list of files in bucket")
    list_of_files = get_list_of_files(bucket_name, s3, s3_path)

    for file in list_of_files:

        file_key = f"{s3_path}/{file}"

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

        engine.execute(create_table_statement(table_name, schema, columns))
        log.info(f"Table {schema}.{table_name} created")

        truncate_table(table_name, schema, engine)

        log.info(f'Inserting records into "{schema}"."{table_name}"')

        if len(df_renamed.index) > 0:
            try:
                n = chunk_size  # chunk row size
                list_df = [
                    df_renamed[i : i + n] for i in range(0, df_renamed.shape[0], n)
                ]

                for df_chunked in list_df:
                    engine.execute(
                        create_insert_statement(table_name, schema, columns, df_chunked)
                    )
                    log.info(
                        f'Rows inserted into "{schema}"."{table_name}": {get_row_count(table_name, schema, engine)}'
                    )
                log.info(f"Processed {file}\n\n")
            except Exception:
                log.info(f"Failed to process {file}\n\n")
        else:
            log.info(f"No rows to insert for table {table_name}")


if __name__ == "__main__":
    main()