CREATE SCHEMA IF NOT EXISTS pmf_reports_20220311_in1204;

-- DROP TABLE IF EXISTS pmf_reports_20220311_in1204.annual_report_log_updates;
-- DROP TABLE IF EXISTS pmf_reports_20220311_in1204.annual_report_log_audit;
-- DROP TABLE IF EXISTS pmf_reports_20220311_in1204.supervision_level_log_audit;

SELECT DISTINCT p.caserecnumber,
    arl.id AS arl_id,
    arl.casesupervisionlevel AS original_value,
    x.supervisionlevel AS expected_value
INTO pmf_reports_20220311_in1204.annual_report_log_updates
FROM annual_report_logs arl
INNER JOIN persons p ON p.id = arl.client_id
LEFT JOIN LATERAL (
    SELECT sll.supervisionlevel
    FROM supervision_level_log sll
    INNER JOIN cases c ON c.id = sll.order_id
    WHERE c.client_id = arl.client_id
    AND sll.appliesfrom <= arl.reportingperiodenddate
    ORDER BY sll.createddate DESC
    LIMIT 1
) x ON TRUE
WHERE arl.casesupervisionlevel IS NULL
AND p.clientsource = 'CASRECMIGRATION';

SELECT arl.*
INTO pmf_reports_20220311_in1204.annual_report_log_audit
FROM annual_report_logs arl
INNER JOIN pmf_reports_20220311_in1204.annual_report_log_updates u ON arl.id = u.arl_id;

SELECT DISTINCT sll.*
INTO pmf_reports_20220311_in1204.supervision_level_log_audit
FROM supervision_level_log sll
INNER JOIN cases c ON c.id = sll.order_id
INNER JOIN annual_report_logs arl ON arl.client_id = c.client_id
INNER JOIN pmf_reports_20220311_in1204.annual_report_log_updates u ON arl.id = u.arl_id;

BEGIN;
    UPDATE annual_report_logs arl SET casesupervisionlevel = u.expected_value
    FROM pmf_reports_20220311_in1204.annual_report_log_updates u
    WHERE u.arl_id = arl.id;
-- Run if counts incorrect
ROLLBACK;
-- Run if counts correct
COMMIT;

-- Validation script (should be 0)
SELECT caserecnumber, expected_value
FROM pmf_reports_20220311_in1204.annual_report_log_updates
EXCEPT
SELECT p.caserecnumber, arl.casesupervisionlevel
FROM persons p
INNER JOIN annual_report_logs arl ON p.id = arl.client_id
WHERE p.clientsource = 'CASRECMIGRATION';
