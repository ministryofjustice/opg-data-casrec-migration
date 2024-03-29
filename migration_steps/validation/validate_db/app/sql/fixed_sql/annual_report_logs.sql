DROP TABLE IF EXISTS {casrec_schema}.exceptions_annual_report_logs;

CREATE TABLE {casrec_schema}.exceptions_annual_report_logs(
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

INSERT INTO {casrec_schema}.exceptions_annual_report_logs(
    -- non-pending annual_report_logs derived from casrec account table
    WITH casrec_annual_report_logs AS (
        SELECT
            caserecnumber,
            reportingperiodenddate,
            reportingperiodstartdate,
            end_date,
            CAST(receiveddate AS date) AS receiveddate,
            CAST(NULLIF(revisedduedate, '') AS date) AS revisedduedate,
            numberofchaseletters,
            {casrec_schema}.report_element(full_status, 1) AS status,
            NULLIF({casrec_schema}.report_element(full_status, 3), '') AS reviewstatus,
            CAST(NULLIF(reviewdate, '') AS date) AS reviewdate
        FROM (
            SELECT
                caserecnumber,
                reportingperiodenddate,
                reportingperiodstartdate,
                end_date,
                receiveddate,
                revisedduedate,
                numberofchaseletters,
                {casrec_schema}.report_status(
                    {casrec_schema}.report_status_aggregate(
                        review_status, wd_count_end_date, receiveddate, lodged_date, reviewdate, next_yr_flag
                    )
                ) full_status,
                reviewdate
            FROM (
                SELECT
                    "Case" AS caserecnumber,
                    CAST(account."End Date" AS date) AS reportingperiodenddate,
                    CAST(account."End Date" AS date) - INTERVAL '1 year' + INTERVAL '1 day' AS reportingperiodstartdate,
                    account."End Date" AS end_date,
                    COALESCE(
                        NULLIF(account."Rcvd Date", ''),
                        NULLIF(account."Lodge Date", '')
                    ) AS receiveddate,
                    "Revise Date" AS revisedduedate,
                    0 AS numberofchaseletters,
                    {casrec_schema}.weekday_count(account."End Date") AS wd_count_end_date,
                    "Rev Stat" AS review_status,
                    "Lodge Date" AS lodged_date,
                    "Review Date" AS reviewdate,
                    "Next Yr" AS next_yr_flag
                FROM
                    {casrec_schema}.account
            ) AS account_annual_report_logs
        ) AS non_pending_annual_report_logs

        UNION

        -- pending annual_report_logs derived from casrec pat table
        SELECT
            "Case" AS caserecnumber,
            CAST(p."Report Due" AS date) AS reportingperiodenddate,
            active_cases.reportingperiodstartdate,
            p."Report Due" AS end_date,
            NULL AS receiveddate,
            NULL AS revisedduedate,
            0 AS numberofchaseletters,
            'PENDING' AS status,
            'NO_REVIEW' AS review_status,
            NULL AS reviewdate
        FROM
            {casrec_schema}.pat p

        INNER JOIN(
            SELECT account_case, reportingperiodstartdate
            FROM {casrec_schema}.order o
            INNER JOIN (
                SELECT
                    a."Case" as account_case,
                    CAST(a."End Date" AS date) + 1 as reportingperiodstartdate,
                    row_number() OVER (
                        PARTITION BY a."Case"
                        ORDER BY a."End Date" DESC
                    ) AS rownum
                FROM {casrec_schema}.account a
            ) AS cases
            ON o."Case" = cases.account_case
            WHERE cases.rownum = 1
            AND o."Ord Stat" = 'Active'
        ) AS active_cases

        ON p."Case" = active_cases.account_case

        WHERE p."Report Due" != ''
    ),
    cases_with_active_pa_pro_deputies AS (
        SELECT DISTINCT "Case"
        FROM {casrec_schema}.deputy d
        INNER JOIN {casrec_schema}.deputyship ds
        ON d."Deputy No" = ds."Deputy No"
        WHERE d."Dep Type" IN ('20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '60', '73', '90')
        AND d."Stat" = '1'
    )

    SELECT
        caserecnumber,
        reportingperiodenddate,
        CAST(reportingperiodstartdate AS date),
        CASE
            WHEN cwappd."Case" IS NOT NULL THEN transf_add_business_days(cast(end_date as date), 40)
            ELSE transf_calculate_duedate(end_date)
        END AS duedate,
        receiveddate,
        revisedduedate,
        numberofchaseletters,
        status,
        reviewstatus,
        reviewdate
    FROM casrec_annual_report_logs carl
    LEFT JOIN cases_with_active_pa_pro_deputies cwappd
    ON carl.caserecnumber = cwappd."Case"

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
