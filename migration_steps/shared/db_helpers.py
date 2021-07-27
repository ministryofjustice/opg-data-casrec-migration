import os
import sys

import psycopg2
import pandas as pd
import numpy as np
import sh
import fileinput
from sqlalchemy import create_engine
from psycopg2.extensions import register_adapter, AsIs

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)


def delete_all_schemas(log, conn, preserve_schemas):
    cursor = conn.cursor()
    if preserve_schemas != "":
        schemas_list = preserve_schemas.split(",")
        preserve_schemas = "'" + "', '".join(schemas_list) + "', "
        for preserve_schema in schemas_list:
            log.info(f"Schema: {preserve_schema} not dropped")
            if preserve_schema == "casrec_csv":
                drop_statement = """
                    DROP TABLE IF EXISTS "casrec_csv"."migration_progress";
                    DROP TABLE IF EXISTS "casrec_csv"."table_list";
                """
                cursor.execute(drop_statement)
                conn.commit()
    get_schemas_statement = f"""
        SELECT schema_name
        FROM
        information_schema.schemata
        WHERE
        schema_name not like 'pg_%'
        and schema_name not in ({preserve_schemas}'public', 'information_schema', 'fees');
    """
    cursor.execute(get_schemas_statement)
    schemas = ""
    for schema in cursor:
        schemas = schemas + schema[0] + ", "
    schemas = schemas[:-2]
    if len(schemas) > 0:
        delete_schemas_statement = f"""
        DROP SCHEMA {schemas} CASCADE;
        """
        log.info(f"Schemas {schemas} dropped")
        log.debug(f'Running "{delete_schemas_statement}"')
        cursor.execute(delete_schemas_statement)
        conn.commit()
    cursor.close()


def create_schema(log, engine, schema):
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
        log.debug(f"Schema {schema} already exists\n\n")


def copy_schema(
    log, sql_path, from_config, from_schema, to_config, to_schema, structure_only=False
):
    log.info(f'{from_config["name"]}.{from_schema} -> {to_config["name"]}.{to_schema}')

    log.debug("Dump")
    os.environ["PGPASSWORD"] = from_config["password"]
    if structure_only:
        schema_dump = (
            sql_path
            / "schemas"
            / f'{from_config["name"]}_{from_schema}_structure_only.sql'
        )
        print(
            sh.pg_dump(
                "-U",
                from_config["user"],
                "-n",
                from_schema,
                "-h",
                from_config["host"],
                "-p",
                from_config["port"],
                "-s",
                from_config["name"],
                _err_to_out=True,
                _out=str(schema_dump),
            ),
            end="",
        )
    else:
        schema_dump = sql_path / "schemas" / f'{from_config["name"]}_{from_schema}.sql'
        print(
            sh.pg_dump(
                "-U",
                from_config["user"],
                "-n",
                from_schema,
                "-h",
                from_config["host"],
                "-p",
                from_config["port"],
                from_config["name"],
                _err_to_out=True,
                _out=str(schema_dump),
            ),
            end="",
        )

    log.debug("Modify")
    with fileinput.FileInput(str(schema_dump), inplace=True) as file:
        for line in file:
            print(line.replace(from_schema, to_schema), end="")

    with fileinput.FileInput(schema_dump, inplace=True) as file:
        for line in file:
            print(
                line.replace(
                    "CREATE SCHEMA " + to_schema,
                    f"DROP SCHEMA IF EXISTS {to_schema} CASCADE; CREATE SCHEMA {to_schema}; "
                    f'set search_path to {to_schema},public; CREATE EXTENSION IF NOT EXISTS "uuid-ossp"',
                ),
                end="",
            )

    # change role name
    with fileinput.FileInput(str(schema_dump), inplace=True) as file:
        for line in file:
            print(
                line.replace(
                    f'TO {from_config["user"]}',
                    f'TO {to_config["user"]}',
                ),
                end="",
            )
    with fileinput.FileInput(str(schema_dump), inplace=True) as file:
        for line in file:
            print(
                line.replace(
                    f'Owner: {from_config["user"]}',
                    f'Owner: {to_config["user"]}',
                ),
                end="",
            )
    log.debug(f"Saved to file: {schema_dump}")

    log.debug("Import")
    os.environ["PGPASSWORD"] = to_config["password"]
    schemafile = open(schema_dump, "r")
    print(
        sh.psql(
            "-U",
            to_config["user"],
            "-h",
            to_config["host"],
            "-p",
            to_config["port"],
            "--quiet",
            "-o",
            "/dev/null",
            to_config["name"],
            _err_to_out=True,
            _in=schemafile,
        ),
        end="",
    )


def execute_sql_file(sql_path, filename, conn, schema="public"):
    cursor = conn.cursor()
    sql_file = open(sql_path / filename, "r")

    try:
        cursor.execute(sql_file.read().replace("{schema}", str(schema)))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        os._exit(1)
    cursor.close()


def create_from_template(sql_path, template_filename, write_filename, search, replace):
    template = open(sql_path / template_filename, "r")
    write_file = open(sql_path / write_filename, "w+")
    for line in template:
        write_file.write(line.replace(search, str(replace)))
    template.close()
    write_file.close()


def execute_generated_sql(sql_path, template_filename, search, replace, conn):
    sql_filename = template_filename.replace("template.", "")
    create_from_template(sql_path, template_filename, sql_filename, search, replace)
    execute_sql_file(sql_path, sql_filename, conn)
    os.remove(sql_path / sql_filename)
    conn.commit()


def result_from_sql_file(sql_path, filename, conn):
    cursor = conn.cursor()
    sql_file = open(sql_path / filename, "r")
    cursor.execute(sql_file.read())
    result = cursor.fetchone()[0]
    cursor.close()
    return result


def df_from_sql_file(sql_path, filename, conn, schema="public"):
    sql_file = open(sql_path / filename, "r")
    sql = sql_file.read().replace("{schema}", str(schema))
    return pd.read_sql_query(sql, con=conn, index_col=None)


def execute_insert(conn, df, table):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ",".join(list(df.columns))

    cursor = conn.cursor()
    row_str_template = ",".join(["%s"] * len(df.columns))
    values = [
        cursor.mogrify("(" + row_str_template + ")", tup).decode("utf8")
        for tup in tuples
    ]
    query = "INSERT INTO %s(%s) VALUES " % (table, cols) + ",".join(values)

    try:
        cursor.execute(query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        os._exit(1)
    cursor.close()


def nan_to_null(
    f,
    _NULL=psycopg2.extensions.AsIs("NULL"),
    _NaN=np.NaN,
    _Float=psycopg2.extensions.Float,
):
    if f is not _NaN:
        return _Float(f)
    return _NULL


def execute_update(conn, df, table, pk_col):
    # Just ensure that the primary key is the first column of the dataframe
    psycopg2.extensions.register_adapter(float, nan_to_null)
    psycopg2.extensions.register_adapter(int, nan_to_null)

    cols = list(df.columns)
    try:
        cols.remove(pk_col)
    except ValueError:
        pass
    colstring = "=%s,".join(cols)
    colstring += "=%s"
    update_template = f"UPDATE {table} SET {colstring} WHERE {pk_col}="

    cursor = conn.cursor()

    for vals in df.to_numpy():
        query = cursor.mogrify(update_template + str(vals[0]), vals[1:]).decode("utf8")
        cursor.execute(query)

    conn.commit()
    cursor.close()
