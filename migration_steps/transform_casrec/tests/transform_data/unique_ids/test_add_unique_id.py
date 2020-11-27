import pandas as pd
import pytest

from transform_data.unique_id import add_unique_id

table_definition = {"destination_table_name": "persons"}

test_source_data_dict = {
    "Remarks": ["row1", "row2", "row3"],
    "Logdate": ["blah", "blah", "blah"],
}

source_data_df = pd.DataFrame(
    test_source_data_dict, columns=[x for x in test_source_data_dict]
)


@pytest.mark.parametrize(
    "existing_max_id, expected_next_id", [(0, 1), (1, 2), (1000, 1001), (-1, 0)]
)
def test_add_unique_id(monkeypatch, existing_max_id, expected_next_id):
    def mock_df(query, db_conn):
        return pd.DataFrame([existing_max_id], columns=["max"])

    monkeypatch.setattr(pd, "read_sql_query", mock_df)

    test_data_df = source_data_df.copy(deep=True)

    transformed_df = add_unique_id(
        db_conn_string="",
        db_schema="",
        table_definition=table_definition,
        source_data_df=test_data_df,
    )

    assert transformed_df.loc[0]["id"] == expected_next_id
    no_of_records = len(transformed_df)
    assert (
        transformed_df.loc[no_of_records - 1]["id"] == existing_max_id + no_of_records
    )


def test_add_unique_id_new_table(monkeypatch):

    monkeypatch.setattr(pd, "read_sql_query", Exception)

    test_data_df = source_data_df.copy(deep=True)

    transformed_df = add_unique_id(
        db_conn_string="",
        db_schema="",
        table_definition=table_definition,
        source_data_df=test_data_df,
    )

    assert transformed_df.loc[0]["id"] == 1
    no_of_records = len(transformed_df)
    assert transformed_df.loc[no_of_records - 1]["id"] == no_of_records
