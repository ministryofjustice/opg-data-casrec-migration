-- get event IDs (for person_timeline only, there are no cases, so no case TE)
SELECT
    pt.person_id,
    pt.timelineevent_id
INTO deleted_cases_sw6081.client_nodocs_events_ids
FROM deleted_cases_sw6081.clients_selection cl
INNER JOIN person_timeline pt
    ON pt.person_id = cl.id;

-- use ids to get full events
SELECT tid.person_id, te.*
INTO deleted_cases_sw6081.clients_selection_timeline_events
FROM deleted_cases_sw6081.client_nodocs_events_ids tid
INNER JOIN timeline_event te
    ON te.id = tid.timelineevent_id;
DROP TABLE deleted_cases_sw6081.client_nodocs_events_ids;

-- Delete timeline events which do not contribute to establishing 'Last Action' in Sirius
DELETE FROM deleted_cases_sw6081.clients_selection_timeline_events WHERE event->'payload'->>'subject' = 'Migration Notice';
DELETE FROM deleted_cases_sw6081.clients_selection_timeline_events WHERE eventtype = 'Opg\Core\Model\Event\Person\DeputyContactDetailsChanged';
DELETE FROM deleted_cases_sw6081.clients_selection_timeline_events WHERE eventtype = 'Opg\Core\Model\Event\Person\PaDetailsChanged';

-- now assess last action based on available data
ALTER TABLE deleted_cases_sw6081.clients_selection ADD COLUMN latest_timestamp timestamp;
ALTER TABLE deleted_cases_sw6081.clients_selection ADD COLUMN latest_activity date;

-- calculate and update each row with last activity date
WITH latest_timeline AS(
    SELECT person_id, MAX(timestamp) as latest_timestamp
    FROM deleted_cases_sw6081.clients_selection_timeline_events te
    GROUP BY person_id
)
UPDATE deleted_cases_sw6081.clients_selection cl
SET latest_timestamp = t1.latest_timestamp,
    latest_activity = t1.latest_activity
FROM(
    SELECT
        cl.id,
        CAST(lt.latest_timestamp AS DATE),
        GREATEST(
            CAST(statusdate AS DATE),
            CAST(createddate AS DATE),
            CAST(updateddate AS DATE),
            CAST(lt.latest_timestamp AS DATE)
        ) AS latest_activity
    FROM deleted_cases_sw6081.clients_selection cl
    LEFT JOIN latest_timeline lt ON lt.person_id = cl.id
) t1
WHERE t1.id = cl.id;

DROP TABLE deleted_cases_sw6081.clients_selection_timeline_events;

INSERT INTO deleted_cases_sw6081.run_clients (
    SELECT
        id,
        caserecnumber,
        clientsource,
        caseactorgroup,
        supervisioncaseowner_id,
        statusdate,
        createddate,
        updateddate,
        latest_timestamp,
        latest_activity,
        :runId
    FROM deleted_cases_sw6081.clients_selection
--     WHERE latest_activity <= (current_date - INTERVAL '3 months')
);

DROP TABLE deleted_cases_sw6081.clients_selection;
