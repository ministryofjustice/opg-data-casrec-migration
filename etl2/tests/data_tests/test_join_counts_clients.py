import pandas as pd
import psycopg2


def test_joins_clients():

    casrec_db_connection = psycopg2.connect(
        "host=localhost port=6666 "
        "dbname=casrecmigration "
        "user=casrec "
        "password=casrec"
    )

    etl1_query = (
        "select "
        '"Case" as caserecnumber, "Forename" as firstname, "Surname" as surname, '
        "1 as address_count, "
        '(select count(*) from etl1."order" where "Case" = etl1.pat."Case") as '
        "cases, "
        '(select count(*) from etl1."remarks" where "Case" = etl1.pat."Case") as notes '
        "from etl1.pat;"
    )

    etl2_query = (
        "select persons.caserecnumber, persons.firstname, persons.surname, "
        "(select count(*) from etl2.addresses as addresses where addresses.person_id = persons.id) as address_count, "
        "(select count(*) from etl2.person_caseitem as person_caseitem where person_caseitem.person_id = persons.id) as cases, "
        "(select count(*) from etl2.person_note as person_note where "
        "person_note.person_id = persons.id) as notes "
        "from etl2.persons as persons "
        "where persons.type = 'actor_client'"
    )

    # print(etl1_query)
    # print(etl2_query)

    etl1_df = pd.read_sql_query(etl1_query, casrec_db_connection)
    etl2_df = pd.read_sql_query(etl2_query, casrec_db_connection)

    match = etl1_df.equals(etl2_df)

    if match:
        print("The two queries match!")
    else:
        merged = etl1_df.merge(etl2_df, indicator=True, how="outer")
        print(merged.to_markdown())

    assert match is True
