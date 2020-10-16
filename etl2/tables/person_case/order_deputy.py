import psycopg2
import pandas as pd


definition = {
    "destination_table_name": "order_deputy",
}


def insert_order_deputy(config, etl2_db):

    persons_query = (
        f'select "id", "c_deputy_no" from etl2.persons '
        f"where \"type\" = 'actor_deputy';"
    )
    persons_df = pd.read_sql_query(persons_query, config.connection_string)

    deputyship_query = (
        f'select "Deputy No", "Case", "Order No" '
        f"from {config.etl1_schema}.deputyship;"
    )

    deuptyship_df = pd.read_sql_query(deputyship_query, config.connection_string)

    person_with_case_df = persons_df.merge(
        deuptyship_df, how="inner", left_on="c_deputy_no", right_on="Deputy No"
    )

    # person_with_case_df['caserecnumber'] = person_with_case_df['Case']
    # person_with_case_df = person_with_case_df.drop(columns=['Case', 'Deputy No'])

    cases_query = f'select "id", "caserecnumber", "c_order_no" from etl2.cases;'
    cases_df = pd.read_sql_query(cases_query, config.connection_string)

    order_deputy_df = cases_df.merge(
        person_with_case_df,
        how="inner",
        left_on=["caserecnumber", "c_order_no"],
        right_on=["Case", "Order No"],
        suffixes=["_case", "_person"],
    )

    order_deputy_df = order_deputy_df.drop(columns=["caserecnumber"])
    order_deputy_df = order_deputy_df.rename(
        columns={"id_case": "case_id", "id_person": "deputy_id"}
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=order_deputy_df
    )
