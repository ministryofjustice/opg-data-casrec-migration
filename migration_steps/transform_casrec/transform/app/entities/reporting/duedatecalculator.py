import numpy as np
import pandas as pd

from utilities.standard_transformations import calculate_date


class DueDateCalculatorUnpopulatedException(Exception):
    def __str__(self):
        return """
            DueDateCalculator instance is not populated; call populate() or set_cases()
            to populate it with a list of case numbers.
        """


class DueDateCalculator:
    """
    Calculate duedate for a report, depending on whether or not
    it has an active PRO/PA deputy associated with its case.
    """

    # Dep Type values which denote PA/PRO deputies; see IN-1208
    PA_PRO_DEP_TYPES = list(range(20, 30)) + [
        60,
        73,
        90,
    ]

    # Query to get all cases which have an active PA/PRO deputy;
    # "Stat" = '1' denotes an active deputy
    PA_PRO_CASES_WITH_ACTIVE_DEPUTIES_QUERY = """
        SELECT DISTINCT CAST(ds."Case" AS text) AS case
        FROM casrec_csv_p2.deputy d
        INNER JOIN {source_schema}.deputyship ds
        ON d."Deputy No" = ds."Deputy No"
        WHERE d."Dep Type" IN ('{"', '".join(deputy_types)}')
        AND d."Stat" = '1'
    """

    def __init__(self, db_config: dict = None):
        """
        :param db_config: database config, with db_connection_string
            (db connection string) and source_schema (casrec source schema name)
            properties
        """
        if db_config is None:
            db_config = {}
        self.db_config = db_config

        # cases is a list of strings representing case numbers which have
        # active deputies; use populate to set this from the database
        self.cases = None

    def populate(self) -> pd.DataFrame:
        """
        Load case numbers with active PA/PRO deputies from the casrec db;
        resulting dataframe has a single column, "case"
        """
        query = self.PA_PRO_CASES_WITH_ACTIVE_DEPUTIES_QUERY.format(
            source_schema=self.db_config["source_schema"],
            deputy_types=self.PA_PRO_DEP_TYPES,
        )

        df = pd.read_sql_query(query, self.db_config["db_connection_string"])

        self.set_cases(df["case"].tolist())

        return self.cases

    def set_cases(self, cases: list):
        """
        :param cases: list of case numbers as strings
        """
        self.cases = cases

    def calculate_duedate(self, row: pd.Series) -> pd.Series:
        """
        Given a row from annual_report_logs, set the duedate, depending
        on whether it is a PA/PRO or Lay report. The returned row
        contains a set duedate field (will be None if reportingperiodenddate
        is None or "").

        The row must contain these fields with these types:
        * reportingperiodenddate: str in format "23/12/2022"
        * c_case: str

        If the row references a case which has an active PA/PRO deputy,
        duedate = end date + 40 working days.

        Otherwise, duedate = end date + 21 working days.

        This ignores bank holidays and rolls the day forward if it falls on
        a weekend.

        :param row: row from the annual_report_logs select
        :raises DueDateCalculatorUnpopulatedException: if called before
            self.cases has been populated
        """
        # we haven't set self.cases, so anything we do will be invalid
        if self.cases is None:
            raise DueDateCalculatorUnpopulatedException()

        # can't do anything with this
        if row["reportingperiodenddate"] in (
            None,
            "",
        ):
            row["duedate"] = None
            return row

        if row["c_case"] in self.cases:
            # active PA/PRO deputy
            day_offset = 40
        else:
            # everything else
            day_offset = 21

        row["duedate"] = calculate_date(
            base_date=row["reportingperiodenddate"],
            delta=pd.offsets.DateOffset(days=day_offset),
            weekend_adjustment="next",
        )

        return row
