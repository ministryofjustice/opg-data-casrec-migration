import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from entities.reporting.annual_report_type_assignments import calculate_report_types


def test_calculate_report_types_one_case_multiple_orders():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [1, 1, 1],
            "sirius_report_log_casrec_case_no": ["C1", "C1", "C1"],
            "ord_stat": ["Active", "Closed", "Closed"],
            "ord_risk_lvl": ["3", "3", "2"],
        }
    )

    expected_df = pd.DataFrame(
        {
            "annualreport_id": [1],
            "sirius_report_log_casrec_case_no": ["C1"],
            "reporttype": ["OPG103"],
            "type": ["-"],
        }
    )

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)


def test_calculate_report_types_multiple_reports_same_case():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [1, 1, 2, 2],
            "sirius_report_log_casrec_case_no": ["C1", "C1", "C1", "C1"],
            "ord_stat": ["Active", "Closed", "Active", "Closed"],
            "ord_risk_lvl": ["3", "3", "2", "2"],
        }
    )

    expected_df = pd.DataFrame(
        {
            "annualreport_id": [1, 2],
            "sirius_report_log_casrec_case_no": ["C1", "C1"],
            "reporttype": ["OPG103", "OPG102"],
            "type": ["-", "-"],
        }
    )

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)


def test_calculate_report_types_no_active_order():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [1],
            "sirius_report_log_casrec_case_no": ["C1"],
            "ord_stat": ["Closed"],
            "ord_risk_lvl": ["2"],
        }
    )

    expected_df = pd.DataFrame(
        {
            "annualreport_id": [1],
            "sirius_report_log_casrec_case_no": ["C1"],
            "reporttype": [""],
            "type": ["-"],
        }
    )

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)


def test_calculate_report_types_no_orders():
    test_df = pd.DataFrame(
        {
            "annualreport_id": [1],
            "sirius_report_log_casrec_case_no": ["C1"],
            "ord_stat": [None],
            "ord_risk_lvl": [None],
        }
    )

    expected_df = pd.DataFrame(
        {
            "annualreport_id": [1],
            "sirius_report_log_casrec_case_no": ["C1"],
            "reporttype": [""],
            "type": ["-"],
        }
    )

    transformed_df = calculate_report_types(test_df)

    assert_frame_equal(expected_df, transformed_df)
