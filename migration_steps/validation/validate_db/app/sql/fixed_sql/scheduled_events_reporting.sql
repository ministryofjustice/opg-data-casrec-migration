DROP TABLE IF EXISTS casrec_csv.exceptions_scheduled_events_reporting;

CREATE TABLE casrec_csv.exceptions_scheduled_events_reporting(
    caserecnumber text default NULL,
    report_log_id text default NULL,
    version text default NULL,
    processed text default NULL,
    dueby text default NULL,
    enddate text default NULL
);

CREATE INDEX ix_scheduled_events_json_payload ON {target_schema}.scheduled_events USING BTREE ((event->'payload'->>'reportingPeriodId'));
CREATE INDEX ix_scheduled_events_json_clientid ON {target_schema}.scheduled_events USING BTREE ((event->'payload'->>'clientId'));
CREATE INDEX ix_scheduled_events_json_class ON {target_schema}.scheduled_events USING BTREE ((event->>'class'));

INSERT INTO casrec_csv.exceptions_scheduled_events_reporting(
	SELECT * FROM (
        SELECT
            persons.caserecnumber AS caserecnumber,
            annual_report_logs.id AS report_log_id,
            1 AS version,
            FALSE AS processed,
            annual_report_logs.reportingperiodenddate + INTERVAL '1 YEAR - 1 DAY' AS dueby,
            to_char(
                annual_report_logs.reportingperiodenddate + INTERVAL '1 YEAR',
                'YYYY-MM-DD"T"HH24:MI:SS+00:00'
            ) AS enddate
        FROM {target_schema}.annual_report_logs
	    LEFT JOIN {target_schema}.persons ON persons.id = annual_report_logs.client_id
	    WHERE persons.clientsource = 'CASRECMIGRATION'
            AND annual_report_logs.status = 'PENDING'
    ) AS sirius_reports_data

    EXCEPT

    SELECT * FROM (
        SELECT
            persons.caserecnumber AS caserecnumber,
            annual_report_logs.id AS report_log_id,
            scheduled_events.version AS version,
            scheduled_events.processed AS processed,
            scheduled_events.dueby AS dueby,
            scheduled_events.event->'payload'->>'endDate' AS enddate
        FROM
            {target_schema}.annual_report_logs
        LEFT JOIN {target_schema}.persons ON persons.id = annual_report_logs.client_id
        LEFT JOIN {target_schema}.scheduled_events
            ON scheduled_events.event->>'class' = 'Opg\Core\Model\Event\DeputyshipReporting\ScheduledReportingPeriodEndDate'
            AND scheduled_events.event->'payload'->>'clientId' = persons.id::text
            AND scheduled_events.event->'payload'->>'reportingPeriodId' = annual_report_logs.id::text
        WHERE persons.clientsource = 'CASRECMIGRATION'
            AND annual_report_logs.status = 'PENDING'
    ) AS sirius_events_data
);

DROP INDEX IF EXISTS ix_scheduled_events_json_payload;
DROP INDEX IF EXISTS ix_scheduled_events_json_clientid;
DROP INDEX IF EXISTS ix_scheduled_events_json_class;