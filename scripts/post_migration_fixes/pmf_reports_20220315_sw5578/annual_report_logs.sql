CREATE SCHEMA IF NOT EXISTS pmf_reports_20220315_sw5578;

WITH report_updates AS (
    SELECT DISTINCT p.caserecnumber, arl.id AS arl_id, arl.status AS original_value, 'LODGED' AS expected_value
    FROM annual_report_logs arl
    INNER JOIN annual_report_lodging_details arld ON arld.annual_report_log_id = arl.id
    INNER JOIN persons p ON p.id = arl.client_id
    WHERE p.clientsource = 'CASRECMIGRATION'
    AND arl.status = 'INCOMPLETE'
    AND arld.bankstatementsreceived IS False
    AND arld.bankstatementdeadlinedate IS NOT NULL
    AND arld.lodgedstatus = 'REFERRED_FOR_REVIEW'

    UNION

    SELECT DISTINCT p.caserecnumber, arl.id AS arl_id, arl.status AS original_value, 'INCOMPLETE' AS expected_value
    FROM annual_report_logs arl
    INNER JOIN annual_report_lodging_details arld ON arld.annual_report_log_id = arl.id
    INNER JOIN persons p ON p.id = arl.client_id
    WHERE p.clientsource = 'CASRECMIGRATION'
    AND arl.status = 'LODGED'
    AND arld.deadlinedate IS NOT NULL
    AND arld.resubmitteddate IS NULL
)
SELECT *
INTO pmf_reports_20220315_sw5578.annual_report_log_updates
FROM report_updates;

SELECT arl.*
INTO pmf_reports_20220315_sw5578.annual_report_log_audit
FROM pmf_reports_20220315_sw5578.annual_report_log_updates u
INNER JOIN annual_report_logs arl ON arl.id = u.arl_id;

BEGIN;
    UPDATE annual_report_logs arl SET status = u.expected_value
    FROM pmf_reports_20220315_sw5578.annual_report_log_updates u
    WHERE u.arl_id = arl.id;
-- Run if counts incorrect
ROLLBACK;
-- Run if counts correct
COMMIT;

-- Validation script (should be 0)
SELECT caserecnumber, expected_value
FROM pmf_reports_20220315_sw5578.annual_report_log_updates
EXCEPT
SELECT p.caserecnumber, arl.status
FROM persons p
INNER JOIN annual_report_logs arl ON p.id = arl.client_id
INNER JOIN annual_report_lodging_details arld ON arl.id = arld.annual_report_log_id
WHERE p.clientsource = 'CASRECMIGRATION'
AND (
    (
        arl.status = 'LODGED'
        AND arld.bankstatementsreceived IS False
        AND arld.bankstatementdeadlinedate IS NOT NULL
        AND arld.lodgedstatus = 'REFERRED_FOR_REVIEW'
    )
    OR
    (
        arl.status = 'INCOMPLETE'
        AND arld.deadlinedate IS NOT NULL
        AND arld.resubmitteddate IS NULL
    )
);
