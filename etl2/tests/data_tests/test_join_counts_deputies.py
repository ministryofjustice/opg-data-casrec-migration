import pandas as pd
import psycopg2


def test_joins_deputies():

    casrec_db_connection = psycopg2.connect(
        "host=localhost port=6666 "
        "dbname=casrecmigration "
        "user=casrec "
        "password=casrec"
    )

    etl1_query = """
        select
            "Dep Forename" as firstname,
            "Dep Surname" as surname,
           (select count(*)
                from etl1.deputyship
                inner join etl1."order"
                    on etl1.deputyship."Case" = etl1."order"."Case"
                    and etl1.deputyship."Order No" = etl1."order"."Order No"
                where etl1.deputyship."Deputy No" = deputy."Deputy No") as cases
        from etl1.deputy as deputy;
    """

    etl2_query = """
        select
               persons.firstname,
               persons.surname,
               (select count(*) from etl2.order_deputy as order_deputy where order_deputy.deputy_id = persons.id) as cases
        from etl2.persons as persons where persons.type = 'actor_deputy'
    """

    etl1_df = pd.read_sql_query(etl1_query, casrec_db_connection)
    etl2_df = pd.read_sql_query(etl2_query, casrec_db_connection)

    match = etl1_df.equals(etl2_df)

    if match:
        print("The two queries match!")
    else:
        merged = etl1_df.merge(etl2_df, indicator=True, how="outer")
        print(merged.to_markdown())

    assert match is True
