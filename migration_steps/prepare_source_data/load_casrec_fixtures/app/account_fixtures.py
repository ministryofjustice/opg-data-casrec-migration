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
_end_date_ten_working_days_ago = np.busday_offset(_now, -10).astype(datetime)
_end_date_thirty_working_days_ago = np.busday_offset(_now, -30).astype(datetime)
_end_date_eighty_working_days_ago = np.busday_offset(_now, -80).astype(datetime)

ACCOUNT_FIXTURES = {
    # get the latest account for a case; note that the column names here are
    # used to construct the where clause for the update query, so should match actual
    # column names in the original table (even if you're doing an aggregation
    # of some kind)
    "source_query": 'SELECT "Case", MAX("End Date") AS "End Date" FROM {schema}.account WHERE "Case" = \'{case}\' GROUP BY "Case"',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.account SET {set_clause} WHERE {where_clause}",
    "updates": [
        # fixtures for annual_report_logs;
        # for criteria, see table_transforms_annual_report_logs.py
        # casrec accounts with the dates set below will be transformed to
        # Sirius annual_report_log records with the status and reviewstatus shown
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
            "source_criteria": {"case": "10005928"},
            "set": {
                "End Date": _end_date_ten_working_days_ago.strftime("%Y-%m-%d"),
                "Lodge Date": None,
                "Rcvd Date": None,
                "Review Date": None,
            },
        },
        {
            # status=OVERDUE, reviewstatus=NO_REVIEW
            "source_criteria": {"case": "10461469"},
            "set": {
                "End Date": _end_date_thirty_working_days_ago.strftime("%Y-%m-%d"),
                "Lodge Date": None,
                "Rcvd Date": None,
                "Review Date": None,
            },
        },
        {
            # status=NON_COMPLIANT, reviewstatus=NO_REVIEW
            "source_criteria": {"case": "97200058"},
            "set": {
                "End Date": _end_date_eighty_working_days_ago.strftime("%Y-%m-%d"),
                "Lodge Date": None,
                "Rcvd Date": None,
                "Review Date": None,
            },
        },
        # fixtures for annual_reporting_lodging_details;
        # for rules, see table_transforms_annual_report_lodging_details.py
        # casrec accounts with the specified case numbers will be transformed to
        # Sirius annual_report_log records with the lodgedstatus shown
        {
            # arld rule 1.6: lodgedstatus=ACKNOWLEDGED
            "source_criteria": {"case": "10016431"},
            "set": {
                "Rev Stat": "N",
                "Rcvd Date": "2022-01-05",
                "Lodge Date": "2022-01-07",
                "Review Date": None,
            },
        },
        {
            # arld rule 1.7: lodgedstatus=INCOMPLETE
            "source_criteria": {"case": "10233264"},
            "set": {
                "Rev Stat": "I",
                "Rcvd Date": "2022-01-05",
                "Lodge Date": "2022-01-07",
                "Review Date": None,
            },
        },
        {
            # arld rule 1.8: rev stat="S", lodgedstatus=REFERRED_FOR_REVIEW
            "source_criteria": {"case": "95000400"},
            "set": {
                "Rev Stat": "S",
                "Rcvd Date": "2022-01-05",
                "Lodge Date": "2022-01-07",
            },
        },
        {
            # arld rule 1.9: rev stat="R", lodgedstatus=REFERRED_FOR_REVIEW
            "source_criteria": {"case": "10050512"},
            "set": {
                "Rev Stat": "R",
                "Rcvd Date": "2022-01-05",
                "Lodge Date": "2022-01-07",
                "Review Date": "2022-01-12",
            },
        },
        {
            # arld rule 1.9: rev stat="G", lodgedstatus=REFERRED_FOR_REVIEW
            "source_criteria": {"case": "94040677"},
            "set": {
                "Rev Stat": "G",
                "Rcvd Date": "2022-01-05",
                "Lodge Date": "2022-01-07",
                "Review Date": "2022-01-12",
            },
        },
        {
            # arld rule 1.9: rev stat="M", lodgedstatus=REFERRED_FOR_REVIEW
            "source_criteria": {"case": "1119959T"},
            "set": {
                "Rev Stat": "M",
                "Rcvd Date": "2022-01-05",
                "Lodge Date": "2022-01-07",
                "Review Date": "2022-01-12",
            },
        },
        {
            # arld rule 2.1: lodgedstatus=INCOMPLETE
            "source_criteria": {"case": "12022071"},
            "set": {
                "Revise Date": "2022-01-05",
                "Further Code": "2",
                "Rcvd Date": None,
                "Rcvd Date1": None,
                "Rcvd Date2": None,
                "Rcvd Date3": None,
                "Rcvd Date4": None,
                "Rcvd Date5": None,
                "Rcvd Date6": None,
                "Sent1": None,
                "Sent2": None,
                "Sent3": None,
                "Sent4": None,
                "Sent5": None,
                "Sent6": None,
                "Followup Date": "2022-01-12",
            },
        },
        {
            # arld rule 2.2: lodgedstatus=INCOMPLETE
            "source_criteria": {"case": "11508154"},
            "set": {
                "Revise Date": "2022-01-05",
                "Further Code": "3",
                "Rcvd Date": "2022-01-06",
                "Sent1": None,
                "Sent2": None,
                "Sent3": None,
                "Sent4": None,
                "Sent5": None,
                "Sent6": None,
                "Followup Date": "2022-01-12",
            },
        },
        {
            # arld rule 2.3: lodgedstatus=REFERRED_FOR_REVIEW
            "source_criteria": {"case": "10065868"},
            "set": {
                "Revise Date": "2022-01-05",
                "Further Code": "1",
                "Rcvd Date": None,
                "Rcvd Date1": None,
                "Rcvd Date2": None,
                "Rcvd Date3": None,
                "Rcvd Date4": None,
                "Rcvd Date5": None,
                "Rcvd Date6": None,
                "Sent1": "2022-01-12",
                "Followup Date": None,
            },
        },
        {
            # arld rule 2.4: lodgedstatus=REFERRED_FOR_REVIEW
            "source_criteria": {"case": "10015094"},
            "set": {
                "Revise Date": "2022-01-06",
                "Further Code": "8",
                "Rcvd Date": "2022-01-05",
                "Sent1": "2022-01-12",
                "Followup Date": None,
            },
        },
        {
            # arld rule 2.5: lodgedstatus=REFERRED_FOR_REVIEW
            "source_criteria": {"case": "10011951"},
            "set": {
                "Revise Date": None,
                "Further Code": None,
                "Rcvd Date": None,
                "Rcvd Date1": None,
                "Rcvd Date2": None,
                "Rcvd Date3": None,
                "Rcvd Date4": None,
                "Rcvd Date5": None,
                "Rcvd Date6": None,
                "Sent1": None,
                "Sent2": None,
                "Sent3": None,
                "Sent4": None,
                "Sent5": None,
                "Sent6": None,
                "Followup Date": None,
            },
        },
    ],
}
