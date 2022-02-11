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


def case_table_transforms_set_visits_visitsubtype_vsthw():
    test_data = {
        "c_req_by": [
            "1",
            "2",
            "4",
            "5",
            "6",
            "7",
        ],
        "c_report_type": list("2" * 6),
    }
    expected_data = {"visitsubtype": "VST-HW"}
    return (test_data, expected_data)


def case_table_transforms_set_visits_visitsubtype_vstmed():
    test_data = {
        "c_req_by": [
            "1",
            "2",
            "4",
            "5",
            "6",
            "7",
        ],
        "c_report_type": list("3" * 6),
    }
    expected_data = {"visitsubtype": "VST-MED"}
    return (test_data, expected_data)


def case_table_transforms_set_visits_visitsubtype_vstdep():
    test_data = {
        "c_req_by": [
            "3",
            "3",
        ],
        "c_report_type": ["1", "2"],
    }
    expected_data = {"visitsubtype": "VST-DEP"}
    return (test_data, expected_data)


def case_table_transforms_set_visits_visitsubtype_vstmlpa():
    test_data = {
        "c_req_by": [
            "3",
        ],
        "c_report_type": ["3"],
    }
    expected_data = {"visitsubtype": "VST-MLPA"}
    return (test_data, expected_data)


def case_table_transforms_set_visits_visitsubtype_vstpro1():
    test_data = {
        "c_req_by": [
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
        ],
        "c_report_type": list("1" * 7),
    }
    expected_data = {"visitsubtype": "VST-PRO"}
    return (test_data, expected_data)


def case_table_transforms_set_visits_visitsubtype_vstpro2():
    test_data = {
        "c_req_by": [
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
        ],
        "c_report_type": list("2" * 7),
    }
    expected_data = {"visitsubtype": "VST-PRO"}
    return (test_data, expected_data)


def case_table_transforms_set_visits_visitsubtype_vstpro3():
    test_data = {
        "c_req_by": [
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
        ],
        "c_report_type": list("3" * 7),
    }
    expected_data = {"visitsubtype": "VST-PRO"}
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
