import pandas as pd
import io
import os
import re
import argparse
from sqlalchemy import create_engine
import boto3
import random as rnd
from pathlib import Path
from dotenv import load_dotenv


def get_list_of_files(bucket_name, s3, path, tables):
    resp = s3.list_objects_v2(Bucket=bucket_name)
    files_in_bucket = []
    files_to_process = []

    for obj in resp["Contents"]:
        file_folder = obj["Key"]
        print(obj["Key"])
        folder = file_folder.split("/")[0]
        file = file_folder.split("/")[1]
        if folder == path and len(file) > 1:
            print(f"file is: {file}")
            files_in_bucket.append(file)

    if tables[0].lower() == "all":
        print("Will process all files")
        files_to_process.extend(files_in_bucket)
    else:
        print("Bring back specific entities")
        for bucket_file in files_in_bucket:
            if bucket_file.split(".")[0].lower() in tables:
                files_to_process.append(bucket_file)

    print(f"Total files returned: {len(files_in_bucket)}")
    return files_to_process


def get_remaining_files(table_name, schema_name, engine):
    remaining_files = f"""
    SELECT file
    FROM \"{schema_name}\".\"{table_name}\"
    WHERE state = 'UNPROCESSED';
    """

    files = engine.execute(remaining_files)
    file_list = []
    for r in files:
        file_list.append(r.values()[0])
        return file_list


def update_progress(table_name, schema_name, engine, file, status="IN_PROGRESS"):
    row_update = f"""
    UPDATE \"{schema_name}\".\"{table_name}\"
    SET state = '{status}'
    WHERE file = '{file}';
    """

    response = engine.execute(row_update)
    if response.rowcount > 0:
        print(f"Updated {file} to {status}")


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
    create_statement = f'CREATE TABLE "{schema}"."{table_name}" ('
    for i, col in enumerate(columns):
        create_statement += f'"{col}" text'
        if i + 1 < len(columns):
            create_statement += ","
    create_statement += "); \n\n\n"

    return create_statement


def truncate_table(table_name, schema, engine):
    print(f"Truncating table {schema}.{table_name}")
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


def get_row_count(table_name, schema_name, engine, status=None):
    get_count_statement = f"""
        SELECT COUNT(*) FROM {schema_name}.{table_name}
        """

    if status is not None:
        get_count_statement += f" WHERE state = '{status}'"

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
        print(f"Creating schema {schema}...")
        create_schema_sql = f"CREATE SCHEMA {schema} AUTHORIZATION casrec;"
        engine.execute(create_schema_sql)
        print(f"Schema {schema} created\n\n")
    else:
        print(f"Schema {schema} already exists\n\n")


def dev_sirius_session():

    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]
    print(f"Current users account: {account_id}")

    role_to_assume = "arn:aws:iam::288342028542:role/sirius-ci"
    response = client.assume_role(
        RoleArn=role_to_assume, RoleSessionName="assumed_role"
    )

    session = boto3.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )

    return session


