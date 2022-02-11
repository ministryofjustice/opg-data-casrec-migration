import pandas as pd

from pytest_cases import parametrize_with_cases

from transform_data.table_transforms import process_table_transformations


def case_table_transforms_set_visits_visitsubtype_vstlay():
    test_data = {
        "c_req_by": [
            "1",
            "2",
            "4",
            "5",
            "6",
            "7",
        ],
        "c_report_type": list("1" * 6),
    }
    expected_data = {"visitsubtype": "VST-LAY"}
    return (test_data, expected_data)


@parametrize_with_cases(
    "test_data, expected_data",
    cases=".",
    prefix="case_table_transforms_set_visits_visitsubtype",
)
def test_table_transforms_visits(test_data, expected_data):
    """
    Test visits transform specified in IN-1089.
    """
    test_df = pd.DataFrame(test_data)

    transforms = {
        "set_visits_visitsubtype": {
            "source_cols": [
                "Req By",
                "Report Type",
            ],
            "target_cols": [
                "visitsubtype",
            ],
        }
    }

    actual_df = process_table_transformations(test_df, transforms)

    for _, row in actual_df.iterrows():
        for col, value in expected_data.items():
            assert row[col] == value
