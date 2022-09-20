-- Purpose: With Casrecmigration P1 and P2, timeline events were imported as casenotes
-- Add a timeline event with of most recent casenote, to provide a source date for Last Action date in FE

CREATE SCHEMA IF NOT EXISTS pmf_timeline_event_sw5926;

-- Work with migrated clients only (the dataset is 104k not 45m)
-- Expected: 104,326 / 7s
SELECT id, caserecnumber, clientsource, caseactorgroup
INTO pmf_timeline_event_sw5926.migratedclients
FROM persons p
WHERE type = 'actor_client'
AND clientsource IN('CASRECMIGRATION','CASRECMIGRATION_P2'); -- P3 all have a putaway notice

-- ...and their cases
-- Expected: 126,122 / 1s
SELECT
    p.id AS person_id,
    c.id AS case_id,
    c.caserecnumber
INTO pmf_timeline_event_sw5926.migratedcases
FROM pmf_timeline_event_sw5926.migratedclients p
INNER JOIN cases c
    ON c.client_id = p.id;

-- person_events_ids
-- Expected: 611,870 / 5s
SELECT
    pt.person_id,
    pt.timelineevent_id
INTO pmf_timeline_event_sw5926.person_timeline_event_ids
FROM pmf_timeline_event_sw5926.migratedclients p
INNER JOIN person_timeline pt
    ON pt.person_id = p.id;

CREATE INDEX idx_person_timeline_event_ids ON pmf_timeline_event_sw5926.person_timeline_event_ids USING btree (timelineevent_id);

-- gather full timeline data for person_events
-- Expected: 611,870 / 18s or 2:35
SELECT tid.person_id, te.eventtype, te.event
INTO pmf_timeline_event_sw5926.all_timeline_events
FROM pmf_timeline_event_sw5926.person_timeline_event_ids tid
INNER JOIN timeline_event te
    ON te.id = tid.timelineevent_id;

-- case_events_ids
-- Expected: 567,870 / 4s
SELECT
    c.person_id,
    c.case_id,
    ct.timelineevent_id
INTO pmf_timeline_event_sw5926.case_timeline_event_ids
FROM pmf_timeline_event_sw5926.migratedcases c
INNER JOIN case_timeline ct
    ON ct.case_id = c.case_id;

CREATE INDEX idx_case_timeline_event_ids ON pmf_timeline_event_sw5926.case_timeline_event_ids USING btree (timelineevent_id);

-- gather full timeline data for case_events
-- Expected: 567,870 / 1:12
INSERT INTO pmf_timeline_event_sw5926.all_timeline_events (
    SELECT tid.person_id, te.eventtype, te.event
    FROM pmf_timeline_event_sw5926.case_timeline_event_ids tid
    INNER JOIN timeline_event te
        ON te.id = tid.timelineevent_id
);

SELECT COUNT(1) FROM pmf_timeline_event_sw5926.all_timeline_events;
-- Expected: 1,179,740

SELECT DISTINCT eventtype FROM pmf_timeline_event_sw5926.all_timeline_events ORDER BY eventtype;

DELETE FROM pmf_timeline_event_sw5926.all_timeline_events WHERE event->'payload'->>'subject' = 'Migration Notice';
-- Expected: 104,326 / 10s

DELETE FROM pmf_timeline_event_sw5926.all_timeline_events WHERE eventtype = 'Opg\Core\Model\Event\Person\DeputyContactDetailsChanged';
-- Expected: 34,191 / 1s

DELETE FROM pmf_timeline_event_sw5926.all_timeline_events WHERE eventtype = 'Opg\Core\Model\Event\Person\PaDetailsChanged';
-- Expected: 74,367 / 1s

-- clients with events
-- Expected: 63,748 / 1s
SELECT DISTINCT person_id
INTO pmf_timeline_event_sw5926.clients_with_events
FROM pmf_timeline_event_sw5926.all_timeline_events;

-- clients without events
-- Expected: 40,578 / 1s
SELECT mc.id AS person_id, mc.caserecnumber
INTO pmf_timeline_event_sw5926.clients_without_events
FROM pmf_timeline_event_sw5926.migratedclients mc
LEFT JOIN pmf_timeline_event_sw5926.clients_with_events cwe
    ON cwe.person_id = mc.id
WHERE cwe.person_id IS NULL;

-- Verification step
-- 1. The clients without events really haven't got any PERSON events without the Migration notice
-- Expected: 0
SELECT COUNT(1)
FROM pmf_timeline_event_sw5926.clients_without_events cwoe
INNER JOIN pmf_timeline_event_sw5926.person_timeline_event_ids tid
    ON tid.person_id = cwoe.person_id
INNER JOIN timeline_event te
    ON te.id = tid.timelineevent_id
AND event->'payload'->>'subject' != 'Migration Notice';

