CREATE TABLE IF NOT EXISTS countverification.lpa_persons (id int);
INSERT INTO countverification.lpa_persons (id)
SELECT id FROM persons p
WHERE p.type NOT IN (
    'actor_client',
    'actor_deputy',
    'actor_contact',
    'actor_non_case_contact'
); -- ~2m
CREATE UNIQUE INDEX lpa_persons_idx ON countverification.lpa_persons (id); -- ~1m

CREATE TABLE IF NOT EXISTS countverification.lpa_cases (id int);
INSERT INTO countverification.lpa_cases (id)
SELECT cases.id FROM cases WHERE type != 'order'; -- ~22s
CREATE UNIQUE INDEX lpa_cases_idx ON countverification.lpa_cases (id);

ALTER TABLE countverification.counts DROP COLUMN IF EXISTS {working_column};
ALTER TABLE countverification.counts ADD COLUMN {working_column} int;

-- persons (both)
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverification.lpa_persons
)
WHERE supervision_table = 'persons';

-- cases
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverification.lpa_cases
)
WHERE supervision_table = 'cases';

-- phonenumbers
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.lpa_persons lp
        ON lp.id = pn.person_id
)
WHERE supervision_table = 'phonenumbers';

-- addresses
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.lpa_persons lp
        ON lp.id = ad.person_id
)
WHERE supervision_table = 'addresses';

-- warnings
UPDATE countverification.counts
SET {working_column} =
    (
        SELECT COUNT(*)
        FROM warnings w
        INNER JOIN person_warning pw on pw.warning_id = w.id
        INNER JOIN countverification.lpa_persons lp
            ON lp.id = pw.person_id
    )
WHERE supervision_table = 'warnings';

-- timeline_event
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM timeline_event te
    INNER JOIN person_timeline pt
        ON pt.timelineevent_id = te.id
    INNER JOIN countverification.lpa_persons lp
        ON lp.id = pt.person_id
)
WHERE supervision_table = 'timeline_event';

-- person_caseitem
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM person_caseitem pci
    INNER JOIN countverification.lpa_persons lp
        ON lp.id = pci.person_id
)
WHERE supervision_table = 'person_caseitem';

-- person_warning
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.lpa_persons lp
        ON lp.id = pw.person_id
)
WHERE supervision_table = 'person_warning';

-- person_timeline
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN countverification.lpa_persons lp
        ON lp.id = pt.person_id
)
WHERE supervision_table = 'person_timeline';

-- The following have no connection to LPA (zero rows in Sirius) so have been skipped:
-- supervision_notes
-- tasks
-- death_notifications
-- annual_report_logs
-- annual_report_lodging_details
-- visits
-- bonds
-- feepayer_id
-- supervision_level_log
-- finance_invoice_ad
-- finance_invoice_non_ad
-- finance_remissions
-- finance_exemptions
-- order_deputy
-- person_task


DROP INDEX countverification.lpa_persons_idx;
DROP INDEX countverification.lpa_cases_idx;

DROP TABLE countverification.lpa_persons;
DROP TABLE countverification.lpa_cases;

