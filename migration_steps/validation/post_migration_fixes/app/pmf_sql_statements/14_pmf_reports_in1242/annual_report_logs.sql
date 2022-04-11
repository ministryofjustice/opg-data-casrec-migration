--Purpose: update where users have entered Further dates but have not added the equivalent row Rcvd Date
--and have instead added review dates which maps to resubmitteddate on sirius side
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT
"Case",
"Further Date1",
"Further Date2",
"Further Date3",
"Further Date4",
"Further Date6",
"Further Date6.1",
"Rcvd Date1",
"Rcvd Date2",
"Rcvd Date3",
"Rcvd Date4",
"Rcvd Date5",
"Rcvd Date6",
arld.id as arld_id,
cast("Review Date" as date) as expected_value
INTO {pmf_schema}.annual_report_lodging_details_updates
FROM
(
    SELECT
    "Case",
    "casrec_row_id",
    CASE
    WHEN "Further Date1" != '' and "Rcvd Date1" = ''
    OR "Further Date2" != '' and "Rcvd Date2" = ''
    OR "Further Date3" != '' and "Rcvd Date3" = ''
    OR "Further Date4" != '' and "Rcvd Date4" = ''
    OR "Further Date6" != '' and "Rcvd Date5" = ''
    OR "Further Date6.1" != '' and "Rcvd Date6" = ''
    THEN 1 ELSE 0 END as mismatch,
    "Further Date1",
    "Further Date2",
    "Further Date3",
    "Further Date4",
    "Further Date6",
    "Further Date6.1",
    "Rcvd Date1",
    "Rcvd Date2",
    "Rcvd Date3",
    "Rcvd Date4",
    "Rcvd Date5",
    "Rcvd Date6",
    "Review Date"
    from {casrec_schema}.account
    where "Review Date" != ''
) as account_records
INNER JOIN {casrec_mapping}.annual_report_logs_casrec_id map
ON cast(map.casrec_row_id as int) = cast(account_records."casrec_row_id" as int)
INNER JOIN annual_report_logs arl on arl.id = map.id
INNER JOIN annual_report_lodging_details arld on arld.annual_report_log_id = arl.id
INNER JOIN persons p on p.id = arl.client_id
WHERE account_records.mismatch = 1
AND p.clientsource = '{client_source}';

--@audit_tag
SELECT arld.*
INTO {pmf_schema}.annual_report_log_audit
FROM annual_report_lodging_details arld
INNER JOIN {pmf_schema}.annual_report_lodging_details_updates u ON arld.id = u.arld_id;

--@update_tag
UPDATE annual_report_lodging_details arld SET resubmitteddate = u.expected_value
FROM {pmf_schema}.annual_report_lodging_details_updates u
WHERE u.arld_id = arld.id;

--@validate_tag
SELECT arld_id, cast(expected_value as date)
FROM {pmf_schema}.annual_report_lodging_details_updates
EXCEPT
SELECT arld.id, cast(arld.resubmitteddate as date)
FROM persons p
INNER JOIN annual_report_logs arl on p.id = arl.client_id
INNER JOIN annual_report_lodging_details arld on arld.annual_report_log_id = arl.id;

