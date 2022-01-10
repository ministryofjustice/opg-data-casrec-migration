DROP TABLE IF EXISTS casrec_csv.exceptions_timeline_event;

CREATE TABLE casrec_csv.exceptions_timeline_event(
    source text default NULL,
    target text default NULL,
    case_no text default NULL,
    validation_failure_reason text default NULL
);

-- when Title = 99, we expect title lookup to fail,
-- so timeline_event.event.payload.personName should not include a title
INSERT INTO casrec_csv.exceptions_timeline_event (
    SELECT
        'pat' AS source,
        'timeline_event' AS target,
        failures.case_no,
        'timeline_event event.payload.personName mismatch (Title lookup fail): ' || failures.person_name AS validation_failure_reason
    FROM (
        SELECT
            "Case" AS case_no,
            INITCAP(SPLIT_PART(TRIM("Forename"), ' ', 1)) || ' ' || INITCAP(TRIM("Surname")) AS person_name
        FROM casrec_csv.pat where CAST("Title" AS int) = 99

        EXCEPT

        SELECT
            event->'payload'->>'courtReference' AS case_no,
            event->'payload'->>'personName' AS person_name
        FROM {target_schema}.timeline_event
        WHERE
            event->'payload'->>'subject' = 'Migration Notice'
            AND event->'payload'->>'type' = 'Case note'
    ) AS failures
);

-- when Title != 99, we expect title to be in timeline_event.event.payload.personName
INSERT INTO casrec_csv.exceptions_timeline_event (
    SELECT
        'pat' AS source,
        'timeline_event' AS target,
        failures.case_no,
        'timeline_event event.payload.personName mismatch (Title lookup success): ' || failures.person_name AS validation_failure_reason
    FROM (
        SELECT
            "Case" AS case_no,
            casrec_csv.title_codes_lookup("Title") || ' ' || INITCAP(SPLIT_PART(TRIM("Forename"), ' ', 1)) || ' ' || INITCAP(TRIM("Surname")) AS person_name
        FROM casrec_csv.pat where CAST("Title" AS int) != 99

        EXCEPT

        SELECT
            event->'payload'->>'courtReference' AS case_no,
            event->'payload'->>'personName' AS person_name
        FROM {target_schema}.timeline_event
        WHERE
            event->'payload'->>'subject' = 'Migration Notice'
            AND event->'payload'->>'type' = 'Case note'
    ) AS failures
);

-- expect case ref to be put into the payload in two places
INSERT INTO casrec_csv.exceptions_timeline_event (
    SELECT
        'pat' AS source,
        'timeline_event' AS target,
        failures.case_no,
        'timeline_event event.payload has incorrect case no.' AS validation_failure_reason
    FROM (
        SELECT
            "Case" AS case_no,
            "Case" AS person_court_ref
        FROM casrec_csv.pat

        EXCEPT

        SELECT
            event->'payload'->>'courtReference' AS case_no,
            event->'payload'->>'personCourtRef' AS person_court_ref
        FROM {target_schema}.timeline_event
        WHERE
            event->'payload'->>'subject' = 'Migration Notice'
            AND event->'payload'->>'type' = 'Case note'
    ) AS failures
);

-- check format of event.payload.eventDate is correct (YYYY-MM-DD)
INSERT INTO casrec_csv.exceptions_timeline_event (
    SELECT
        'pat' AS source,
        'timeline_event' AS target,
        failures.case_no,
        'timeline_event event.payload.eventDate is invalid: ' || failures.payload AS validation_failure_reason
    FROM (
        SELECT
            event->'payload'->>'courtReference' AS case_no,
            event->>'payload' AS payload
        FROM {target_schema}.timeline_event
        WHERE
            event->'payload'->>'subject' = 'Migration Notice'
            AND event->'payload'->>'type' = 'Case note'

        EXCEPT

        SELECT
            event->'payload'->>'courtReference' AS case_no,
            event->>'payload' AS payload
        FROM {target_schema}.timeline_event
        WHERE
            event->'payload'->>'eventDate' similar to '[0-9]{4}-(0?[1-9]|1[012])-([12][0-9]|3[01]|0?[1-9])%'
            AND event->'payload'->>'subject' = 'Migration Notice'
            AND event->'payload'->>'type' = 'Case note'
    ) AS failures
);
