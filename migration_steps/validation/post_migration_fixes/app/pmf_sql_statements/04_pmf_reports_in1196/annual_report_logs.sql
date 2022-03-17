--Purpose: update annual report logs casesupervisionlevel to be equal to supervision_level_log's supervisionlevel
--where it's an active order and report log status is RECEIVED
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT distinct p.caserecnumber, a.id AS arl_id, a.casesupervisionlevel AS original_value, s.supervisionlevel AS expected_value
INTO {pmf_schema}.annual_report_log_updates
FROM persons p
INNER JOIN cases c ON c.client_id = p.id
INNER JOIN supervision_level_log s ON c.id = s.order_id
INNER JOIN annual_report_logs a ON p.id = a.client_id
WHERE c.orderstatus = 'ACTIVE'
AND a.status = 'RECEIVED'
AND p.clientsource = '{client_source}';

--@audit_tag
SELECT a.*
INTO {pmf_schema}.annual_report_log_audit
FROM {pmf_schema}.annual_report_log_updates f
INNER JOIN annual_report_logs a ON a.id = f.arl_id;

--@update_tag
UPDATE annual_report_logs a SET casesupervisionlevel = f.expected_value
FROM {pmf_schema}.annual_report_log_updates f
WHERE f.arl_id = a.id;

--@validate_tag
SELECT caserecnumber, expected_value
FROM {pmf_schema}.annual_report_log_updates
except
SELECT p.caserecnumber, a.casesupervisionlevel
FROM persons p
INNER JOIN cases c ON c.client_id = p.id
INNER JOIN supervision_level_log s ON c.id = s.order_id
INNER JOIN annual_report_logs a ON p.id = a.client_id
WHERE c.orderstatus = 'ACTIVE'
AND a.status = 'RECEIVED'
AND p.clientsource = '{client_source}';
