import pandas as pd
import psycopg2


def test_joins_deputies(get_config):
    config = get_config

    etl1_query = f"""
        select
            "Dep Forename" as firstname,
            "Dep Surname" as surname,
           (select count(*)
                from {config.etl1_schema}.deputyship
                inner join {config.etl1_schema}."order"
                    on {config.etl1_schema}.deputyship."Case" = {config.etl1_schema}."order"."Case"
                    and {config.etl1_schema}.deputyship."Order No" = {config.etl1_schema}."order"."Order No"
                where {config.etl1_schema}.deputyship."Deputy No" = deputy."Deputy No") as cases
        from {config.etl1_schema}.deputy as deputy;
    """

    etl2_query = f"""
        select
               persons.firstname,
               persons.surname,
               (select count(*) from {config.etl2_schema}.order_deputy as order_deputy where order_deputy.deputy_id = persons.id) as cases
        from {config.etl2_schema}.persons as persons
        where persons.type = 'actor_deputy'
    """

    etl1_df = pd.read_sql_query(etl1_query, config.connection_string)
    etl2_df = pd.read_sql_query(etl2_query, config.connection_string)

    match = etl1_df.equals(etl2_df)

    if match:
        print("The two queries match!")
    else:
        merged = etl1_df.merge(etl2_df, indicator=True, how="outer")
        print(merged.to_markdown())

    assert match is True
