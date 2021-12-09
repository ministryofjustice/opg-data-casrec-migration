"""
Dynamic fixtures for the casrec account table, mostly for testing
annual_report_logs statuses and reviewstatuses.
"""
import numpy as np
from datetime import datetime

# see https://opgtransform.atlassian.net/browse/IN-763 for criteria used
# to map End Date to status and reviewstatus for annual_report_logs
_now = np.datetime64(datetime.now().strftime("%Y-%m-%d"))
_end_date_future = np.busday_offset(_now, 7).astype(datetime)
_end_date_ten_working_days_ago = np.busday_offset(_now, -14).astype(datetime)
_end_date_thirty_working_days_ago = np.busday_offset(_now, -30).astype(datetime)
_end_date_eighty_working_days_ago = np.busday_offset(_now, -80).astype(datetime)

ACCOUNT_FIXTURES = [
    {
        # get the latest account for a case; note that the column names here are
        # used to construct the where clause for the update query, so should match actual
        # column names in the original table (even if you're doing an aggregation
        # of some kind)
        "source_query": 'SELECT "Case", MAX("End Date") AS "End Date" FROM {schema}.account WHERE "Case" = \'{case}\' GROUP BY "Case"',
        # set an account's fields to fixture values
        "update_query": "UPDATE {schema}.account SET {set_clause} WHERE {where_clause}",
        # casrec accounts with the dates set below will be transformed to
        # Sirius annual_report_log records with the status and reviewstatus shown
        "updates": [
            {
                # status=PENDING, reviewstatus=NO_REVIEW
                "source_criteria": {"case": "94055780"},
                "set": {
                    "End Date": _end_date_future.strftime("%Y-%m-%d"),
                    "Lodge Date": None,
                    "Rcvd Date": None,
                    "Review Date": None,
                },
            },
            {
                # status=DUE, reviewstatus=NO_REVIEW
                "source_criteria": {"case": "12233313"},
                "set": {
                    "End Date": _end_date_ten_working_days_ago.strftime("%Y-%m-%d"),
                    "Lodge Date": None,
                    "Rcvd Date": None,
                    "Review Date": None,
                },
            },
            {
                # status=OVERDUE, reviewstatus=NO_REVIEW
                "source_criteria": {"case": "94061819"},
                "set": {
                    "End Date": _end_date_thirty_working_days_ago.strftime("%Y-%m-%d"),
                    "Lodge Date": None,
                    "Rcvd Date": None,
                    "Review Date": None,
                },
            },
            {
                # status=NON_COMPLIANT, reviewstatus=NO_REVIEW
                "source_criteria": {"case": "95002441"},
                "set": {
                    "End Date": _end_date_eighty_working_days_ago.strftime("%Y-%m-%d"),
                    "Lodge Date": None,
                    "Rcvd Date": None,
                    "Review Date": None,
                },
            },
        ],
    }
]
