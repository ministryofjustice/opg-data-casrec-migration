import pandas as pd

from tests.transformations.transformations_from_mapping.cases import (
    cases_transformations_called,
    cases_steps_called,
)
from transformations.transformations_from_mapping import (
    do_simple_transformations,
    perform_transformations,
)
from pytest_cases import parametrize_with_cases

test_source_data_dict = {
    "Remarks": ["row1", "row2", "row3"],
    "Logdate": ["blah", "blah", "blah"],
}

test_source_data_df = pd.DataFrame(
    test_source_data_dict, columns=[x for x in test_source_data_dict]
)

table_definition = {"source_table_name": "source_table_name"}
db_conn_string = "db_conn_string"
db_schema = "db_schema"


@parametrize_with_cases(("mapping", "log_message"), cases=cases_steps_called)
def test_correct_steps_called(caplog, mock_transformation_steps, mapping, log_message):

    print(mapping)
    perform_transformations(
        mapping, table_definition, test_source_data_df, db_conn_string, db_schema
    )

    assert log_message in caplog.text
