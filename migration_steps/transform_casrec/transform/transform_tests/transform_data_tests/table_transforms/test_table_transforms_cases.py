import pandas as pd
from pytest_cases import parametrize_with_cases
from transform_data.table_transforms import process_table_transformations


def case_table_transforms_cases_active_supplement_order():
    return (
        {
            "c_ord_stat": ["Active"],
            "c_ord_type": ["26"]
        },
        {
            "orderstatus": "OPEN"
        }
    )


def case_table_transforms_cases_active_call_in_bond_order():
    return (
        {
            "c_ord_stat": ["Active"],
            "c_ord_type": ["43"]
        },
        {
            "orderstatus": "OPEN"
        }
    )


def case_table_transforms_cases_active_tenancy_order():
    return (
        {
            "c_ord_stat": ["Active"],
            "c_ord_type": ["45"]
        },
        {
            "orderstatus": "OPEN"
        }
    )


def case_table_transforms_cases_active_pfa_order():
    return (
        {
            "c_ord_stat": ["Active"],
            "c_ord_type": ["1"]
        },
        {
            "orderstatus": "ACTIVE"
        }
    )


def case_table_transforms_cases_active_hw_order():
    return (
        {
            "c_ord_stat": ["Active"],
            "c_ord_type": ["2"]
        },
        {
            "orderstatus": "ACTIVE"
        }
    )


def case_table_transforms_cases_active_replacement_pa_order():
    return (
        {
            "c_ord_stat": ["Active"],
            "c_ord_type": ["40"]
        },
        {
            "orderstatus": "ACTIVE"
        }
    )


def case_table_transforms_cases_active_interim_pa_order():
    return (
        {
            "c_ord_stat": ["Active"],
            "c_ord_type": ["41"]
        },
        {
            "orderstatus": "ACTIVE"
        }
    )


def case_table_transforms_cases_closed_supplement_order():
    return (
        {
            "c_ord_stat": ["Closed"],
            "c_ord_type": ["26"]
        },
        {
            "orderstatus": "CLOSED"
        }
    )


def case_table_transforms_cases_closed_call_in_bond_order():
    return (
        {
            "c_ord_stat": ["Closed"],
            "c_ord_type": ["43"]
        },
        {
            "orderstatus": "CLOSED"
        }
    )


def case_table_transforms_cases_closed_tenancy_order():
    return (
        {
            "c_ord_stat": ["Closed"],
            "c_ord_type": ["45"]
        },
        {
            "orderstatus": "CLOSED"
        }
    )


def case_table_transforms_cases_closed_pfa_order():
    return (
        {
            "c_ord_stat": ["Closed"],
            "c_ord_type": ["1"]
        },
        {
            "orderstatus": "CLOSED"
        }
    )


def case_table_transforms_cases_closed_hw_order():
    return (
        {
            "c_ord_stat": ["Closed"],
            "c_ord_type": ["2"]
        },
        {
            "orderstatus": "CLOSED"
        }
    )


def case_table_transforms_cases_closed_replacement_pa_order():
    return (
        {
            "c_ord_stat": ["Closed"],
            "c_ord_type": ["40"]
        },
        {
            "orderstatus": "CLOSED"
        }
    )


def case_table_transforms_cases_closed_interim_pa_order():
    return (
        {
            "c_ord_stat": ["Closed"],
            "c_ord_type": ["41"]
        },
        {
            "orderstatus": "CLOSED"
        }
    )


@parametrize_with_cases("test_data, expected_data", cases=".", prefix="case_table_transforms_cases")
def test_table_transforms_cases(test_data, expected_data):
    test_df = pd.DataFrame(test_data)

    transforms = {
        'set_cases_orderstatus': {
            'source_cols': [
                'Ord Stat',
                'Ord Type'
            ],
            'target_cols': [
                'orderstatus'
            ]
        }
    }

    actual_df = process_table_transformations(test_df, transforms)

    for _, row in actual_df.iterrows():
        for col, value in expected_data.items():
            assert row[col] == value
