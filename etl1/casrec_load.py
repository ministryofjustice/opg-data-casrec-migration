import pandas as pd
import io
import os
import argparse
from sqlalchemy import create_engine
import boto3


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
        print("Bring back specific tables")
        for bucket_file in files_in_bucket:
            if bucket_file.split(".")[0].lower() in tables:
                files_to_process.append(bucket_file)

    print(f"Total files returned: {len(files_in_bucket)}")
    return files_to_process


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


def get_rows_inserted(table_name, schema_name, engine):
    get_count_statement = f"""
        SELECT COUNT(*) FROM {schema_name}.{table_name};
        """
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
        create_schema_sql = "CREATE SCHEMA etl1 AUTHORIZATION casrec;"
        engine.execute(create_schema_sql)
        print(f"Schema {schema} created\n\n")
    else:
        print(f"Schema {schema} already exists\n\n")


def main():
    parser = argparse.ArgumentParser(description="Load into casrec.")
    parser.add_argument(
        "--tables", default="all", help="list of tables to load",
    )
    parser.add_argument(
        "--chunk", default="50000", help="chunk size",
    )
    args = parser.parse_args()

    table_list = args.tables.split(",")
    chunk_size = int(args.chunk)

    password = os.environ["DB_PASSWORD"]
    db_host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    name = os.environ["DB_NAME"]
    environment = os.environ["ENVIRONMENT"]
    path = os.environ["S3_PATH"]

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

    bucket_name = f"casrec-migration-{environment}"
    schema = "etl1"

    print(f"Creating schema {schema}")
    create_schema(schema, engine)

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
    else:
        s3 = s3_session.client("s3")

    for file in get_list_of_files(bucket_name, s3, path, table_list):
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

        if check_table_exists(table_name, schema, engine):
            print(f"Truncating table {schema}.{table_name}")
            truncate_statement = f'TRUNCATE TABLE "{schema}"."{table_name}"'
            engine.execute(truncate_statement)
        else:
            print(f"Table {schema}.{table_name} doesn't exist. Creating table...")
            engine.execute(create_table_statement(table_name, schema, columns))
            print(f"Table {schema}.{table_name} created")

        print(f'Inserting records into "{schema}"."{table_name}"')
        if len(df_renamed.index) > 0:
            n = chunk_size  # chunk row size
            list_df = [df_renamed[i : i + n] for i in range(0, df_renamed.shape[0], n)]

            for df_chunked in list_df:
                engine.execute(
                    create_insert_statement(table_name, schema, columns, df_chunked)
                )
                print(
                    f'Rows inserted into "{schema}"."{table_name}": {get_rows_inserted(table_name, schema, engine)}\n\n'
                )
        else:
            print(f"No rows to insert for table {table_name}")


if __name__ == "__main__":
    main()
