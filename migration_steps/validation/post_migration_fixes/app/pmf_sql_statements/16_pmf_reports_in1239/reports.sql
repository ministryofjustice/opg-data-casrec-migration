--Purpose: Create pending report for active orders which don't have such a report already
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

WITH relevant_orders AS (
    SELECT DISTINCT
        p.caserecnumber,
        CAST(c.orderdate AS date) AS orderdate,
        c.id AS order_id,
        c.client_id AS client_id
    FROM persons p
    LEFT JOIN annual_report_logs arl
    ON p.id = arl.client_id
    LEFT JOIN cases c
    ON c.client_id = p.id
    WHERE p.type = 'actor_client'
    AND p.clientsource IN ('CASRECMIGRATION', 'CASRECMIGRATION_P2')
    AND c.orderstatus = 'ACTIVE'
    AND arl.id IS NULL
),
pa_pro_cases_with_active_deputies AS (
    SELECT DISTINCT c.caserecnumber
    FROM order_deputy od
    INNER JOIN cases c
    ON od.order_id = c.id
    WHERE od.statusoncase = 'ACTIVE'
    AND od.statusoncaseoverride IS NULL
    AND od.deputytype IN ('PA', 'PRO')
)
SELECT *
INTO {pmf_schema}.annual_report_logs_inserts
FROM (
    SELECT
        'PENDING' AS status,
        'NO_REVIEW' AS reviewstatus,
        0 AS numberofchaseletters,
        ro.orderdate + INTERVAL '1 day' AS reportingperiodstartdate,
        ro.orderdate + INTERVAL '366 days' AS reportingperiodenddate,
        -- duedate = reportingperiodenddate + 21 days for Lay (shifting to next working day if on a weekend),
        -- reportingperiodenddate + 40 working days for PA/PRO
        (
            CASE
                WHEN
                    ro.caserecnumber IN (SELECT caserecnumber FROM pa_pro_cases_with_active_deputies)
                THEN
                    {casrec_mapping}.transf_add_business_days(CAST((ro.orderdate + INTERVAL '366 days') AS date), 40)
                ELSE
                    {casrec_mapping}.transf_calculate_duedate(CAST((ro.orderdate + INTERVAL '366 days') AS date))
            END
        ) AS duedate,
        ro.order_id AS order_id,
        ro.client_id AS client_id
    FROM relevant_orders ro
    LEFT JOIN annual_report_logs arl
    ON ro.order_id = arl.order_id
    AND ro.client_id = arl.client_id
    WHERE arl.id IS NULL
) arls_to_insert;

-- Active orders with no account which don't have an
-- annual_report_logs row
SELECT *
INTO {pmf_schema}.annual_report_logs_missing
FROM (
    SELECT DISTINCT
        'PENDING' AS status,
        'NO_REVIEW' AS reviewstatus,
        c.id AS order_id,
        c.client_id AS client_id
    FROM persons p
    LEFT JOIN annual_report_logs arl
        ON p.id = arl.client_id
    LEFT JOIN cases c
        ON c.client_id = p.id
    WHERE p.type = 'actor_client'
    AND p.clientsource IN ('CASRECMIGRATION', 'CASRECMIGRATION_P2')
    AND c.orderstatus = 'ACTIVE'
    AND arl.id IS NULL
) active_orders_without_arls;

--@update_tag
-- Construct the rows to be inserted within the @update_tag, so that they
-- happen inside a transaction (as we are adding new rows, we want to keep
-- an audit trail of their IDs so we can remove them again if necessary)
SELECT
    nextval('annual_report_logs_id_seq') AS id,
    ins.*
INTO {pmf_schema}.annual_report_logs_inserts_audit
FROM {pmf_schema}.annual_report_logs_inserts ins;

-- The insert uses the audit table, as this has IDs in it
INSERT INTO annual_report_logs (
    id, status, reviewstatus, numberofchaseletters,
    reportingperiodstartdate, reportingperiodenddate,
    duedate, order_id, client_id
)
SELECT *
FROM {pmf_schema}.annual_report_logs_inserts_audit;

--@validate_tag
SELECT * FROM (
    SELECT
        (
            SELECT COUNT(*) FROM (
                -- Migrated cases without a pending report (before this pmf)
                SELECT *
                FROM {pmf_schema}.annual_report_logs_missing
                EXCEPT
                -- Migrated cases with a pending annual report (after this pmf)
                SELECT status, reviewstatus, order_id, client_id
                FROM {pmf_schema}.annual_report_logs_inserts
            ) a
        ) AS count_diff,
        (
            SELECT COUNT(*)
            FROM {pmf_schema}.annual_report_logs_missing
        ) AS count_missing,
        (
            SELECT COUNT(*)
            FROM {pmf_schema}.annual_report_logs_inserts
        ) AS count_added
) b
WHERE count_diff != 0
OR count_missing != count_added;