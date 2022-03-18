import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from entities.reporting.duedatecalculator import DueDateCalculator


def test_examples():
    ddc = DueDateCalculator()
    ddc.set_cases(["1"])

    expected = pd.DataFrame(
        [
            # no end date, Lay => no duedate
            {
                "reportingperiodenddate": "",
                "c_case": "3",
                "duedate": None,
                "note": "No End Date, so no Due Date",
            },
            # no end date, PA/PRO => no duedate
            {
                "reportingperiodenddate": "",
                "c_case": "1",
                "duedate": None,
                "note": "No End Date, so no Due Date",
            },
            # bad end date, Lay => no duedate
            {
                "reportingperiodenddate": "88/11/2999",
                "c_case": "3",
                "duedate": None,
                "note": "Bad End Date, so no Due Date",
            },
            # bad end date, PA/PRO => no duedate
            {
                "reportingperiodenddate": "99/12/2022",
                "c_case": "1",
                "duedate": None,
                "note": "Bad End Date, so no Due Date",
            },
            # Saturday, Lay => duedate = end date + 21 days, rolled forward to Monday
            {
                "reportingperiodenddate": "19/03/2022",
                "c_case": "3",
                "duedate": "2022-04-11",
                "note": "Due Date = End Date + 21 days, falls on a Saturday, moves to following Monday",
            },
            # Sunday, Lay => duedate = end date + 21 days, rolled forward to Monday
            {
                "reportingperiodenddate": "20/03/2022",
                "c_case": "3",
                "duedate": "2022-04-11",
                "note": "Due Date = End Date + 21 days, falls on a Sunday, moves to following Monday",
            },
            # Friday, Lay => duedate = end date + 21 days
            {
                "reportingperiodenddate": "04/03/2022",
                "c_case": "3",
                "duedate": "2022-03-25",
                "note": "Due Date = End Date + 21 days, falls on a Friday, left as-is",
            },
            # PA/PRO => duedate = end date + 40 working days
            {
                "reportingperiodenddate": "21/03/2022",
                "c_case": "1",
                "duedate": "2022-05-16",
                "note": "Due Date = End Date + 40 working days",
            },
            # PA/PRO => duedate = end date + 40 working days
            {
                "reportingperiodenddate": "28/11/1999",
                "c_case": "1",
                "duedate": "2000-01-21",
                "note": "Due Date = End Date + 40 working days",
            },
            # PA/PRO => duedate = end date + 40 working days
            {
                "reportingperiodenddate": "09/06/2012",
                "c_case": "1",
                "duedate": "2012-08-03",
                "note": "Due Date = End Date + 40 working days",
            },
            # PA/PRO => duedate = end date + 40 working days, treats 3 bank holidays in May as working days
            {
                "reportingperiodenddate": "21/04/2022",
                "c_case": "1",
                "duedate": "2022-06-16",
                "note": "Due Date = End Date + 40 working days, 3 bank holidays treated as working days",
            },
        ]
    )

    test_df = expected.drop(columns=["duedate", "note"])
    actual = test_df.apply(ddc.calculate_duedate, axis=1)

    assert_frame_equal(expected.drop(columns=["note"]), actual)

    # print the examples (useful for showing UaT)
    expected["Has active PA/PRO deputy?"] = "no"
    expected.loc[
        expected["c_case"].isin(ddc.cases), "Has active PA/PRO deputy?"
    ] = "yes"

    expected = expected.drop(columns=["c_case"])
    expected = expected.rename(
        columns={
            "reportingperiodenddate": "End Date",
            "duedate": "Due Date",
            "note": "Note",
        }
    )

    print(
        "\n"
        + expected[
            ["End Date", "Due Date", "Has active PA/PRO deputy?", "Note"]
        ].to_markdown()
    )
