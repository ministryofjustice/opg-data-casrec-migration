DROP SCHEMA IF EXISTS deletions CASCADE;
CREATE SCHEMA deletions;

CREATE TABLE IF NOT EXISTS deletions.base_clients_persons (id int);
INSERT INTO deletions.base_clients_persons (id)
SELECT distinct p.id
FROM persons p ;

CREATE UNIQUE INDEX stub_person_id_idx ON deletions.base_clients_persons (id);

CREATE TABLE IF NOT EXISTS deletions.temp_documents_on_cases(
    documentId int,
    caseType VARCHAR(255),
    clientId int,
    dateMoved timestamp
);

INSERT INTO deletions.temp_documents_on_cases ( documentId, caseType, clientId, dateMoved)
SELECT d.id, c.casetype, p.id, now()
FROM documents d
INNER JOIN caseitem_document cd on d.id = cd.document_id
INNER JOIN cases c on c.id = cd.caseitem_id
INNER JOIN persons p on p.id = c.client_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = p.id;

INSERT INTO person_document ( person_id, document_id )
SELECT c.client_id, d.id
FROM documents d
INNER JOIN caseitem_document cd on d.id = cd.document_id
INNER JOIN cases c on c.id = cd.caseitem_id
INNER JOIN persons p on p.id = c.client_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = p.id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_complaints (id int);
INSERT INTO deletions.deletions_client_complaints (id)
SELECT co.id
FROM complaints co
INNER JOIN cases ca ON co.caseitem_id = ca.id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = ca.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_document_pages (id int);
INSERT INTO deletions.deletions_deputy_document_pages (id)
SELECT dpd.id
FROM document_pages dpd
INNER JOIN documents doc ON doc.id = dpd.document_id
INNER JOIN caseitem_document cd ON doc.id = cd.document_id
INNER JOIN cases c ON c.id = cd.caseitem_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_annual_report_logs (id int);
INSERT INTO deletions.deletions_client_annual_report_logs (id)
SELECT al.id
FROM annual_report_logs al
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = al.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_annual_report_logs (id int);
INSERT INTO deletions.deletions_deputy_annual_report_logs (id)
SELECT al.id
FROM annual_report_logs al
INNER JOIN cases c  ON c.id = al.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_hold_period (id int);
INSERT INTO deletions.deletions_client_hold_period (id)
SELECT hp.id
FROM hold_period hp
INNER JOIN investigation inv ON inv.id = hp.investigation_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = inv.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_hold_period (id int);
INSERT INTO deletions.deletions_deputy_hold_period (id)
SELECT hp.id
FROM hold_period hp
INNER JOIN investigation inv ON inv.id = hp.investigation_id
INNER JOIN persons dep ON dep.id = inv.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_investigation (id int);
INSERT INTO deletions.deletions_client_investigation (id)
SELECT inv.id
FROM investigation inv
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = inv.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_investigation (id int);
INSERT INTO deletions.deletions_deputy_investigation (id)
SELECT inv.id
FROM investigation inv
INNER JOIN persons dep ON dep.id = inv.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_phonenumbers (id int);
INSERT INTO deletions.deletions_client_phonenumbers (id)
SELECT pn.id
FROM phonenumbers pn
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = pn.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_phonenumbers (id int);
INSERT INTO deletions.deletions_deputy_phonenumbers (id)
SELECT pn.id
FROM phonenumbers pn
INNER JOIN persons dep ON dep.id = pn.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_addresses (id int);
INSERT INTO deletions.deletions_client_addresses (id)
SELECT ad.id
FROM addresses ad
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = ad.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_addresses (id int);
INSERT INTO deletions.deletions_deputy_addresses (id)
SELECT ad.id
FROM addresses ad
INNER JOIN persons dep ON dep.id = ad.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_validation_check (id int);
INSERT INTO deletions.deletions_validation_check (id)
SELECT vc.id
FROM validation_check vc
INNER JOIN cases c  ON c.id = vc.caseitem_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_warnings (id int);
INSERT INTO deletions.deletions_client_warnings (id)
SELECT wa.id
FROM warnings wa
INNER JOIN person_warning pw ON wa.id = pw.warning_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = pw.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_warnings (id int);
INSERT INTO deletions.deletions_deputy_warnings (id)
SELECT wa.id
FROM warnings wa
INNER JOIN person_warning pw ON wa.id = pw.warning_id
INNER JOIN persons dep ON dep.id = pw.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_tasks (id int);
INSERT INTO deletions.deletions_client_tasks (id)
SELECT t.id
FROM tasks t
INNER JOIN person_task pt ON t.id = pt.task_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = pt.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_tasks (id int);
INSERT INTO deletions.deletions_deputy_tasks (id)
SELECT t.id
FROM tasks t
INNER JOIN person_task pt ON t.id = pt.task_id
INNER JOIN persons dep ON dep.id = pt.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_documents (id int);
INSERT INTO deletions.deletions_deputy_documents (id)
SELECT d.id
FROM documents d
INNER JOIN caseitem_document cd ON d.id = cd.document_id
INNER JOIN cases c ON c.id = cd.caseitem_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_persons (id int);
INSERT INTO deletions.deletions_client_persons (id)
SELECT p.id
FROM persons p
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = p.id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_cases (id int);
INSERT INTO deletions.deletions_client_cases (id)
SELECT c.id
FROM cases c
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_visits (id int);
INSERT INTO deletions.deletions_client_visits (id)
SELECT v.id
FROM visits v
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = v.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_supervision_notes (id int);
INSERT INTO deletions.deletions_client_supervision_notes (id)
SELECT s.id
FROM supervision_notes s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_supervision_notes (id int);
INSERT INTO deletions.deletions_deputy_supervision_notes (id)
SELECT s.id
FROM supervision_notes s
INNER JOIN persons dep ON dep.id = s.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_powerofattorney_person (person_id int);
INSERT INTO deletions.deletions_client_powerofattorney_person (person_id)
SELECT s.person_id
FROM powerofattorney_person s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_powerofattorney_person (person_id int);
INSERT INTO deletions.deletions_deputy_powerofattorney_person (person_id)
SELECT s.person_id
FROM powerofattorney_person s
INNER JOIN persons dep ON dep.id = s.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_person_timeline (id int);
INSERT INTO deletions.deletions_client_person_timeline (id)
SELECT s.id
FROM person_timeline s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_person_timeline (id int);
INSERT INTO deletions.deletions_deputy_person_timeline (id)
SELECT s.id
FROM person_timeline s
INNER JOIN persons dep ON dep.id = s.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_person_caseitem (person_id int);
INSERT INTO deletions.deletions_client_person_caseitem (person_id)
SELECT s.person_id
FROM person_caseitem s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_bonds (id int);
INSERT INTO deletions.deletions_deputy_bonds (id)
SELECT bo.id
FROM bonds bo
INNER JOIN cases c  ON c.id = bo.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_death_notifications (id int);
INSERT INTO deletions.deletions_client_death_notifications (id)
SELECT s.id
FROM death_notifications s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_death_notifications (id int);
INSERT INTO deletions.deletions_deputy_death_notifications (id)
SELECT s.id
FROM death_notifications s
INNER JOIN persons dep ON dep.id = s.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_person (id int);
INSERT INTO deletions.deletions_deputy_person (id)
SELECT dep.id
FROM persons dep
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

