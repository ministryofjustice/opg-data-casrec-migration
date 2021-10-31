DROP TABLE IF EXISTS casrec_csv.exceptions_annual_report_logs;

CREATE TABLE casrec_csv.exceptions_annual_report_logs(
    reportingperiodenddate text default NULL,
    reportingperiodstartdate text default NULL,
    duedate text default NULL,
    receiveddate text default NULL,
    reviewdate text default NULL
);

INSERT INTO casrec_csv.exceptions_annual_report_logs(
    SELECT * FROM(
        -- assumption: End Date is never NULL or ''
        SELECT
            CAST(account."End Date" AS date) AS reportingperiodenddate,
            CAST(account."End Date" AS date) - 366 AS reportingperiodstartdate,
            transf_calculate_duedate(account."End Date") AS duedate,
            CAST(
                GREATEST(
                    NULLIF(account."Rcvd Date", ''),
                    NULLIF(account."Rcvd Date1", ''),
                    NULLIF(account."Rcvd Date2", ''),
                    NULLIF(account."Rcvd Date3", ''),
                    NULLIF(account."Rcvd Date4", ''),
                    NULLIF(account."Rcvd Date5", ''),
                    NULLIF(account."Rcvd Date6", '')
                )
            AS date) AS receiveddate,
            CAST(NULLIF(account."Review Date", '') AS date) AS reviewdate
        FROM
            casrec_csv.account
     ) as csv_data
    EXCEPT
    SELECT * FROM(
        SELECT
            annual_report_logs.reportingperiodenddate AS reportingperiodenddate,
            annual_report_logs.reportingperiodstartdate AS reportingperiodstartdate,
            annual_report_logs.duedate AS duedate,
            annual_report_logs.receiveddate AS receiveddate,
            annual_report_logs.reviewdate AS reviewdate
        FROM
            {target_schema}.annual_report_logs
     ) as sirius_data
);