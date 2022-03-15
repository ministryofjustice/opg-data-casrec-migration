CREATE TABLE IF NOT EXISTS {count_schema}.lpa_persons (id int);
INSERT INTO {count_schema}.lpa_persons (id)
SELECT id FROM persons p
WHERE p.type NOT IN (
    'actor_client',
    'actor_deputy',
    'actor_contact',
    'actor_non_case_contact'
); -- ~2m
CREATE UNIQUE INDEX lpa_persons_idx ON {count_schema}.lpa_persons (id); -- ~1m

CREATE TABLE IF NOT EXISTS {count_schema}.lpa_cases (id int);
INSERT INTO {count_schema}.lpa_cases (id)
SELECT cases.id FROM cases WHERE type != 'order'; -- ~22s
CREATE UNIQUE INDEX lpa_cases_idx ON {count_schema}.lpa_cases (id);

ALTER TABLE {count_schema}.counts DROP COLUMN IF EXISTS {working_column};
ALTER TABLE {count_schema}.counts ADD COLUMN {working_column} int;

-- persons (both)
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM {count_schema}.lpa_persons
)
WHERE supervision_table = 'persons';

-- cases
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM {count_schema}.lpa_cases
)
WHERE supervision_table = 'cases';

-- phonenumbers
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN {count_schema}.lpa_persons lp
        ON lp.id = pn.person_id
)
WHERE supervision_table = 'phonenumbers';

-- addresses
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN {count_schema}.lpa_persons lp
        ON lp.id = ad.person_id
)
WHERE supervision_table = 'addresses';

-- warnings
UPDATE {count_schema}.counts
SET {working_column} =
    (
        SELECT COUNT(*)
        FROM warnings w
        INNER JOIN person_warning pw on pw.warning_id = w.id
        INNER JOIN {count_schema}.lpa_persons lp
            ON lp.id = pw.person_id
    )
WHERE supervision_table = 'warnings';

-- timeline_event
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM timeline_event te
    INNER JOIN person_timeline pt
        ON pt.timelineevent_id = te.id
    INNER JOIN {count_schema}.lpa_persons lp
        ON lp.id = pt.person_id
)
WHERE supervision_table = 'timeline_event';

-- person_caseitem
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM person_caseitem pci
    INNER JOIN {count_schema}.lpa_persons lp
        ON lp.id = pci.person_id
)
WHERE supervision_table = 'person_caseitem';

-- person_warning
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN {count_schema}.lpa_persons lp
        ON lp.id = pw.person_id
)
WHERE supervision_table = 'person_warning';

-- person_timeline
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN {count_schema}.lpa_persons lp
        ON lp.id = pt.person_id
)
WHERE supervision_table = 'person_timeline';

-- assignee_teams
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM assignee_teams
)
WHERE supervision_table = 'assignee_teams';

-- assignees
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM assignees
)
WHERE supervision_table = 'assignees';

-- caseitem_document
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM caseitem_document cd
    INNER JOIN {count_schema}.lpa_cases c
        ON cd.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_document';

-- caseitem_note
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM caseitem_note cn
    INNER JOIN {count_schema}.lpa_cases c
        ON cn.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_note';

-- caseitem_paymenttype
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM caseitem_paymenttype cpt
    INNER JOIN {count_schema}.lpa_cases c
        ON cpt.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_paymenttype';

-- caseitem_task
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM caseitem_task ct
    INNER JOIN {count_schema}.lpa_cases c
        ON ct.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_task';

-- caseitem_warning
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM caseitem_warning cw
    INNER JOIN {count_schema}.lpa_cases c
    ON cw.caseitem_id = c.id
)
WHERE supervision_table = 'caseitem_warning';

-- complaints
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM complaints
)
WHERE supervision_table = 'complaints';

-- notes
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM notes n
    INNER JOIN person_note pn
        ON pn.note_id = n.id
    INNER JOIN {count_schema}.lpa_persons lp
        ON lp.id = pn.person_id
)
WHERE supervision_table = 'notes';

