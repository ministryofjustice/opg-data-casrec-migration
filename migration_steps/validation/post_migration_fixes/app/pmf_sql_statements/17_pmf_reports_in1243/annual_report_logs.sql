--Purpose: update report logs - set pending reports with date range > 1 year back to 365 days
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT *
INTO {pmf_schema}.arl_updates
FROM (
    SELECT
        p.caserecnumber,
        arl.id AS arl_id,
        reportingperiodenddate,
        (reportingperiodenddate - INTERVAL '364 DAY')::DATE AS startdate_expected,
        (reportingperiodenddate::DATE - (reportingperiodenddate - INTERVAL '364 DAY')::DATE) diff_days_expected,
        reportingperiodstartdate AS startdate_actual,
        (reportingperiodenddate::DATE - reportingperiodstartdate::DATE) diff_days_actual
    FROM annual_report_logs arl
    LEFT JOIN persons p
    ON p.id = arl.client_id
    WHERE p.clientsource = '{client_source}'
) to_update
WHERE to_update.diff_days_actual > 365
ORDER BY to_update.diff_days_actual DESC;

--@audit_tag
SELECT arl.*
INTO {pmf_schema}.arl_audit
FROM annual_report_logs arl
INNER JOIN {pmf_schema}.arl_updates u ON arl.id = u.arl_id;

--@update_tag
UPDATE annual_report_logs arl SET reportingperiodstartdate = u.startdate_expected
FROM {pmf_schema}.arl_updates u
WHERE u.arl_id = arl.id;

--@validate_tag
SELECT
    arl_id,
    startdate_expected
FROM {pmf_schema}.arl_updates u
EXCEPT
SELECT
       arl.id,
       arl.reportingperiodstartdate
FROM annual_report_logs arl
INNER JOIN {pmf_schema}.arl_audit a
    ON a.id = arl.id;