UPDATE cases SET correspondent_id = NULL
WHERE id in (
    SELECT id FROM deletions.deletions_client_cases
);

UPDATE cases SET donor_id = NULL
WHERE id in (
    SELECT id FROM deletions.deletions_client_cases
);

DELETE FROM events
WHERE source_complaint_id in (
    SELECT id FROM deletions.deletions_client_complaints
);

DELETE FROM events
WHERE source_page_id in (
    SELECT id FROM deletions.deletions_deputy_document_pages
);

DELETE FROM events
WHERE source_annualreportlog_id in (
    SELECT id FROM deletions.deletions_client_annual_report_logs
);

DELETE FROM events
WHERE source_holdperiod_id in (
    SELECT id FROM deletions.deletions_client_hold_period
);

DELETE FROM events
WHERE source_holdperiod_id in (
    SELECT id FROM deletions.deletions_deputy_hold_period
);

DELETE FROM events
WHERE source_investigation_id in (
    SELECT id FROM deletions.deletions_client_investigation
);

DELETE FROM events
WHERE source_investigation_id in (
    SELECT id FROM deletions.deletions_deputy_investigation
);

DELETE FROM events
WHERE source_phonenumber_id in (
    SELECT id FROM deletions.deletions_client_phonenumbers
);

DELETE FROM events
WHERE source_phonenumber_id in (
    SELECT id FROM deletions.deletions_deputy_phonenumbers
);

DELETE FROM events
WHERE source_address_id in (
    SELECT id FROM deletions.deletions_client_addresses
);

DELETE FROM events
WHERE source_address_id in (
    SELECT id FROM deletions.deletions_deputy_addresses
);

DELETE FROM events
WHERE source_validationcheck_id in (
    SELECT id FROM deletions.deletions_validation_check
);

