-- casrec_mapping.annual_report_logs is populated from:
-- SELECT
-- id AS sirius_id,
-- casrec_details->0->>'casrec_row_id' AS casrec_row_id
-- FROM integration.annual_report_logs
-- WHERE casrec_details != '{}'

-- 1. New schema per update pmf_[table]_[field]_[date]_[Jira]
CREATE SCHEMA if not exists pmf_annual_report_logs_reviewstatus_20220310_in1198;

-- 2. Build Update table: PK, original value, expected value
SELECT sirius_arl_id, original_reviewstatus, expected_reviewstatus
INTO pmf_annual_report_logs_reviewstatus_20220310_in1198.annual_report_logs_updates
FROM (
    SELECT
        sirius_arl_id,
        original_reviewstatus,
        'STAFF_PRESELECTED' AS expected_reviewstatus
    FROM (
        WITH
        -- casrec reporting periods with Rev Stat = 'S'
        casrec_s_accounts AS (
            SELECT
                casrec_row_id,
                "Case" AS casrec_case,
                "Rev Stat" AS casrec_rev_stat
            FROM casrec_csv.account
            WHERE "Rev Stat" = 'S'
        )
        SELECT
            arl.id AS sirius_arl_id,
            arl.reviewstatus AS original_reviewstatus
        FROM annual_report_logs arl
        INNER JOIN persons p
        ON arl.client_id = p.id
        INNER JOIN casrec_mapping.annual_report_logs cma
        ON cma.sirius_id = arl.id
        INNER JOIN casrec_s_accounts a
        ON cma.casrec_row_id = a.casrec_row_id
        WHERE p.clientsource IN ('CASRECMIGRATION')
        AND arl.status = 'PENDING'
    ) arls
) to_update;


-- 3. Build Audit Table - a complete snapshot of each row affected
SELECT arl.*
INTO pmf_annual_report_logs_reviewstatus_20220310_in1198.annual_report_logs_audit
FROM pmf_annual_report_logs_reviewstatus_20220310_in1198.annual_report_logs_updates up
INNER JOIN annual_report_logs arl ON arl.id = up.sirius_arl_id;


-- 4. Perform Update
BEGIN;
    UPDATE annual_report_logs
    SET reviewstatus = up.expected_reviewstatus
    FROM pmf_annual_report_logs_reviewstatus_20220310_in1198.annual_report_logs_updates up
    WHERE id = up.sirius_arl_id;

    -- 5. Validation
    -- Validation script (should be 0)
    SELECT sirius_arl_id, expected_reviewstatus
    FROM pmf_annual_report_logs_reviewstatus_20220310_in1198.annual_report_logs_updates
    EXCEPT
    SELECT arl.id, arl.reviewstatus
    FROM annual_report_logs arl
    INNER JOIN pmf_annual_report_logs_reviewstatus_20220310_in1198.annual_report_logs_audit au
    ON arl.id = au.id;

-- Rollback OR Commit
-- affected row count looks BAD: back out
ROLLBACK;
-- OR
-- affected row count correct: commit
COMMIT;
