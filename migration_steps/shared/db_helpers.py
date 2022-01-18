import os
import re
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
        and schema_name not in ({preserve_schemas}'public', 'information_schema');
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


def schema_exists(conn, schema):
    sql = f"""SELECT EXISTS (
          SELECT FROM information_schema.schemata WHERE schema_name = '{schema}'
          );"""
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchone()[0]


def copy_schema(
    log, sql_path, config, from_db, from_schema, to_db, to_schema, structure_only=False
):
    from_config = config.db_config[from_db]
    to_config = config.db_config[to_db]

    log.info(f'{from_config["name"]}.{from_schema} -> {to_config["name"]}.{to_schema}')

    from_conn = psycopg2.connect(config.get_db_connection_string(from_db))
    from_cursor = from_conn.cursor()

    if from_schema != to_schema:
        log.debug("Rename schema beforehand to avoid search&replace in the dump file")
        sql = f"""
                DO $$
                BEGIN
                    IF EXISTS(
                        SELECT schema_name
                        FROM information_schema.schemata
                        WHERE schema_name = '{to_schema}'
                      )
                    THEN
                        EXECUTE 'ALTER SCHEMA {to_schema} RENAME TO temp_renamed_{to_schema}';
                    END IF;

                    EXECUTE 'ALTER SCHEMA {from_schema} RENAME TO {to_schema}';
                END
                $$;
            """
        from_cursor.execute(sql)
        from_conn.commit()

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
                to_schema,  # schema has already been renamed in the source DB
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
                to_schema,  # schema has already been renamed in the source DB
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

    role_name_regex = re.compile(r"^(ALTER.*OWNER TO )%s(;)$" % from_config["user"])
    owner_regex = re.compile(r"^(-- Name:.*; Owner: )%s$" % from_config["user"])

    with fileinput.FileInput(schema_dump, inplace=True) as file:
        for line in file:
            line = line.replace(
                f"CREATE SCHEMA {to_schema};",
                f"""
                DROP SCHEMA IF EXISTS {to_schema} CASCADE;
                CREATE SCHEMA {to_schema};
                SET search_path TO {to_schema},public;
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                """
            )
            line = role_name_regex.sub(r"\1%s\2" % to_config["user"], line)
            line = owner_regex.sub(r"\1%s" % to_config["user"], line)
            print(line, end="")

    log.debug(f"Saved to file: {schema_dump}")

    if from_schema != to_schema:
        # restore schema names in the source DB back to what they were
        log.debug("Source DB cleanup")
        sql = f"""
            DO $$
            BEGIN
                EXECUTE 'ALTER SCHEMA {to_schema} RENAME TO {from_schema}';
                
                IF EXISTS(
                    SELECT schema_name
                    FROM information_schema.schemata
                    WHERE schema_name = 'temp_renamed_{to_schema}'
                  )
                THEN
                    EXECUTE 'ALTER SCHEMA temp_renamed_{to_schema} RENAME TO {to_schema}';
                END IF;
            END
            $$;
        """
        from_cursor.execute(sql)
        from_conn.commit()

    from_cursor.close()

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


def replace_panda_nulls(x):
    full_replacements = [
        ("nan", ""),
        ("NaT", ""),
        ("<NA>", ""),
        ("None", ""),
    ]

    substring_replacements = [("'", "''"), ("%", "%%")]

    x = str(x)
    for old_value, new_value in full_replacements:
        x = re.sub(rf"^{old_value}[ ]?$", new_value, x)

    for old_value, new_value in substring_replacements:
        x = x.replace(old_value, new_value)

    return x


def replace_with_sql_friendly_chars(row_as_list):
    row = [str(replace_panda_nulls(x)) for x in row_as_list]

    return row


def replace_with_sql_friendly_chars_single(val):
    return str(replace_panda_nulls(val))
