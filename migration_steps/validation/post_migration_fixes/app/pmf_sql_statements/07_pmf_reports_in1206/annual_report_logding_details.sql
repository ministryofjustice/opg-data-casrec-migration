--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT
    distinct p.caserecnumber,
    arld.id AS arld_id,
    arld.lodgedstatus AS original_value,
    CASE
        WHEN arld.deadlinedate IS NOT NULL AND arld.resubmitteddate IS NULL THEN 'INCOMPLETE'
        WHEN arld.bankstatementdeadlinedate IS NOT NULL AND arld.bankstatementsreceived IS FALSE THEN 'REFERRED_FOR_REVIEW'
    END AS expected_value
INTO {pmf_schema}.annual_report_lodging_details_updates
FROM persons p
INNER JOIN annual_report_logs arl ON p.id = arl.client_id
INNER JOIN annual_report_lodging_details arld ON arl.id = arld.annual_report_log_id
WHERE p.clientsource = 'CASRECMIGRATION'
AND (
    arld.lodgedstatus IS NULL
    OR
    arld.lodgedstatus IN ('INCOMPLETE', 'REFERRED_FOR_REVIEW')
)
AND (
    (arld.deadlinedate IS NOT NULL AND arld.resubmitteddate IS NULL)
    OR
    (arld.bankstatementdeadlinedate IS NOT NULL AND arld.bankstatementsreceived IS FALSE)
);

--@audit_tag
SELECT arld.*
INTO {pmf_schema}.annual_report_lodging_details_audit
FROM {pmf_schema}.annual_report_lodging_details_updates u
INNER JOIN annual_report_lodging_details arld ON arld.id = u.arld_id;

--@update_tag
UPDATE annual_report_lodging_details arld SET lodgedstatus = u.expected_value
FROM {pmf_schema}.annual_report_lodging_details_updates u
WHERE u.arld_id = arld.id;

--@validate_tag
SELECT caserecnumber, expected_value
FROM {pmf_schema}.annual_report_lodging_details_updates
except
SELECT p.caserecnumber, arld.lodgedstatus
FROM persons p
INNER JOIN annual_report_logs arl ON p.id = arl.client_id
INNER JOIN annual_report_lodging_details arld ON arl.id = arld.annual_report_log_id
WHERE p.clientsource = 'CASRECMIGRATION'
AND (
    (arld.deadlinedate IS NOT NULL AND arld.resubmitteddate IS NULL)
    OR
    (arld.bankstatementdeadlinedate IS NOT NULL AND arld.bankstatementsreceived IS FALSE)
);
