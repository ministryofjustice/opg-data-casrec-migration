import logging

import pandas as pd

from data_tests.helpers import (
    get_data_from_query,
    get_merge_col_data_as_list,
)

log = logging.getLogger("root")


def test_deputy_address_joins(
    test_config,
):

    config = test_config
    source_query = f"""
        SELECT distinct surname from transform.persons where casrec_mapping_file_name = 'deputy_persons_mapping';
    """

    source_sample_df = get_data_from_query(
        query=source_query, config=config, sample=True
    )

    assert source_sample_df.shape[0] > 0

    sample_caserefs = get_merge_col_data_as_list(
        df=source_sample_df, column_name="surname"
    )

    result = {"total": 0, "passed": 0, "failed": []}
    for single_case in sample_caserefs:
        result["total"] += 1
        transformed_query = f"""
            select
                persons.firstname, persons.surname,
                   addresses.postcode
            from transform.persons
            left outer join transform.addresses on persons.id = addresses.person_id
            where persons.casrec_mapping_file_name = 'deputy_persons_mapping'
            and persons.surname = '{single_case}'
            order by firstname, surname, postcode;
        """

        transformed_df = pd.read_sql_query(
            transformed_query, config.get_db_connection_string(db="migration")
        )

        casrec_query = f"""
            select distinct
                "Dep Forename" as firstname,
                   "Dep Surname" as surname,
                   "Dep Postcode" as postcode
            from {config.schemas["pre_transform"]}.deputy
            left outer join {config.schemas["pre_transform"]}.deputyship on deputy."Deputy No" = deputyship."Deputy No"
            left outer join {config.schemas["pre_transform"]}.deputy_address on deputyship."Dep Addr No" = deputy_address."Dep Addr No"
            where deputy."Dep Surname" = '{single_case}'
            order by "Dep Forename", "Dep Surname", "Dep Postcode";
        """

        casrec_df = pd.read_sql_query(
            casrec_query, config.get_db_connection_string(db="migration")
        )

        try:
            pd.testing.assert_frame_equal(transformed_df, casrec_df)
            result["passed"] += 1
        except AssertionError:
            result["failed"].append(single_case)

    print(f"result: {result['passed']}/{result['total']} passed")
    if len(result["failed"]) > 0:
        print(f"Failed caserecnumbers: {', '.join(result['failed'])}")

    assert len(result["failed"]) == 0
