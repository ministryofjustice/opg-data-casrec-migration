from transformations.transformations_from_mapping import add_unique_id
import pandas as pd


table_definition = {"destination_table_name": "persons"}

test_source_data_dict = {
    "Remarks": ["row1", "row2", "row3"],
    "Logdate": ["blah", "blah", "blah"],
}

source_data_df = pd.DataFrame(
    test_source_data_dict, columns=[x for x in test_source_data_dict]
)


def test_add_unique_id(mock_max_id_from_db):
    transformed_df = add_unique_id(
        db_conn_string="",
        db_schema="",
        table_definition=table_definition,
        source_data_df=source_data_df,
    )

    assert transformed_df.loc[0]["id"] == 56
    no_of_records = len(transformed_df)
    assert transformed_df.loc[no_of_records - 1]["id"] == 55 + no_of_records
