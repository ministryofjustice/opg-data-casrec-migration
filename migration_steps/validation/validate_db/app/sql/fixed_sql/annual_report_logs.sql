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
            CAST(nullif(reviewdate, '') AS date) AS reviewdate,
            bankstatementdeadlinedate,
            deadlinedate,
            resubmitteddate
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
                reviewdate,
                casrec_csv.report_bankstatementdeadlinedate(latest_further_date, last_further_code) AS bankstatementdeadlinedate,
                casrec_csv.report_deadlinedate(latest_further_date, last_further_code) AS deadlinedate,
                casrec_csv.report_resubmitteddate(further_codes, rcvd_dates) AS resubmitteddate
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
                    "Next Yr" AS next_yr_flag,

                    -- get latest date from "Further Date*" columns
                    GREATEST(
                        CAST(NULLIF("Further Date1", '') AS date),
                        CAST(NULLIF("Further Date2", '') AS date),
                        CAST(NULLIF("Further Date3", '') AS date),
                        CAST(NULLIF("Further Date4", '') AS date),
                        CAST(NULLIF("Further Date6", '') AS date),
                        CAST(NULLIF("Further Date6.1", '') AS date)
                    ) AS latest_further_date,

                    -- in alphabetical order (Further1 is on left, Further6 on the right), get the last
                    -- value which is not 0 or 2
                    CAST(
                        TO_JSON(
                            ARRAY_REMOVE(
                                ARRAY_REMOVE(
                                    ARRAY[
                                        CAST(NULLIF("Further1", '') AS text),
                                        CAST(NULLIF("Further2", '') AS text),
                                        CAST(NULLIF("Further3", '') AS text),
                                        CAST(NULLIF("Further4", '') AS text),
                                        CAST(NULLIF("Further5", '') AS text),
                                        CAST(NULLIF("Further6", '') AS text)
                                    ],
                                    '0'
                                ),
                                '2'
                            )
                        )->>-1
                    AS text) AS last_further_code,

                    -- all "Further*" column values
                    ARRAY[
                        CAST(NULLIF("Further1", '') AS text),
                        CAST(NULLIF("Further2", '') AS text),
                        CAST(NULLIF("Further3", '') AS text),
                        CAST(NULLIF("Further4", '') AS text),
                        CAST(NULLIF("Further5", '') AS text),
                        CAST(NULLIF("Further6", '') AS text)
                    ] AS further_codes,

                    -- all "Rcvd Date*" column values
                    ARRAY[
                        CAST(NULLIF("Rcvd Date1", '') AS date),
                        CAST(NULLIF("Rcvd Date2", '') AS date),
                        CAST(NULLIF("Rcvd Date3", '') AS date),
                        CAST(NULLIF("Rcvd Date4", '') AS date),
                        CAST(NULLIF("Rcvd Date5", '') AS date),
                        CAST(NULLIF("Rcvd Date6", '') AS date)
                    ] AS rcvd_dates
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
            NULL AS review_status,
            NULL AS reviewdate,
            NULL AS bankstatementdeadlinedate,
            NULL AS deadlinedate,
            NULL AS resubmitteddate
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
        annual_report_logs.reviewdate,
        annual_report_logs.bankstatementdeadlinedate,
        annual_report_logs.deadlinedate,
        annual_report_logs.resubmitteddate
    FROM {target_schema}.annual_report_logs
    LEFT JOIN {target_schema}.persons
    ON persons.id = annual_report_logs.client_id
);
