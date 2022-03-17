--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT distinct p.caserecnumber, a.id AS arl_id, a.status AS original_value, 'LODGED' AS expected_value
INTO {pmf_schema}.annual_report_log_updates
FROM persons p
INNER JOIN annual_report_logs a ON p.id = a.client_id
INNER JOIN annual_report_lodging_details d ON a.id = d.annual_report_log_id
WHERE a.status = 'RECEIVED'
AND d.datereportlodged IS NOT NULL
AND p.clientsource = 'CASRECMIGRATION';

--@audit_tag
SELECT a.*
INTO {pmf_schema}.annual_report_log_audit
FROM {pmf_schema}.annual_report_log_updates f
INNER JOIN annual_report_logs a ON a.id = f.arl_id;

--@update_tag
UPDATE annual_report_logs a SET status = f.expected_value
FROM {pmf_schema}.annual_report_log_updates f
WHERE f.arl_id = a.id;

--@validate_tag
SELECT caserecnumber, expected_value
FROM {pmf_schema}.annual_report_log_updates
EXCEPT
SELECT p.caserecnumber, a.status
FROM persons p
INNER JOIN annual_report_logs a ON p.id = a.client_id
INNER JOIN annual_report_lodging_details d ON a.id = d.annual_report_log_id
WHERE d.datereportlodged IS NOT NULL
AND p.clientsource = 'CASRECMIGRATION';
