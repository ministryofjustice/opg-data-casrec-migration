import pandas as pd
import psycopg2
import pytest

from config import LocalConfig


@pytest.mark.skip(reason="not required")
def test_joins_clients(get_config):
    config = get_config

    etl1_query = f"""
        select
           "Case" as caserecnumber,
           "Forename" as firstname,
           "Surname" as surname,
           1 as address_count,
           (select count(*) from {config.etl1_schema}."order" where "Case" = etl1.pat."Case") as cases,
           (select count(*) from {config.etl1_schema}."remarks" where "Case" = etl1.pat."Case") as notes
        from {config.etl1_schema}.pat;
    """

    etl2_query = f"""
        select
           persons.caserecnumber,
           persons.firstname,
           persons.surname,
           (select count(*) from {config.etl2_schema}.addresses as addresses
                where cast(addresses.person_id as int) = persons.id) as address_count,
           (select count(*) from {config.etl2_schema}.person_caseitem as person_caseitem
                where cast(person_caseitem.person_id as int) = persons.id) as cases,
           (select count(*) from {config.etl2_schema}.person_note as person_note
                where cast(person_note.person_id as int) = persons.id) as notes
        from {config.etl2_schema}.persons as persons
        where persons.type = 'actor_client'
    """

    print(etl1_query)
    print(etl2_query)

    etl1_df = pd.read_sql_query(etl1_query, config.connection_string)
    etl2_df = pd.read_sql_query(etl2_query, config.connection_string)

    match = etl1_df.equals(etl2_df)

    if match:
        print("The two queries match!")
    else:
        merged = etl1_df.merge(etl2_df, indicator=True, how="outer")
        print(merged.to_markdown())

    assert match is True


def test_path():
    import os

    print(os.environ.get("PYTHONPATH"))
