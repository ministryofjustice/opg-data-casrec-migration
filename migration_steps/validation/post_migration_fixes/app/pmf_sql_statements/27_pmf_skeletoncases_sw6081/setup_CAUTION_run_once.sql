-- delete this

SELECT COUNT(1) FROM (

) t1;

SELECT * FROM deleted_cases_sw6081.deleted_timeline_event_audit ORDER BY id DESC LIMIT 10;

WITH latest_timeline AS(
    SELECT
    person_id,
    MAX(timestamp) as latest
    FROM deleted_cases_sw6081.deleted_person_timeline dpt
    INNER JOIN deleted_cases_sw6081.deleted_timeline_event_audit tea
        ON tea.id = dpt.timelineevent_id
    WHERE dpt.delete_run_id > 33
    -- AND timestamp > '2022-08-08 00:00:00'
    GROUP BY person_id
) --229
SELECT
    cl.id,
    cl.caserecnumber,
    cl.clientsource,
    cl.caseactorgroup,
    a.email,
    cl.statusdate,
    cl.createddate,
    cl.updateddate,
    cl.latest_activity client_latest_activity,
    cl.delete_run_id
    -- dtea.timestamp AS timeline_event_timestamp,
    -- timeline_assignees.email AS timeline_event_email,
    -- dtea.eventtype timeline_event_type,
    -- dtea.event
FROM deleted_cases_sw6081.run_clients cl
INNER JOIN assignees a
    ON cl.supervisioncaseowner_id = a.id
-- LEFT JOIN latest_timeline lt
--     ON lt.person_id = cl.id
-- LEFT JOIN deleted_cases_sw6081.deleted_person_timeline dpt
--     ON dpt.person_id = cl.id
-- LEFT JOIN deleted_cases_sw6081.deleted_timeline_event_audit dtea
--     ON dtea.id = dpt.timelineevent_id
-- LEFT JOIN assignees timeline_assignees
--     ON dtea.user_id = timeline_assignees.id
WHERE cl.latest_activity > '2022-08-08 00:00:00'
AND cl.delete_run_id > 33 -- new runs Nov 9th 34,35,36,37,38 @ 2000 each
ORDER BY cl.id, latest_activity DESC;

-- query missing client
SELECT
    p.id,
    dpc.id
    dpca.* 
    FROM 


-- end delete this




DROP SCHEMA IF EXISTS deleted_cases_sw6081 CASCADE;
CREATE SCHEMA IF NOT EXISTS deleted_cases_sw6081;

CREATE TABLE deleted_cases_sw6081.run (
    id int PRIMARY KEY,
    notes varchar(255),
    selections_made_at timestamp,
    deleted_at timestamp,
    clients_affected int
);
CREATE SEQUENCE deleted_cases_sw6081.deleterun_id_seq start 1 increment 1;

CREATE TABLE deleted_cases_sw6081.run_clients (
    id int NOT NULL,
    caserecnumber varchar(255),
    clientsource varchar(255),
    caseactorgroup varchar(255),
    supervisioncaseowner_id int,
    statusdate date,
    createddate timestamp,
    updateddate timestamp,
    latest_timestamp timestamp,
    latest_activity date,
    delete_run_id int
);
ALTER TABLE deleted_cases_sw6081.run_clients
    ADD CONSTRAINT fk_deleterunid
    foreign key (delete_run_id) references deleted_cases_sw6081.run
ON DELETE CASCADE;

-- MAIN SELECT - ALL CLIENTS WITH NO CASES
DROP TABLE IF EXISTS deleted_cases_sw6081.clients_nocases;
SELECT DISTINCT
    p.id,
    p.caserecnumber,
    p.clientsource,
    p.caseactorgroup,
    p.supervisioncaseowner_id,
    p.statusdate,
    p.createddate,
    p.updateddate
INTO deleted_cases_sw6081.clients_nocases
FROM persons p
LEFT JOIN cases c ON c.client_id = p.id
WHERE p.type = 'actor_client'-- supervision clients only
AND c.id IS NULL -- has no orders
ORDER BY p.id ASC;
CREATE INDEX idx_sw6081_clients_nocases_id ON deleted_cases_sw6081.clients_nocases USING btree (id);

