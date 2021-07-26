import random

import psycopg2
from sqlalchemy import create_engine
import pandas as pd


def get_max_value(table, column, db_config):
    connection_string = db_config["sirius_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = f"SELECT max({column}) from {db_config['sirius_schema']}.{table};"

    try:
        cursor.execute(query)
        max_id = cursor.fetchall()[0][0]
        if max_id:
            return max_id
        else:
            return 0

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"error: {error}")
        conn.rollback()
        cursor.close()
        return 0


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


def insert_client_data_into_sirius(db_config, source_db_engine, sirius_db_engine):

    id = get_max_value(table="persons", column="id", db_config=db_config)
    uid = get_max_value(table="persons", column="uid", db_config=db_config)
    query = f"""
        SELECT
            row_number() over () + {id} as id,
            "Case" as caserecnumber,
            "Forename"||' EXISTING DATA' as firstname,
            "Surname"||' EXISTING DATA' as surname,
            false as correspondencebypost,
            false as correspondencebyphone,
            false as correspondencebyemail,
            row_number() over () + {uid} as uid,
            'actor_client' as type,
            'SKELETON' as clientsource,
            false as correspondencebywelsh
        from {db_config['source_schema']}.pat;
    """

    data = pd.read_sql_query(query, con=source_db_engine, index_col=None)

    columns = [
        "id",
        "caserecnumber",
        "firstname",
        "surname",
        "correspondencebypost",
        "correspondencebyphone",
        "correspondencebyemail",
        "uid",
        "type",
        "clientsource",
        "correspondencebywelsh",
    ]

    insert_statement = create_insert_statement(
        table_name="persons",
        schema=db_config["sirius_schema"],
        columns=columns,
        df=data,
    )

    sirius_db_engine.execute(insert_statement)


def insert_client_address_data_into_sirius(
    db_config, source_db_engine, sirius_db_engine
):
    id = get_max_value(table="addresses", column="id", db_config=db_config)

    insert_statement = f"""
        INSERT INTO addresses (id, person_id, town)
        SELECT
            row_number() over () + {id} as id,
            id as person_id,
            'EXISTING DATA'
        from persons where clientsource = 'SKELETON';
    """
    print(insert_statement)

    sirius_db_engine.execute(insert_statement)


def insert_skeleton_data(db_config):
    source_db_engine = create_engine(db_config["db_connection_string"])
    sirius_db_engine = create_engine(db_config["sirius_db_connection_string"])

    # client_persons
    insert_client_data_into_sirius(
        db_config=db_config,
        sirius_db_engine=sirius_db_engine,
        source_db_engine=source_db_engine,
    )
    insert_client_address_data_into_sirius(
        db_config=db_config,
        sirius_db_engine=sirius_db_engine,
        source_db_engine=source_db_engine,
    )