DELETE FROM events
WHERE source_warning_id in (
    SELECT id FROM deletions.deletions_client_warnings
);

DELETE FROM events
WHERE source_warning_id in (
    SELECT id FROM deletions.deletions_deputy_warnings
);

DELETE FROM events
WHERE source_task_id in (
    SELECT id FROM deletions.deletions_client_tasks
);

DELETE FROM events
WHERE source_task_id in (
    SELECT id FROM deletions.deletions_deputy_tasks
);

DELETE FROM events
WHERE source_document_id in (
    SELECT id FROM deletions.deletions_deputy_documents
);

DELETE FROM events
WHERE owning_donor_id in (
    SELECT id FROM deletions.deletions_client_persons
);

DELETE FROM events
WHERE owning_case_id in (
    SELECT id FROM deletions.deletions_client_cases
);

DELETE FROM complaints
WHERE id in (
    SELECT id FROM deletions.deletions_client_complaints
);

DELETE FROM document_pages
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_document_pages
);

DELETE FROM annual_report_logs
WHERE id in (
    SELECT id FROM deletions.deletions_client_annual_report_logs
);

DELETE FROM annual_report_logs
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_annual_report_logs
);

DELETE FROM hold_period
WHERE id in (
    SELECT id FROM deletions.deletions_client_hold_period
);

DELETE FROM hold_period
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_hold_period
);

DELETE FROM investigation
WHERE id in (
    SELECT id FROM deletions.deletions_client_investigation
);

DELETE FROM investigation
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_investigation
);

DELETE FROM phonenumbers
WHERE id in (
    SELECT id FROM deletions.deletions_client_phonenumbers
);

DELETE FROM phonenumbers
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_phonenumbers
);

DELETE FROM addresses
WHERE id in (
    SELECT id FROM deletions.deletions_client_addresses
);

DELETE FROM addresses
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_addresses
);

DELETE FROM validation_check
WHERE id in (
    SELECT id FROM deletions.deletions_validation_check
);

DELETE FROM warnings
WHERE id in (
    SELECT id FROM deletions.deletions_client_warnings
);

DELETE FROM warnings
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_warnings
);

DELETE FROM person_warning
WHERE warning_id in (
    SELECT id FROM deletions.deletions_client_warnings
);

DELETE FROM person_warning
WHERE warning_id in (
    SELECT id FROM deletions.deletions_deputy_warnings
);

DELETE FROM tasks
WHERE id in (
    SELECT id FROM deletions.deletions_client_tasks
);

DELETE FROM tasks
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_tasks
);

DELETE FROM person_task
WHERE task_id in (
    SELECT id FROM deletions.deletions_client_tasks
);

DELETE FROM person_task
WHERE task_id in (
    SELECT id FROM deletions.deletions_deputy_tasks
);

DELETE FROM supervision_notes
WHERE id in (
    SELECT id FROM deletions.deletions_client_supervision_notes
);

DELETE FROM supervision_notes
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_supervision_notes
);

DELETE FROM powerofattorney_person
WHERE person_id in (
    SELECT person_id FROM deletions.deletions_deputy_powerofattorney_person
);

DELETE FROM powerofattorney_person
WHERE person_id in (
    SELECT person_id FROM deletions.deletions_client_powerofattorney_person
);

DELETE FROM person_timeline
WHERE id in (
    SELECT id FROM deletions.deletions_client_person_timeline
);

DELETE FROM person_timeline
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_person_timeline
);

DELETE FROM person_caseitem
WHERE person_id in (
    SELECT person_id FROM deletions.deletions_client_person_caseitem
);

DELETE FROM bonds
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_bonds
);

DELETE FROM death_notifications
WHERE id in (
    SELECT id FROM deletions.deletions_client_death_notifications
);

DELETE FROM death_notifications
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_death_notifications
);

DELETE FROM addresses
WHERE id in (
    SELECT id FROM deletions.deletions_client_addresses
);

DELETE FROM addresses
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_addresses
);

DELETE FROM person_research_preferences
WHERE person_id in (
    SELECT id FROM deletions.deletions_deputy_person
);

DELETE FROM person_personreference
WHERE person_id in (
    SELECT id FROM deletions.deletions_deputy_person
);

UPDATE persons set feepayer_id = null
WHERE id in (
 SELECT id FROM deletions.base_clients_persons
);

DELETE FROM persons
WHERE id in (
    SELECT id FROM deletions.deletions_deputy_person
);

DELETE FROM order_deputy
WHERE deputy_id in (
    SELECT id FROM deletions.deletions_deputy_person
);

DELETE FROM cases
WHERE id in (
    SELECT id FROM deletions.deletions_client_cases
);
