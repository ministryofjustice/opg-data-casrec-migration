--Purpose: Update reviewstatus on annual_report_logs
--@setup_tag
CREATE SCHEMA if not exists {pmf_schema};

SELECT sirius_arl_id, original_reviewstatus, expected_reviewstatus
INTO {pmf_schema}.annual_report_logs_updates
FROM (
    SELECT
        sirius_arl_id,
        original_reviewstatus,
        'STAFF_PRESELECTED' AS expected_reviewstatus
    FROM (
        WITH
        -- most-recent reporting period rows with Rev Stat = 'S'
        casrec_latest_s_accounts AS (
            -- most-recent reporting period rows (via casrec account table)
            SELECT
                "Case" AS casrec_case,
                "Rev Stat" AS casrec_rev_stat
            FROM (
                SELECT "Case", "Rev Stat",
                row_number() OVER (PARTITION BY "Case" ORDER BY "End Date" DESC) as rownum
                FROM {casrec_schema}.account
            ) s_cases
            WHERE rownum = 1
            -- only keep the most-recent account rows with Rev Stat = 'S'
            AND "Rev Stat" = 'S'
        )
        -- inner join above to the most-recent reporting period rows to get the arls we're interested in;
        -- note that as we're starting from the annual_report_logs table, we know we're only
        -- getting reports associated with an active order in casrec, so we don't need to do
        -- any additional filtering here
        SELECT
            arl.id AS sirius_arl_id,
            arl.reviewstatus AS original_reviewstatus
        FROM annual_report_logs arl

        -- only modify annual_report_logs which have not changed since migration;
        -- this also implicitly restricts the modifications to annual_report_logs
        -- we created as we are using a casrec mapping table
        INNER JOIN {casrec_mapping}.annual_report_logs carl
        ON carl.sirius_id = arl.id
        AND carl.status = arl.status
        AND carl.reviewstatus = arl.reviewstatus

        INNER JOIN persons p
        ON arl.client_id = p.id

        INNER JOIN casrec_latest_s_accounts a
        ON p.caserecnumber = a.casrec_case
        WHERE arl.status = 'PENDING'
    ) arls
) to_update;

--@audit_tag
SELECT arl.*
INTO {pmf_schema}.annual_report_logs_audit
FROM {pmf_schema}.annual_report_logs_updates up
INNER JOIN annual_report_logs arl ON arl.id = up.sirius_arl_id;

--@update_tag
UPDATE annual_report_logs
SET reviewstatus = up.expected_reviewstatus
FROM {pmf_schema}.annual_report_logs_updates up
WHERE id = up.sirius_arl_id;

--@validate_tag
SELECT sirius_arl_id, expected_reviewstatus
FROM {pmf_schema}.annual_report_logs_updates
EXCEPT
SELECT arl.id, arl.reviewstatus
FROM annual_report_logs arl
INNER JOIN {pmf_schema}.annual_report_logs_audit au
ON arl.id = au.id;
