--Purpose: update supervision levels based on some fairly complex logic (see PR)
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT DISTINCT p.caserecnumber,
    arl.id AS arl_id,
    arl.casesupervisionlevel AS original_value,
    x.supervisionlevel AS expected_value
INTO {pmf_schema}.annual_report_log_updates
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
AND p.clientsource = '{client_source}';

--@audit_tag
SELECT arl.*
INTO {pmf_schema}.annual_report_log_audit
FROM annual_report_logs arl
INNER JOIN {pmf_schema}.annual_report_log_updates u ON arl.id = u.arl_id;

SELECT DISTINCT sll.*
INTO {pmf_schema}.supervision_level_log_audit
FROM supervision_level_log sll
INNER JOIN cases c ON c.id = sll.order_id
INNER JOIN annual_report_logs arl ON arl.client_id = c.client_id
INNER JOIN {pmf_schema}.annual_report_log_updates u ON arl.id = u.arl_id;

--@update_tag
UPDATE annual_report_logs arl SET casesupervisionlevel = u.expected_value
FROM {pmf_schema}.annual_report_log_updates u
WHERE u.arl_id = arl.id;

--@validate_tag
SELECT caserecnumber, expected_value
FROM {pmf_schema}.annual_report_log_updates
EXCEPT
SELECT p.caserecnumber, arl.casesupervisionlevel
FROM persons p
INNER JOIN annual_report_logs arl ON p.id = arl.client_id
WHERE p.clientsource = '{client_source}';
