import logging

import pandas as pd

from data_tests.helpers import (
    get_data_from_query,
    get_merge_col_data_as_list,
)

log = logging.getLogger("root")


def test_order_deputy_joins(
    test_config,
):

    config = test_config
    source_query = f"""
        SELECT distinct caserecnumber from transform.cases;
    """

    source_sample_df = get_data_from_query(
        query=source_query, config=config, sample=True
    )

    assert source_sample_df.shape[0] > 0

    sample_caserefs = get_merge_col_data_as_list(
        df=source_sample_df, column_name="caserecnumber"
    )

    result = {"total": 0, "passed": 0, "failed": []}
    for single_case in sample_caserefs:
        result["total"] += 1
        transformed_query = f"""
            select
                cases.caserecnumber,
                persons.firstname, persons.surname
            from transform.cases
            left outer join transform.order_deputy on cases.id = order_deputy.order_id
            left outer join transform.persons on persons.id = order_deputy.deputy_id
            where cases.caserecnumber = '{single_case}'
            order by cases.caserecnumber, firstname, surname;
        """

        transformed_df = pd.read_sql_query(
            transformed_query, config.get_db_connection_string(db="migration")
        )

        casrec_query = f"""
            select
                "order"."Case" as caserecnumber,
                   deputy."Dep Forename" as firstname,
                   deputy."Dep Surname" as surname
            from casrec_csv.order
            left outer join casrec_csv.deputyship on "order"."Order No" = deputyship."Order No"
            left outer join casrec_csv.deputy on deputyship."Deputy No" = deputy."Deputy No"
            where "order"."Case" = '{single_case}'
            order by "order"."Case", "Dep Forename", "Dep Surname";
        """

        casrec_df = pd.read_sql_query(
            casrec_query, config.get_db_connection_string(db="migration")
        )

        try:
            pd.testing.assert_frame_equal(transformed_df, casrec_df)
            result["passed"] += 1
        except AssertionError:
            result["failed"].append(single_case)

    print(f"result: {round(result['passed']/result['total']*100, 2)}% passed")
    if len(result["failed"]) > 0:
        print(f"Failed caserecnumbers: {', '.join(result['failed'])}")

    assert len(result["failed"]) == 0
