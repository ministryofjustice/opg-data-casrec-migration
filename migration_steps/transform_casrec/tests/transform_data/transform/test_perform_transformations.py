import pandas as pd

from tests.transform_data.transform import cases_steps_called

from pytest_cases import parametrize_with_cases

from transform_data.transform import perform_transformations

test_source_data_dict = {
    "Remarks": ["row1", "row2", "row3", "row4", "row5"],
    "Logdate": ["blah", "blah", "blah", "blah", "blah"],
}

test_source_data_df = pd.DataFrame(
    test_source_data_dict, columns=[x for x in test_source_data_dict]
)

table_definition = {
    "source_table_name": "source_table_name",
    "destination_table_name": "destination_table_name",
}
db_conn_string = "db_conn_string"
db_schema = "db_schema"


@parametrize_with_cases(("mapping", "log_message"), cases=cases_steps_called)
def test_correct_steps_called(caplog, mock_transformation_steps, mapping, log_message):

    perform_transformations(
        mapping, table_definition, test_source_data_df, db_conn_string, db_schema
    )

    assert log_message in caplog.text
