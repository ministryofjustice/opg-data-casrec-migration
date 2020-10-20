import pandas as pd

from transformations.transformations_from_mapping import do_simple_mapping

test_simple_mapping_dict = {
    "status": {
        "casrec_table": "REMARKS",
        "casrec_column_name": "Log Type",
        "alias": "Log Type",
    },
    "description": {
        "casrec_table": "REMARKS",
        "casrec_column_name": "Remarks",
        "alias": "Remarks",
    },
    "createdtime": {
        "casrec_table": "REMARKS",
        "casrec_column_name": "Logdate",
        "alias": "Logdate",
    },
}

table_definition = {"source_table_name": "remarks"}

test_source_data_dict = {
    "Remarks": ["row1", "row2", "row3"],
    "Logdate": ["blah", "blah", "blah"],
}

test_source_data_df = pd.DataFrame(
    test_source_data_dict, columns=[x for x in test_source_data_dict]
)


def test_do_simple_mapping():
    transformed_df = do_simple_mapping(
        test_simple_mapping_dict, table_definition, test_source_data_df
    )
    transformed_columns = list(transformed_df)

    required_columns = ["description", "createdtime"]

    assert transformed_columns == required_columns
