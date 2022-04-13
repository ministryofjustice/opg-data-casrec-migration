--Purpose: add scheduled event for each PENDING annual_report_logs row just added
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

-- Create a scheduled event for each PENDING report we just added
SELECT
   arl.reportingperiodenddate + INTERVAL '1 DAY' AS dueby,
   '{"class": "Opg\\Core\\Model\\Event\\DeputyshipReporting\\ScheduledReportingPeriodEndDate", '
        || '"payload": {"endDate": "' || TO_CHAR(arl.reportingperiodenddate, 'YYYY-MM-DD') || 'T00:00:00+00:00'
        || '", "clientId": ' || arl.client_id::text
        || ', "reportingPeriodId": ' || arl.id::text
        || '}}' AS event,
   FALSE AS processed,
   1 AS version
INTO {pmf_schema}.scheduled_events_inserts
FROM annual_report_logs arl
INNER JOIN {pmf_schema}.annual_report_logs_inserts_audit arlia
ON arl.id = arlia.id;

--@audit_tag
-- nothing to see here

--@update_tag
-- audit table is constructed inside the transaction; that way we have a clear
-- undo path as we know the IDs of rows we added
SELECT nextval('scheduled_events_id_seq') AS id, sei.dueby, CAST(sei.event AS json), sei.processed, sei.version
INTO {pmf_schema}.scheduled_events_inserts_audit
FROM {pmf_schema}.scheduled_events_inserts sei;

INSERT INTO scheduled_events (id, dueby, event, processed, version)
SELECT seia.id, seia.dueby, seia.event, seia.processed, seia.version
FROM {pmf_schema}.scheduled_events_inserts_audit seia;

--@validate_tag
-- Check that scheduled events have been created for the PENDING reports
SELECT ar.id
FROM {pmf_schema}.annual_report_logs_inserts_audit arlia
INNER JOIN annual_report_logs arl ON arl.id = arlia.id
LEFT JOIN scheduled_events se ON se.event->'payload'->>'reportingPeriodId' = arlia.id::text
    AND se.event->'payload'->>'clientId' = arlia.client_id::text
    AND se.event->>'class' = 'Opg\Core\Model\Event\DeputyshipReporting\ScheduledReportingPeriodEndDate'
WHERE arl.status = 'PENDING'
AND se.id IS NULL;
