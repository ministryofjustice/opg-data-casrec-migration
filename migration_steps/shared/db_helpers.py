import os
import psycopg2
import pandas as pd
import numpy as np
import sh
import fileinput

from psycopg2.extensions import register_adapter, AsIs

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)


def copy_schema(
    log, sql_path, from_config, from_schema, to_config, to_schema, structure_only=False
):
    log.info(
        f'Copying {from_config["name"]}.{from_schema} to {to_config["name"]}.{to_schema}'
    )

    log.info("Dump")
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
            )
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
            )
        )

    log.info("Modify")
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
                    f'OWNER TO {from_config["user"]};',
                    f'OWNER TO {to_config["user"]};',
                ),
                end="",
            )

    log.info("Import")
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
            to_config["name"],
            _err_to_out=True,
            _in=schemafile,
        )
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
        return 1
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
        return 1
    cursor.close()


def execute_update(conn, df, table, pk_col):
    # Just ensure that the primary key is the first column of the dataframe

    cols = list(df.columns)
    cols.remove(pk_col)
    colstring = "=%s,".join(cols)
    colstring += "=%s"
    update_template = f"UPDATE {table} SET {colstring} WHERE {pk_col}="

    cursor = conn.cursor()

    for vals in df.to_numpy():
        query = cursor.mogrify(update_template + str(vals[0]), vals[1:]).decode("utf8")
        cursor.execute(query)

    conn.commit()
    cursor.close()
