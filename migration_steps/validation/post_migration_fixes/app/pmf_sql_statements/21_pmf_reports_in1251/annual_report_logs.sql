--Purpose: set lodgedstatus to acknowledged where review date exists but bankstatements have been received
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT caserecnumber, reportingperiodenddate, bankstatements, bankstatementdeadlinedate, reviewdate, reviewstatus, arld_id, current_lodgedstatus, expected_lodgedstatus
INTO {pmf_schema}.annual_report_lodging_details_updates
FROM
(
    SELECT
    p.caserecnumber,
    arl.reportingperiodenddate,
    CASE WHEN bankstatementsreceived is True THEN 1
    ELSE 0 END as bankstatements,
    bankstatementdeadlinedate,
    arld.lodgedstatus as current_lodgedstatus,
    arld.id as arld_id,
    arl.reviewdate,
    arl.reviewstatus,
    'ACKNOWLEDGED' as expected_lodgedstatus
    FROM persons p
    INNER JOIN cases c on c.client_id = p.id
    INNER JOIN annual_report_logs arl ON p.id = arl.client_id
    INNER JOIN annual_report_lodging_details arld ON arld.annual_report_log_id = arl.id
    WHERE p.clientsource = '{client_source}'
    AND c.orderstatus = 'ACTIVE'
) as a
WHERE bankstatements = 0
AND bankstatementdeadlinedate IS NOT NULL
AND reviewdate IS NOT NULL
AND current_lodgedstatus = 'REFERRED_FOR_REVIEW'
ORDER BY caserecnumber;

--@audit_tag
SELECT arld.*
INTO {pmf_schema}.annual_report_lodging_details_audit
FROM annual_report_lodging_details arld
INNER JOIN {pmf_schema}.annual_report_lodging_details_updates u ON arld.id = u.arld_id;

--@update_tag
UPDATE annual_report_lodging_details arld SET lodgedstatus = u.expected_lodgedstatus
FROM {pmf_schema}.annual_report_lodging_details_updates u
WHERE u.arld_id = arld.id;

--@validate_tag
SELECT
    arld_id,
    expected_lodgedstatus
FROM {pmf_schema}.annual_report_lodging_details_updates u
EXCEPT
SELECT
   arld.id,
   arld.lodgedstatus
FROM annual_report_lodging_details arld
INNER JOIN {pmf_schema}.annual_report_lodging_details_audit a
ON a.id = arld.id;









