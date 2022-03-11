CREATE SCHEMA IF NOT EXISTS pmf_reports_20220310_in1178;

SELECT distinct p.caserecnumber, a.id AS arl_id, a.status AS original_value, 'LODGED' AS expected_value
INTO pmf_reports_20220310_in1178.annual_report_log_updates
FROM persons p
INNER JOIN annual_report_logs a ON p.id = a.client_id
INNER JOIN annual_report_lodging_details d ON a.id = d.annual_report_log_id
WHERE a.status = 'RECEIVED'
AND d.datereportlodged IS NOT NULL
AND p.clientsource = 'CASRECMIGRATION';

SELECT a.*
INTO pmf_reports_20220310_in1178.annual_report_log_audit
FROM pmf_reports_20220310_in1178.annual_report_log_updates f
INNER JOIN annual_report_logs a ON a.id = f.arl_id;

BEGIN;
    UPDATE annual_report_logs a SET status = f.expected_value
    FROM pmf_reports_20220310_in1178.annual_report_log_updates f
    WHERE f.arl_id = a.id;
-- Run if counts incorrect
ROLLBACK;
-- Run if counts correct
COMMIT;

-- Validation script (should be 0)
SELECT caserecnumber, expected_value
FROM pmf_reports_20220310_in1178.annual_report_log_updates
except
SELECT p.caserecnumber, a.status
FROM persons p
INNER JOIN annual_report_logs a ON p.id = a.client_id
INNER JOIN annual_report_lodging_details d ON a.id = d.annual_report_log_id
WHERE d.datereportlodged IS NOT NULL
AND p.clientsource = 'CASRECMIGRATION';
