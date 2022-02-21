DROP TABLE IF EXISTS casrec_csv.exceptions_annual_report_logs;

CREATE TABLE casrec_csv.exceptions_annual_report_logs(
    caserecnumber text default NULL,
    reportingperiodenddate text default NULL,
    reportingperiodstartdate text default NULL,
    duedate text default NULL,
    receiveddate text default NULL,
    revisedduedate text default NULL,
    numberofchaseletters text default NULL,
    reviewdate text default NULL,
    status text default NULL,
    reviewstatus text default NULL
);

INSERT INTO casrec_csv.exceptions_annual_report_logs(
    -- non-pending annual_report_logs derived from casrec account table
    SELECT * FROM (
        SELECT
            caserecnumber,
            reportingperiodenddate,
            reportingperiodstartdate,
            duedate,
            CAST(nullif(receiveddate, '') AS date) AS receiveddate,
            CAST(nullif(revisedduedate, '') AS date) AS revisedduedate,
            numberofchaseletters,
            casrec_csv.report_element(full_status, 1) AS status,
            NULLIF(casrec_csv.report_element(full_status, 3), '') AS reviewstatus,
            CAST(nullif(reviewdate, '') AS date) AS reviewdate
        FROM (
            SELECT
                caserecnumber,
                reportingperiodenddate,
                reportingperiodstartdate,
                duedate,
                receiveddate,
                revisedduedate,
                numberofchaseletters,
                casrec_csv.report_status(
                    casrec_csv.report_status_aggregate(
                        review_status, wd_count_end_date, receiveddate, lodged_date, reviewdate, next_yr_flag
                    )
                ) full_status,
                reviewdate
            FROM (
                SELECT
                    "Case" AS caserecnumber,
                    CAST(account."End Date" AS date) AS reportingperiodenddate,
                    CAST(account."End Date" AS date) - INTERVAL '1 year' + INTERVAL '1 day' AS reportingperiodstartdate,
                    transf_calculate_duedate(account."End Date") AS duedate,
                    GREATEST(
                        NULLIF(account."Rcvd Date", ''),
                        NULLIF(account."Rcvd Date1", ''),
                        NULLIF(account."Rcvd Date2", ''),
                        NULLIF(account."Rcvd Date3", ''),
                        NULLIF(account."Rcvd Date4", ''),
                        NULLIF(account."Rcvd Date5", ''),
                        NULLIF(account."Rcvd Date6", '')
                    ) AS receiveddate,
                    "Revise Date" AS revisedduedate,
                    0 AS numberofchaseletters,
                    casrec_csv.weekday_count(account."End Date") AS wd_count_end_date,
                    "Rev Stat" AS review_status,
                    "Lodge Date" AS lodged_date,
                    "Review Date" AS reviewdate,
                    "Next Yr" AS next_yr_flag
                FROM
                    casrec_csv.account
            ) AS account_annual_report_logs
        ) AS non_pending_annual_report_logs

        UNION

        -- pending annual_report_logs derived from casrec pat table
        SELECT
            "Case" AS caserecnumber,
            CAST(p."Report Due" AS date) AS reportingperiodenddate,
            active_cases.reportingperiodstartdate,
            transf_calculate_duedate(p."Report Due") AS duedate,
            NULL AS receiveddate,
            NULL AS revisedduedate,
            0 AS numberofchaseletters,
            'PENDING' AS status,
            'NO_REVIEW' AS review_status,
            NULL AS reviewdate
        FROM
            casrec_csv.pat p

        INNER JOIN(
            SELECT account_case, reportingperiodstartdate
            FROM casrec_csv.order o
            INNER JOIN (
                SELECT
                    a."Case" as account_case,
                    CAST(a."End Date" AS date) + 1 as reportingperiodstartdate,
                    row_number() OVER (
                        PARTITION BY a."Case"
                        ORDER BY a."End Date" DESC
                    ) AS rownum
                FROM casrec_csv.account a
            ) AS cases
            ON o."Case" = cases.account_case
            WHERE cases.rownum = 1
            AND o."Ord Stat" = 'Active'
        ) AS active_cases

        ON p."Case" = active_cases.account_case

        WHERE p."Report Due" != ''
    ) AS casrec_annual_report_logs

    EXCEPT

    SELECT
        persons.caserecnumber AS caserecnumber,
        annual_report_logs.reportingperiodenddate AS reportingperiodenddate,
        annual_report_logs.reportingperiodstartdate AS reportingperiodstartdate,
        annual_report_logs.duedate AS duedate,
        annual_report_logs.receiveddate AS receiveddate,
        annual_report_logs.revisedduedate AS revisedduedate,
        annual_report_logs.numberofchaseletters AS numberofchaseletters,
        annual_report_logs.status,
        annual_report_logs.reviewstatus,
        annual_report_logs.reviewdate
    FROM {target_schema}.annual_report_logs
    LEFT JOIN {target_schema}.persons
    ON persons.id = annual_report_logs.client_id
);