-- 2. The clients without events really haven't got any CASE events without the exception eventtypes
-- Expected: 0
SELECT COUNT(1)
FROM pmf_timeline_event_sw5926.clients_without_events cwoe
INNER JOIN pmf_timeline_event_sw5926.case_timeline_event_ids tid
    ON tid.person_id = cwoe.person_id
INNER JOIN timeline_event te
    ON te.id = tid.timelineevent_id
WHERE eventtype != 'Opg\Core\Model\Event\Person\PaDetailsChanged'
AND eventtype != 'Opg\Core\Model\Event\Person\DeputyContactDetailsChanged';

-- Compile latest notes for clients without timeline events
-- Expected: 40,573 / 8s
SELECT *
INTO pmf_timeline_event_sw5926.latest_note
FROM (
    SELECT
        sn.*,
        row_number() OVER (PARTITION BY sn.person_id ORDER BY "createdtime" DESC) as rownum
    FROM pmf_timeline_event_sw5926.clients_without_events cwoe
    INNER JOIN supervision_notes sn
        ON sn.person_id = cwoe.person_id
) all_notes
WHERE rownum = 1;

-- Prepare timeline_event rows due to be inserted
-- Expected: (as above 40,573)
BEGIN;
SELECT
ln.person_id                     AS person_id,
nextval('timeline_event_id_seq') AS id,
ln.createdbyuser_id              AS user_id,
ln.createdtime                   AS timestamp,
'Opg\Core\Model\Event\Common\NoteCreated' AS eventtype,
format('{' ||
       '"class":"%s",' ||
       '"payload":{' ||
           '"ispersonandcaseevent":false,' ||
           '"isPersonEvent":true,' ||
           '"isCaseEvent":false,' ||
           '"courtReference":"%s",' ||
           '"direction":"%s",' ||
           '"type":"Case note",' ||
           '"eventDate":"%s",' ||
           '"subject":"",' ||
           '"notes":"Last action date updated",' ||
           '"personType":"Client",' ||
           '"personId":"%s",' ||
           '"personUid":"%s",' ||
           '"personName":"%s",' ||
           '"personCourtRef":"%s"' ||
       '}}',
    'Opg\\Core\\Model\\Event\\Common\\NoteCreated',
    p.caserecnumber,
    direction,
    to_char(createdtime, 'YYYY-MM-DD"T"HH:MI:SS+00:00'),
    p.id,
    CONCAT(substr(p.uid::varchar, 1, 4),'-',substr(p.uid::varchar, 5, 4),'-',substr(p.uid::varchar, 9, 4)),
    CONCAT(p.salutation,' ',p.firstname,' ',p.surname),
    p.caserecnumber
    )::json AS event
INTO pmf_timeline_event_sw5926.timeline_event_insert_audit
FROM pmf_timeline_event_sw5926.latest_note ln
INNER JOIN persons p ON p.id = ln.person_id;
COMMIT;

-- Prepare person_timeline rows due to be inserted
-- Expected: (as above 40,573)
BEGIN;
SELECT
    nextval('person_timeline_id_seq') AS id,
    tei.person_id AS person_id,
    tei.id AS timelineevent_id
INTO pmf_timeline_event_sw5926.person_timeline_insert_audit
FROM pmf_timeline_event_sw5926.timeline_event_insert_audit tei;
COMMIT;

-- Perform the inserts
-- 1. Validation pre insert:
-- Expected: 0
SELECT COUNT(1)
FROM pmf_timeline_event_sw5926.timeline_event_insert_audit prepared
INNER JOIN timeline_event te ON te.id = prepared.id;

-- Expected: 0
SELECT COUNT(1)
FROM pmf_timeline_event_sw5926.person_timeline_insert_audit prepared
INNER JOIN person_timeline pt ON pt.id = prepared.id;

BEGIN;

-- 2. Insert
-- Expected: (as above 40,573)
INSERT INTO timeline_event (id, user_id, timestamp, eventtype, event) (
    SELECT id, user_id, timestamp, eventtype, event FROM pmf_timeline_event_sw5926.timeline_event_insert_audit ORDER BY id ASC
);

-- Expected: (as above 40,573)
INSERT INTO person_timeline (id, person_id, timelineevent_id) (
    SELECT id, person_id, timelineevent_id FROM pmf_timeline_event_sw5926.person_timeline_insert_audit ORDER BY timelineevent_id
);

-- 3. Re-validate
-- Expected: (as above 40,573)
SELECT COUNT(1)
FROM pmf_timeline_event_sw5926.timeline_event_insert_audit prepared
INNER JOIN timeline_event te ON te.id = prepared.id;

-- Expected: (as above 40,573)
SELECT COUNT(1)
FROM pmf_timeline_event_sw5926.person_timeline_insert_audit prepared
INNER JOIN person_timeline pt ON pt.id = prepared.id;

COMMIT;

-- or ROLLBACK if validation not ok
ROLLBACK;