-- pa_applicants
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM pa_applicants
)
WHERE supervision_table = 'pa_applicants';

-- pa_certificate_provider
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM pa_certificate_provider
)
WHERE supervision_table = 'pa_certificate_provider';

-- pa_notified_persons
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM pa_notified_persons
)
WHERE supervision_table = 'pa_notified_persons';

-- person_note
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM person_note pn
    INNER JOIN {count_schema}.lpa_persons lp
        ON lp.id = pn.person_id
)
WHERE supervision_table = 'person_note';

-- powerofattorney_person
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM powerofattorney_person
)
WHERE supervision_table = 'powerofattorney_person';

-- documents
UPDATE {count_schema}.counts
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
UPDATE {count_schema}.counts
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
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM validation_check
)
WHERE supervision_table = 'validation_check';

-- visitor
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM visitor
)
WHERE supervision_table = 'visitor';

-- case_timeline
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM case_timeline ct
    INNER JOIN {count_schema}.lpa_cases c
        ON c.id = ct.case_id
)
WHERE supervision_table = 'case_timeline';

-- hold_period
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM hold_period
)
WHERE supervision_table = 'hold_period';

-- person_document
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM person_document pt
    INNER JOIN {count_schema}.lpa_persons lpa
    ON lpa.id = pt.person_id
)
WHERE supervision_table = 'person_document';

-- document_pages
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM document_pages
)
WHERE supervision_table = 'document_pages';

-- document_secondaryrecipient
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM document_secondaryrecipient
)
WHERE supervision_table = 'document_secondaryrecipient';

-- ingested_documents
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM ingested_documents
)
WHERE supervision_table = 'ingested_documents';

-- caseitem_queue
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM caseitem_queue
)
WHERE supervision_table = 'caseitem_queue';

-- finance_invoice_email_status
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM finance_invoice_email_status
)
WHERE supervision_table = 'finance_invoice_email_status';

-- finance_invoice_fee_range
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM finance_invoice_fee_range
)
WHERE supervision_table = 'finance_invoice_fee_range';

-- finance_report
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM finance_report
)
WHERE supervision_table = 'finance_report';

-- opgcore_doctrine_migrations
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM opgcore_doctrine_migrations
)
WHERE supervision_table = 'opgcore_doctrine_migrations';

-- person_personreference
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM person_personreference
)
WHERE supervision_table = 'person_personreference';

-- person_references
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM person_references
)
WHERE supervision_table = 'person_references';

-- person_research_preferences
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM person_research_preferences
)
WHERE supervision_table = 'person_research_preferences';

-- queue_business_rules
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM queue_business_rules
)
WHERE supervision_table = 'queue_business_rules';

-- scheduled_events
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM scheduled_events
)
WHERE supervision_table = 'scheduled_events';

-- uploads
update {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM uploads
)
WHERE supervision_table = 'uploads';

-- The following have no connection to LPA (zero rows in Sirius) so have been skipped:
-- supervision_notes
-- tasks
-- death_notifications
-- annual_report_logs
-- annual_report_lodging_details
-- annual_report_letter_status
-- annual_report_type_assignments
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

-- The following are tables that don't seem to be used or are 0 count
-- courtfund
-- deputy_important_information
-- finance_property
-- deleted_cases
-- order_courtfund
-- payments
-- finance_counter
-- finance_fee
-- epa_personnotifydonor
-- lineitem
-- bond_providers
-- random_review_settings
-- firm


-- total_documents (adding this here as just want to see count staying the same)
UPDATE {count_schema}.counts
SET {working_column} = (
    SELECT COUNT(*) FROM documents d
)
WHERE supervision_table = 'total_documents';

DROP INDEX {count_schema}.lpa_persons_idx;
DROP INDEX {count_schema}.lpa_cases_idx;

DROP TABLE {count_schema}.lpa_persons;
DROP TABLE {count_schema}.lpa_cases;