DROP TABLE IF EXISTS deleted_cases_sw6081.clients_nocases_no_documents;
SELECT *
INTO deleted_cases_sw6081.clients_nocases_no_documents
FROM deleted_cases_sw6081.clients_nocases cl_nocases
LEFT JOIN person_document pd ON pd.person_id = cl_nocases.id
WHERE pd.document_id IS NULL
ORDER BY cl_nocases.id ASC;
CREATE INDEX idx_sw6081_clients_nocases_nodocs_id ON deleted_cases_sw6081.clients_nocases_no_documents USING btree (id);

DROP TABLE IF EXISTS deleted_cases_sw6081.clients_nocases_with_documents;
SELECT cl.*
INTO deleted_cases_sw6081.clients_nocases_with_documents
FROM deleted_cases_sw6081.clients_nocases cl
INNER JOIN (
    SELECT DISTINCT cl_nocases.id
    FROM deleted_cases_sw6081.clients_nocases cl_nocases
    LEFT JOIN person_document pd
        ON pd.person_id = cl_nocases.id
    WHERE pd.document_id IS NOT NULL
) t1
    ON t1.id = cl.id
ORDER BY cl.id ASC;
CREATE INDEX idx_sw6081_clients_nocases_withdocs_id ON deleted_cases_sw6081.clients_nocases_with_documents USING btree (id);

CREATE TABLE deleted_cases_sw6081.results (
    delete_table varchar(255)
);
INSERT INTO deleted_cases_sw6081.results VALUES
('addresses'),
('annual_report_logs'),
('annual_report_letter_status'),
('annual_report_type_assignments'),
('annual_report_lodging_details'),
('death_notifications'),
('finance_person'),
('finance_invoice'),
('finance_order'),
('finance_remission_exemption'),
('finance_invoice_fee_range'),
('finance_ledger'),
('finance_ledger_allocation'),
('person_note'),
('notes'),
('person_personreference'),
('person_references'),
('person_research_preferences'),
('person_task'),
('tasks'),
('person_timeline'),
('timeline_event'),
('person_warning'),
('warnings'),
('phonenumbers'),
('supervision_notes'),
('visits'),
('cases'),
('person_document'),
('document_pages'),
('document_secondaryrecipient'),
('documents'),
('persons_contacts'),
('persons_deputies'),
('persons_clients_audit');

-- tables to hold audit information