def main():
    parser = argparse.ArgumentParser(description="Load into casrec.")
    parser.add_argument(
        "--entities", default="all", help="list of entities to load",
    )
    parser.add_argument(
        "--chunk", default="50000", help="chunk size",
    )
    args = parser.parse_args()

    table_list = args.entities.split(",")
    chunk_size = int(args.chunk)

    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    env_path = current_path / "../../.env"
    load_dotenv(dotenv_path=env_path)

    password = os.environ["DB_PASSWORD"]
    db_host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    name = os.environ["DB_NAME"]
    environment = os.environ["ENVIRONMENT"]
    path = os.environ["S3_PATH"]
    progress_table = "migration_progress"
    progress_table_cols = [
        "file",
        "state",
    ]
    ci = os.getenv("CI")

    processor_id = rnd.randint(0, 99999)

    databases = {
        "casrecmigration": {
            "NAME": name,
            "USER": "casrec",
            "PASSWORD": password,
            "HOST": db_host,
            "PORT": port,
        },
    }

    # choose the database to use
    db = databases["casrecmigration"]

    # construct an engine connection string
    engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(  # pragma: allowlist secret
        user=db["USER"],
        password=db["PASSWORD"],
        host=db["HOST"],
        port=db["PORT"],
        database=db["NAME"],
    )

    engine = create_engine(engine_string)

    s3_session = boto3.session.Session()
    if environment == "local":
        if db_host == "localhost":
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
        s3_session = dev_sirius_session()
        s3 = s3_session.client("s3")
    else:
        s3 = s3_session.client("s3")

    bucket_name = f"casrec-migration-{environment}"
    schema = "etl1"

    print(f"Using bucket {bucket_name}")

    print(f"Creating schema {schema}")
    create_schema(schema, engine)

    if not check_table_exists(progress_table, schema, engine):
        print(f"Creating progress table")
        engine.execute(
            create_table_statement(progress_table, schema, progress_table_cols)
        )
    else:
        print("Progress table exists")

    list_of_files = get_list_of_files(bucket_name, s3, path, table_list)

    progress_df = pd.DataFrame(list_of_files)
    progress_df["state"] = "UNPROCESSED"
    progress_df.rename(index={0: "file"})

    if (
        get_row_count(progress_table, schema, engine) > 0
        and get_row_count(progress_table, schema, engine, "UNPROCESSED") == 0
    ):
        truncate_table(progress_table, schema, engine)

    if get_row_count(progress_table, schema, engine) < 1:
        engine.execute(
            create_insert_statement(
                progress_table, schema, progress_table_cols, progress_df
            )
        )

    prev_table = ""
    while get_row_count(progress_table, schema, engine, status="UNPROCESSED") > 0:

        file = get_remaining_files(progress_table, schema, engine)[0]
        update_progress(progress_table, schema, engine, file, status="IN_PROGRESS")
        print(f"Processor {processor_id} has picked up {file}")

        file_key = f"{path}/{file}"
        print(f'Retrieving "{file_key}" from bucket')
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        if file.split(".")[1] == "csv":
            df = pd.read_csv(io.BytesIO(obj["Body"].read()))
        elif file.split(".")[1] == "xlsx":
            df = pd.read_excel(io.BytesIO(obj["Body"].read()), index_col=0)
        else:
            print("Unknown file format")
            exit(1)

        table_name = file.split(".")[0].lower()

        df_renamed = df.rename(columns={"Unnamed: 0": "Record"})

        columns = [x for x in df_renamed.columns.values]

        # find the last digits
        if table_name[-1].isdigit():
            regex = re.compile("[^a-zA-Z]")
            table_name = regex.sub("", table_name)

        if table_name == prev_table:
            print("Multpart file table detected")
        else:
            if check_table_exists(table_name, schema, engine):
                truncate_table(table_name, schema, engine)
            else:
                print(f"Table {schema}.{table_name} doesn't exist. Creating table...")
                engine.execute(create_table_statement(table_name, schema, columns))
                print(f"Table {schema}.{table_name} created")

        prev_table = table_name

        print(f'Inserting records into "{schema}"."{table_name}"')
        if len(df_renamed.index) > 0:
            n = chunk_size  # chunk row size
            list_df = [df_renamed[i : i + n] for i in range(0, df_renamed.shape[0], n)]

            for df_chunked in list_df:
                engine.execute(
                    create_insert_statement(table_name, schema, columns, df_chunked)
                )
                print(
                    f'Rows inserted into "{schema}"."{table_name}": {get_row_count(table_name, schema, engine)}'
                )
        else:
            print(f"No rows to insert for table {table_name}")

        update_progress(progress_table, schema, engine, file, status="COMPLETE")
        print(f"Processed {file}\n\n")

    print(f"Processor {processor_id} has finished processing")


if __name__ == "__main__":
    main()
