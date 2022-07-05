--Purpose: delete remaining pending reports above 1 that were missed in pmf5
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT count(*), ar.client_id
INTO {pmf_schema}.affected_cases
FROM annual_report_logs ar
INNER JOIN persons p ON p.id = ar.client_id
WHERE p.clientsource = '{client_source}' --Have this apply universally
AND ar.status = 'PENDING'
GROUP BY ar.client_id
HAVING count(*) > 1;

SELECT id, reportingperiodenddate
INTO {pmf_schema}.annual_report_logs_deletes
FROM
(
    SELECT row_number() OVER (partition by ar.client_id order by ar.reportingperiodenddate asc, ar.id asc) as rown,
    ar.id, ar.reportingperiodenddate
    FROM annual_report_logs ar
    INNER JOIN {pmf_schema}.affected_cases ac ON ac.client_id = ar.client_id
    WHERE ar.status = 'PENDING'
    ORDER BY ar.client_id
) as a
WHERE rown > 1;

--@audit_tag
SELECT ar.*
INTO {pmf_schema}.reports_audit
FROM {pmf_schema}.affected_cases ac
INNER JOIN annual_report_logs ar ON ar.client_id = ac.client_id;

--@update_tag
DELETE FROM annual_report_logs ar
USING {pmf_schema}.annual_report_logs_deletes rd
WHERE ar.id = rd.id;

--@validate_tag
SELECT count(*), ar.client_id
FROM annual_report_logs ar
INNER JOIN persons p ON p.id = ar.client_id
WHERE p.clientsource = '{client_source}'
AND ar.status = 'PENDING'
GROUP BY ar.client_id
HAVING count(*) > 1;
