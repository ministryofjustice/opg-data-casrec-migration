import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from entities.reporting.annual_report_type_assignments import calculate_report_types


def test_calculate_report_types_one_case_multiple_orders():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [50, 50, 50],
            "end_date": ["2018-01-01", "2019-01-01", "2020-01-01"],
            "sirius_report_log_casrec_case_no": ["C1", "C1", "C1"],
            "ord_stat": ["Closed", "Closed", "Active"],
            "ord_risk_lvl": ["3", "3", "3"],
        }
    )

    expected_df = pd.DataFrame({"annualreport_id": [50], "reporttype": ["OPG103"]})

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)


def test_calculate_report_types_multiple_reports_same_case():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [100, 100, 200, 200],
            "end_date": ["2018-02-02", "2019-02-02", "2018-03-03", "2019-03-03"],
            "sirius_report_log_casrec_case_no": ["C1", "C1", "C1", "C1"],
            "ord_stat": ["Closed", "Active", "Closed", "Active"],
            "ord_risk_lvl": ["3", "3", "2", "2"],
        }
    )

    expected_df = pd.DataFrame(
        {"annualreport_id": [100, 200], "reporttype": ["OPG103", "OPG102"]}
    )

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)


def test_calculate_report_types_no_active_order():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [11, 11],
            "end_date": ["2018-04-04", "2019-04-04"],
            "sirius_report_log_casrec_case_no": ["C1", "C1"],
            "ord_stat": ["Closed", "Closed"],
            "ord_risk_lvl": ["2", "2"],
        }
    )

    expected_df = pd.DataFrame({"annualreport_id": [11], "reporttype": [None]})

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)


def test_calculate_report_types_no_orders():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [99],
            "end_date": ["2020-07-07"],
            "sirius_report_log_casrec_case_no": ["C1"],
            "ord_stat": [None],
            "ord_risk_lvl": [None],
        }
    )

    expected_df = pd.DataFrame({"annualreport_id": [99], "reporttype": [None]})

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)


def test_calculate_report_types_unrecognised_ord_risk_lvl():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [999],
            "end_date": ["2020-08-08"],
            "sirius_report_log_casrec_case_no": ["C1"],
            "ord_stat": ["Active"],
            "ord_risk_lvl": ["4"],
        }
    )

    expected_df = pd.DataFrame({"annualreport_id": [999], "reporttype": [None]})

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)