-- addresses
CREATE TABLE deleted_cases_sw6081.deleted_addresses(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_addresses_audit FROM addresses a WHERE False;

-- annual_report_logs
CREATE TABLE deleted_cases_sw6081.deleted_annual_report_logs(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_annual_report_logs_audit FROM annual_report_logs WHERE False;

-- annual_report_letter_status
CREATE TABLE deleted_cases_sw6081.deleted_annual_report_letter_status(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_annual_report_letter_status_audit FROM annual_report_letter_status WHERE False;

-- annual_report_type_assignments
CREATE TABLE deleted_cases_sw6081.deleted_annual_report_type_assignments(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_annual_report_type_assignments_audit FROM annual_report_type_assignments WHERE False;

-- annual_report_lodging_details
CREATE TABLE deleted_cases_sw6081.deleted_annual_report_lodging_details(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_annual_report_lodging_details_audit FROM annual_report_lodging_details WHERE False;

-- death_notifications
CREATE TABLE deleted_cases_sw6081.deleted_death_notifications(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_death_notifications_audit FROM death_notifications WHERE False;

-- finance_person (supervision schema)
CREATE TABLE deleted_cases_sw6081.deleted_finance_person(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_finance_person_audit FROM supervision.finance_person WHERE False;

-- finance_invoice (supervision schema)
CREATE TABLE deleted_cases_sw6081.deleted_finance_invoice(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_finance_invoice_audit FROM supervision.finance_invoice WHERE False;

-- finance_order (supervision schema)
CREATE TABLE deleted_cases_sw6081.deleted_finance_order(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_finance_order_audit FROM supervision.finance_order WHERE False;

-- finance_remission_exemption (supervision schema)
CREATE TABLE deleted_cases_sw6081.deleted_finance_remission_exemption(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_finance_remission_exemption_audit FROM supervision.finance_remission_exemption WHERE False;

-- finance_invoice_fee_range
CREATE TABLE deleted_cases_sw6081.deleted_finance_invoice_fee_range(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_finance_invoice_fee_range_audit FROM finance_invoice_fee_range WHERE False;

-- finance_ledger
CREATE TABLE deleted_cases_sw6081.deleted_finance_ledger(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_finance_ledger_audit FROM finance_ledger WHERE False;

-- finance_ledger_allocation
CREATE TABLE deleted_cases_sw6081.deleted_finance_ledger_allocation(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_finance_ledger_allocation_audit FROM finance_ledger_allocation WHERE False;

-- person_note
CREATE TABLE deleted_cases_sw6081.deleted_person_note(
    person_id int NOT NULL,
    note_id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_person_note_audit FROM person_note WHERE False;

-- notes
CREATE TABLE deleted_cases_sw6081.deleted_notes(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_notes_audit FROM notes WHERE False;

-- person_personreference
CREATE TABLE deleted_cases_sw6081.deleted_person_personreference(
    person_id int NOT NULL,
    person_reference_id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_person_personreference_audit FROM person_personreference WHERE False;

-- person_references
CREATE TABLE deleted_cases_sw6081.deleted_person_references(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_person_references_audit FROM person_references WHERE False;

-- person_research_preferences
CREATE TABLE deleted_cases_sw6081.deleted_person_research_preferences(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_person_research_preferences_audit FROM person_research_preferences WHERE False;

-- person_task
CREATE TABLE deleted_cases_sw6081.deleted_person_task(
    person_id int NOT NULL,
    task_id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_person_task_audit FROM person_task WHERE False;

-- tasks
CREATE TABLE deleted_cases_sw6081.deleted_tasks(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_tasks_audit FROM tasks WHERE False;

-- person_timeline
CREATE TABLE deleted_cases_sw6081.deleted_person_timeline(
    id int NOT NULL,
    person_id int NOT NULL,
    timelineevent_id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_person_timeline_audit FROM person_timeline WHERE False;

-- timeline_event
CREATE TABLE deleted_cases_sw6081.deleted_timeline_event(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_timeline_event_audit FROM timeline_event WHERE False;

-- person_warning
CREATE TABLE deleted_cases_sw6081.deleted_person_warning(
    person_id int NOT NULL,
    warning_id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_person_warning_audit FROM person_warning WHERE False;

-- warnings
CREATE TABLE deleted_cases_sw6081.deleted_warnings(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_warnings_audit FROM warnings WHERE False;

-- phonenumbers
CREATE TABLE deleted_cases_sw6081.deleted_phonenumbers(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_phonenumbers_audit FROM phonenumbers WHERE False;

-- supervision_notes
CREATE TABLE deleted_cases_sw6081.deleted_supervision_notes(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_supervision_notes_audit FROM supervision_notes WHERE False;

-- visits
CREATE TABLE deleted_cases_sw6081.deleted_visits(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_visits_audit FROM visits WHERE False;

-- cases (should be zero at all times)
CREATE TABLE deleted_cases_sw6081.deleted_cases(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_cases_audit FROM cases WHERE False;

-- person_document
CREATE TABLE deleted_cases_sw6081.deleted_person_document(
    person_id int NOT NULL,
    document_id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_person_document_audit FROM person_document WHERE False;

-- document_pages
CREATE TABLE deleted_cases_sw6081.deleted_document_pages(
    id int NOT NULL,
    document_id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_document_pages_audit FROM document_pages WHERE False;

-- document_secondaryrecipient
CREATE TABLE deleted_cases_sw6081.deleted_document_secondaryrecipient(
    document_id int NOT NULL,
    person_id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_document_secondaryrecipient_audit FROM document_secondaryrecipient WHERE False;

-- document
CREATE TABLE deleted_cases_sw6081.deleted_documents(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_documents_audit FROM documents WHERE False;

-- persons (contacts)
CREATE TABLE deleted_cases_sw6081.deleted_persons_contacts(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_persons_contacts_audit FROM persons WHERE False;

-- persons (deputies)
CREATE TABLE deleted_cases_sw6081.deleted_persons_deputies(
    id int NOT NULL,
    delete_run_id int NOT NULL
);
SELECT * INTO deleted_cases_sw6081.deleted_persons_deputies_audit FROM persons WHERE False;

-- persons (clients)
SELECT * INTO deleted_cases_sw6081.deleted_persons_clients_audit FROM persons WHERE False;