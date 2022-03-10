DROP TABLE IF EXISTS casrec_csv.exceptions_person_timeline;

CREATE TABLE casrec_csv.exceptions_person_timeline(
    source text default NULL,
    target text default NULL,
    case_no text default NULL,
    validation_failure_reason text default NULL
);

INSERT INTO casrec_csv.exceptions_person_timeline (
    SELECT
        'persons/timeline_event' AS source,
        'person_timeline' AS target,
        failures.case_no,
        'No person_timeline record for persons.id = ' || failures.person_id || ', timeline_event.id = ' || failures.timelineevent_id AS validation_failure_reason
    FROM (
        -- source query
        SELECT
            p.id AS person_id,
            te.id AS timelineevent_id,
            p.caserecnumber AS case_no
        FROM {target_schema}.timeline_event te
        INNER JOIN {target_schema}.persons p
        ON te.event->'payload'->>'courtReference' = p.caserecnumber
        WHERE
            p.clientsource = '{clientsource}'
            AND te.event->'payload'->>'subject' = 'Migration Notice'

        EXCEPT

        -- target query
        SELECT
            person_id,
            timelineevent_id,
            p.caserecnumber AS case_no
        FROM {target_schema}.person_timeline pt
        INNER JOIN {target_schema}.persons p
        ON pt.person_id = p.id
    ) AS failures
);
