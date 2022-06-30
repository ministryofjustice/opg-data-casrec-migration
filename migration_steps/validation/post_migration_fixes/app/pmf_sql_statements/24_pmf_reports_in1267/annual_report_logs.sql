--Purpose: Remove reports on P3 deputies that are prior to first order date AS they were entered erroneously
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

WITH earliest_order AS
(SELECT DISTINCT ON (p.caserecnumber) p.caserecnumber, c.orderdate
FROM persons p
INNER JOIN cases c ON c.client_id = p.id
WHERE p.clientsource = 'CASRECMIGRATION_P3' --Only run for this phase
AND p.type = 'actor_client'
order by p.caserecnumber, c.orderdate ASC)
SELECT p.caserecnumber, arl.id AS arl_id, arld.id AS arld_id
INTO {pmf_schema}.annual_report_log_deletions
FROM annual_report_logs arl
INNER JOIN persons p ON p.id = arl.client_id
INNER JOIN earliest_order eo ON eo.caserecnumber = p.caserecnumber
LEFT JOIN annual_report_lodging_details arld ON arl.id = arld.annual_report_log_id
WHERE (arl.reportingperiodenddate::timestamp < eo.orderdate::timestamp)
OR (arl.reportingperiodstartdate::timestamp < '2007-10-01 00:00:00'::timestamp);

--@audit_tag
SELECT arl.*
INTO {pmf_schema}.annual_report_logs_audit
FROM annual_report_logs arl
INNER JOIN {pmf_schema}.annual_report_log_deletions del ON arl.id = del.arl_id;

SELECT arld.*
INTO {pmf_schema}.annual_report_lodging_details_audit
FROM annual_report_lodging_details arld
INNER JOIN {pmf_schema}.annual_report_log_deletions del ON arld.id = del.arld_id;

--@update_tag
DELETE FROM annual_report_lodging_details
WHERE id IN (SELECT id FROM {pmf_schema}.annual_report_lodging_details_audit);

DELETE FROM annual_report_logs
WHERE id IN (SELECT id FROM {pmf_schema}.annual_report_logs_audit);

--@validate_tag
SELECT arl.*
FROM {pmf_schema}.annual_report_logs_audit arla
INNER JOIN annual_report_logs arl ON arl.id = arla.id;

SELECT arld.*
FROM {pmf_schema}.annual_report_lodging_details_audit arlda
INNER JOIN annual_report_lodging_details arld ON arld.id = arlda.id;