--Purpose: delete last pending report if there are multiples and create scheduled event for the reminaing one
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

-- Capture affected cases that have multiple pending reports
SELECT count(*), ar.client_id
INTO {pmf_schema}.affected_cases
FROM annual_report_logs ar
INNER JOIN persons p ON p.id = ar.client_id
WHERE p.clientsource = '{client_source}'
AND ar.status = 'PENDING'
GROUP BY ar.client_id
HAVING count(*) > 1;

-- The last Pending report should be deleted where there are multiple Pending reports
SELECT DISTINCT ON (ar.client_id) ar.id
INTO {pmf_schema}.annual_report_logs_deletes
FROM annual_report_logs ar
INNER JOIN {pmf_schema}.affected_cases ac ON ac.client_id = ar.client_id
WHERE ar.status = 'PENDING'
ORDER BY ar.client_id, ar.reportingperiodenddate DESC;

-- A scheduled event should be created for the remaining Pending reports
SELECT
       ar.reportingperiodenddate + INTERVAL '1 DAY' as dueby,
       '{"class": "Opg\\Core\\Model\\Event\\DeputyshipReporting\\ScheduledReportingPeriodEndDate", '
            || '"payload": {"endDate": "' || TO_CHAR(ar.reportingperiodenddate, 'YYYY-MM-DD') || 'T00:00:00+00:00'
            || '", "clientId": ' || ar.client_id::text
            || ', "reportingPeriodId": ' || ar.id::text
            || '}}' as event,
       FALSE as processed,
       1 as version
INTO {pmf_schema}.scheduled_events_inserts
FROM annual_report_logs ar
INNER JOIN {pmf_schema}.affected_cases ac ON ac.client_id = ar.client_id
LEFT JOIN {pmf_schema}.annual_report_logs_deletes rd ON rd.id = ar.id
WHERE ar.status = 'PENDING'
AND rd.id IS NULL;

--@audit_tag
SELECT ar.*
INTO {pmf_schema}.reports_audit
FROM {pmf_schema}.affected_cases ac
INNER JOIN annual_report_logs ar ON ar.client_id = ac.client_id;

--@update_tag
DELETE FROM annual_report_logs ar
USING {pmf_schema}.annual_report_logs_deletes rd
WHERE ar.id = rd.id;

INSERT INTO scheduled_events (id, dueby, event, processed, version)
SELECT nextval('scheduled_events_id_seq'), sei.dueby, CAST(sei.event as json), sei.processed, sei.version
FROM {pmf_schema}.scheduled_events_inserts sei;

--@validate_tag
SELECT count(*), ar.client_id
FROM annual_report_logs ar
INNER JOIN persons p ON p.id = ar.client_id
WHERE p.clientsource = '{client_source}'
AND ar.status = 'PENDING'
GROUP BY ar.client_id
HAVING count(*) > 1;

-- Check that report logs have been deleted
SELECT COUNT(*)
FROM annual_report_logs ar
INNER JOIN {pmf_schema}.annual_report_logs_deletes rd ON rd.id = ar.id;

-- Check that scheduled events have been created for the remaining Pending reports
SELECT ar.id
FROM {pmf_schema}.affected_cases ac
INNER JOIN annual_report_logs ar ON ar.client_id = ac.client_id
LEFT JOIN scheduled_events se ON se.event->'payload'->>'reportingPeriodId' = ar.id::text
    AND se.event->'payload'->>'clientId' = ar.client_id::text
    AND se.event->>'class' = 'Opg\Core\Model\Event\DeputyshipReporting\ScheduledReportingPeriodEndDate'
WHERE ar.status = 'PENDING'
AND se.id IS NULL;
