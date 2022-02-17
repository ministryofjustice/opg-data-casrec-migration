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

-- assignee_teams
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM assignee_teams
)
WHERE supervision_table = 'assignee_teams';

-- assignees
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM assignees
)
WHERE supervision_table = 'assignees';

-- caseitem_document
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM caseitem_document cd
    INNER JOIN countverification.lpa_cases c
        ON cd.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_document';

-- caseitem_note
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM caseitem_note cn
    INNER JOIN countverification.lpa_cases c
        ON cn.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_note';

-- caseitem_paymenttype
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM caseitem_paymenttype cpt
    INNER JOIN countverification.lpa_cases c
        ON cpt.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_paymenttype';

-- caseitem_task
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM caseitem_task ct
    INNER JOIN countverification.lpa_cases c
        ON ct.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_task';

-- caseitem_warning
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM caseitem_warning cw
    INNER JOIN countverification.lpa_cases c
    ON cw.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_warning';

-- complaints
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM complaints
)
WHERE supervision_table = 'complaints';

-- notes
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM notes n
    INNER JOIN person_note pn
        ON pn.note_id = n.id
    INNER JOIN countverification.lpa_persons lp
        ON lp.id = pn.person_id
)
WHERE supervision_table = 'notes';

-- pa_applicants
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM pa_applicants
)
WHERE supervision_table = 'pa_applicants';

-- pa_certificate_provider
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM pa_certificate_provider
)
WHERE supervision_table = 'pa_certificate_provider';

-- pa_notified_persons
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM pa_notified_persons
)
WHERE supervision_table = 'pa_notified_persons';

-- person_note
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM person_note pn
    INNER JOIN countverification.lpa_persons lp
        ON lp.id = pn.person_id
)
WHERE supervision_table = 'person_note';

-- powerofattorney_person
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM powerofattorney_person
)
WHERE supervision_table = 'powerofattorney_person';

-- documents
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM documents d
    INNER JOIN persons p
        ON p.id = d.correspondent_id
    WHERE p.type NOT IN (
        'actor_client',
        'actor_deputy',
        'actor_contact',
        'actor_non_case_contact'
    )
)
WHERE supervision_table = 'documents';

-- investigation
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM investigation i
    INNER JOIN persons p
        ON p.id = i.person_id
    WHERE p.type NOT IN (
         'actor_client',
         'actor_deputy',
         'actor_contact',
         'actor_non_case_contact'
    )
)
WHERE supervision_table = 'investigation';

-- validation_check
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM validation_check
)
WHERE supervision_table = 'validation_check';

-- visitor
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM visitor
)
WHERE supervision_table = 'visitor';

-- case_timeline
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM case_timeline ct
    INNER JOIN countverification.lpa_cases c
        ON c.id = ct.case_id
)
WHERE supervision_table = 'case_timeline';

-- hold_period
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM hold_period
)
WHERE supervision_table = 'hold_period';

-- person_document
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM person_document
)
WHERE supervision_table = 'person_document';

-- document_pages
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM document_pages
)
WHERE supervision_table = 'document_pages';

-- document_secondaryrecipient
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM document_secondaryrecipient
)
WHERE supervision_table = 'document_secondaryrecipient';

-- ingested_documents
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM ingested_documents
)
WHERE supervision_table = 'ingested_documents';



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

