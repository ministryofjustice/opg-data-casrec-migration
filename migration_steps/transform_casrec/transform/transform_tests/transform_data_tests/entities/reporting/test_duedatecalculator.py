import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from entities.reporting.duedatecalculator import DueDateCalculator


ddc = DueDateCalculator()


def test_duedatecalculator_no_end_date():
    ddc.set_cases(
        [
            "1",
        ]
    )

    df = pd.DataFrame(
        [
            # no end date, no active PA/PRO deputies
            {"reportingperiodenddate": "", "c_case": "3"},
            {"reportingperiodenddate": None, "c_case": "3"},
            # no end date, has active PA/PRO deputies
            {"reportingperiodenddate": "", "c_case": "1"},
            {"reportingperiodenddate": None, "c_case": "1"},
        ]
    )

    expected = pd.DataFrame(
        [
            # no end date, no active PA/PRO deputies => no duedate
            {"reportingperiodenddate": "", "c_case": "3", "duedate": None},
            {"reportingperiodenddate": None, "c_case": "3", "duedate": None},
            # no end date, has active PA/PRO deputies => no duedate
            {"reportingperiodenddate": "", "c_case": "1", "duedate": None},
            {"reportingperiodenddate": None, "c_case": "1", "duedate": None},
        ]
    )

    actual = df.apply(ddc.calculate_duedate, axis=1)

    print(expected)
    print(actual)

    assert_frame_equal(expected, actual)


def test_duedatecalculator_roll_forward_non_working_day():
    """
    NB empty reportingperiodenddate cases are included here again as they were
    causing errors in the test due to data types being mis-aligned. By keeping them
    here we can ensure this error doesn't recur.
    """
    ddc.set_cases(["1", "2"])

    df = pd.DataFrame(
        [
            # no end date
            {"reportingperiodenddate": "", "c_case": "3"},
            {"reportingperiodenddate": None, "c_case": "3"},
            # Saturday, Lay
            {"reportingperiodenddate": "2022-03-19", "c_case": "3"},
            # Sunday, Lay
            {"reportingperiodenddate": "2022-03-20", "c_case": "3"},
            # Monday, PA/PRO
            {"reportingperiodenddate": "2022-03-21", "c_case": "1"},
            # Tuesday, PA/PRO
            {"reportingperiodenddate": "2022-03-22", "c_case": "1"},
        ]
    )

    expected = pd.DataFrame(
        [
            # no end date => no duedate
            {"reportingperiodenddate": "", "c_case": "3", "duedate": None},
            {"reportingperiodenddate": None, "c_case": "3", "duedate": None},
            # Saturday, Lay => duedate = end date + 21 days, rolled forward to Monday
            {
                "reportingperiodenddate": "2022-03-19",
                "c_case": "3",
                "duedate": np.datetime64("2022-04-11"),
            },
            # Sunday, Lay => duedate = end date + 21 days, rolled forward to Monday
            {
                "reportingperiodenddate": "2022-03-20",
                "c_case": "3",
                "duedate": np.datetime64("2022-04-11"),
            },
            # Monday, PA/PRO => duedate = end date + 40 days (ends up on a Saturday),
            # rolled forward to Monday
            {
                "reportingperiodenddate": "2022-03-21",
                "c_case": "1",
                "duedate": np.datetime64("2022-05-02"),
            },
            # Tuesday, PA/PRO => duedate = end date + 40 days (ends up on a Sunday),
            # rolled forward to Monday
            {
                "reportingperiodenddate": "2022-03-22",
                "c_case": "1",
                "duedate": np.datetime64("2022-05-02"),
            },
        ]
    )

    actual = df.apply(ddc.calculate_duedate, axis=1)

    assert_frame_equal(expected, actual)
