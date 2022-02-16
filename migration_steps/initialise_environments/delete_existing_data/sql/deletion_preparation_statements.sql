DROP SCHEMA IF EXISTS deletions CASCADE;
CREATE SCHEMA deletions;

-- Create base clients table
CREATE TABLE IF NOT EXISTS deletions.base_clients_persons (id int, caserecnumber varchar);

-- Insert base clients
INSERT INTO deletions.base_clients_persons (id, caserecnumber)
SELECT distinct p.id, p.caserecnumber
FROM persons p
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE UNIQUE INDEX stub_person_id_idx ON deletions.base_clients_persons (id);

-- Create table for list of clients to keep
CREATE TABLE IF NOT EXISTS deletions.pilot_one_clients (id int);

-- Insert cp1 clients into table of cp1 clients to keep
INSERT INTO deletions.pilot_one_clients (id)
SELECT distinct p.id
FROM persons p
WHERE p.type = 'actor_client' and p.caseactorgroup = 'CLIENT-PILOT-ONE';

-- Create table for list of deputies to keep
CREATE TABLE IF NOT EXISTS deletions.pilot_one_deputies (id int);

-- Insert deputies attached to pilot one cases as deputies or feepayers
INSERT INTO deletions.pilot_one_deputies (id)
SELECT dep.id
FROM persons dep
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN persons p ON p.id = c.client_id
WHERE p.type = 'actor_client' and p.caseactorgroup = 'CLIENT-PILOT-ONE'
UNION
SELECT distinct p.feepayer_id
FROM persons p
WHERE p.type = 'actor_client' and p.caseactorgroup = 'CLIENT-PILOT-ONE';

CREATE UNIQUE INDEX stub_pilot_one_deputies_idx ON deletions.pilot_one_deputies (id);

--Create the document backup table
CREATE TABLE IF NOT EXISTS deletions.temp_documents_on_cases(
    documentId int,
    caseType VARCHAR(255),
    clientId int,
    dateMoved timestamp
);

-- Inserting into the document backup table
INSERT INTO deletions.temp_documents_on_cases (documentId, caseType, clientId, dateMoved)
SELECT d.id, c.casetype, p.id, now()
FROM documents d
INNER JOIN caseitem_document cd on d.id = cd.document_id
INNER JOIN cases c on c.id = cd.caseitem_id
INNER JOIN persons p on p.id = c.client_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = p.id;

-- Inserting the records from caseitem_document to the client person_document
INSERT INTO person_document (person_id, document_id)
SELECT c.client_id, d.id
FROM documents d
INNER JOIN caseitem_document cd on d.id = cd.document_id
INNER JOIN cases c on c.id = cd.caseitem_id
INNER JOIN persons p on p.id = c.client_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = p.id
LEFT JOIN person_document pd on pd.document_id = d.id and pd.person_id = c.client_id
WHERE pd.document_id is null;

-- Deleting from case documents
DELETE FROM caseitem_document where document_id in (
SELECT d.id
FROM documents d
INNER JOIN caseitem_document cd ON d.id = cd.document_id
INNER JOIN cases c ON c.id = cd.caseitem_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id);

-- Create delete from complaints linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_complaints (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_complaints (id, caserecnumber)
SELECT co.id, bcp.caserecnumber
FROM complaints co
INNER JOIN cases ca ON co.caseitem_id = ca.id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = ca.client_id;

-- Create delete from deputy documents linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_documents (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_documents (id, caserecnumber)
SELECT doc.id, bcp.caserecnumber
FROM documents doc
INNER JOIN person_document pd ON doc.id = pd.document_id
INNER JOIN persons dep ON dep.id = pd.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from deputy document pages linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_document_pages (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_document_pages (id, caserecnumber)
SELECT dpd.id, bcp.caserecnumber
FROM document_pages dpd
INNER JOIN documents doc ON doc.id = dpd.document_id
INNER JOIN caseitem_document cd ON doc.id = cd.document_id
INNER JOIN cases c ON c.id = cd.caseitem_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

-- Create delete from deputy document pages linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_annual_report_logs (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_annual_report_logs (id, caserecnumber)
SELECT al.id, bcp.caserecnumber
FROM annual_report_logs al
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = al.client_id;

-- Create delete from annual report logs linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_annual_report_logs (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_annual_report_logs (id, caserecnumber)
SELECT al.id, bcp.caserecnumber
FROM annual_report_logs al
INNER JOIN cases c  ON c.id = al.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

-- Create delete from client hold period linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_hold_period (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_hold_period (id, caserecnumber)
SELECT hp.id, bcp.caserecnumber
FROM hold_period hp
INNER JOIN investigation inv ON inv.id = hp.investigation_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = inv.person_id;

-- Create delete from deputy hold period linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_hold_period (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_hold_period (id, caserecnumber)
SELECT hp.id, bcp.caserecnumber
FROM hold_period hp
INNER JOIN investigation inv ON inv.id = hp.investigation_id
INNER JOIN persons dep ON dep.id = inv.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from client investigation linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_investigation (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_investigation (id, caserecnumber)
SELECT inv.id, bcp.caserecnumber
FROM investigation inv
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = inv.person_id;

-- Create delete from deputy investigation linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_investigation (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_investigation (id, caserecnumber)
SELECT inv.id, bcp.caserecnumber
FROM investigation inv
INNER JOIN persons dep ON dep.id = inv.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from client phone numbers linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_phonenumbers (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_phonenumbers (id, caserecnumber)
SELECT pn.id, bcp.caserecnumber
FROM phonenumbers pn
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = pn.person_id;

CREATE UNIQUE INDEX client_phone_number_id_idx ON deletions.deletions_client_phonenumbers (id);

-- Create delete from deputy phone numbers linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_phonenumbers (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_phonenumbers (id, caserecnumber)
SELECT pn.id, bcp.caserecnumber
FROM phonenumbers pn
INNER JOIN persons dep ON dep.id = pn.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

CREATE INDEX deputy_phone_number_id_idx ON deletions.deletions_deputy_phonenumbers (id);

-- Create delete from client addresses linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_addresses (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_addresses (id, caserecnumber)
SELECT ad.id, bcp.caserecnumber
FROM addresses ad
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = ad.person_id
WHERE ad.id NOT IN (
    SELECT a.id
    FROM addresses a
    INNER JOIN deletions.pilot_one_clients cp1
    ON cp1.id = a.person_id
);

-- Create delete from deputy addresses linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_addresses (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_addresses (id, caserecnumber)
SELECT ad.id, bcp.caserecnumber
FROM addresses ad
INNER JOIN persons dep ON dep.id = ad.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from validation check linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_validation_check (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_validation_check (id, caserecnumber)
SELECT vc.id, bcp.caserecnumber
FROM validation_check vc
INNER JOIN cases c  ON c.id = vc.caseitem_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

-- Create delete from client warnings linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_warnings (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_warnings (id, caserecnumber)
SELECT wa.id, bcp.caserecnumber
FROM warnings wa
INNER JOIN person_warning pw ON wa.id = pw.warning_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = pw.person_id;

-- Create delete from deputy warnings linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_warnings (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_warnings (id, caserecnumber)
SELECT wa.id, bcp.caserecnumber
FROM warnings wa
INNER JOIN person_warning pw ON wa.id = pw.warning_id
INNER JOIN persons dep ON dep.id = pw.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from client tasks linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_tasks (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_tasks (id, caserecnumber)
SELECT t.id, bcp.caserecnumber
FROM tasks t
INNER JOIN person_task pt ON t.id = pt.task_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = pt.person_id;

CREATE UNIQUE INDEX client_tasks_id_idx ON deletions.deletions_client_tasks (id);

-- Create delete from deputy tasks linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_tasks (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_tasks (id, caserecnumber)
SELECT t.id, bcp.caserecnumber
FROM tasks t
INNER JOIN person_task pt ON t.id = pt.task_id
INNER JOIN persons dep ON dep.id = pt.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

CREATE UNIQUE INDEX deputy_tasks_id_idx ON deletions.deletions_deputy_tasks (id);

-- Create delete from client caseitem tasks linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_case_tasks (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_case_tasks (id, caserecnumber)
SELECT t.id, bcp.caserecnumber
FROM tasks t
INNER JOIN caseitem_task ct ON t.id = ct.task_id
INNER JOIN cases c ON ct.caseitem_id = c.id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

CREATE UNIQUE INDEX case_tasks_id_idx ON deletions.deletions_case_tasks (id);

-- Create delete from deputy documents linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_documents (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_documents (id, caserecnumber)
SELECT d.id, bcp.caserecnumber
FROM documents d
INNER JOIN caseitem_document cd ON d.id = cd.document_id
INNER JOIN cases c ON c.id = cd.caseitem_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

-- Create delete from client persons linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_persons (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_persons (id, caserecnumber)
SELECT p.id, bcp.caserecnumber
FROM persons p
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = p.id;

-- Create delete from client cases linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_cases (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_cases (id, caserecnumber)
SELECT c.id, bcp.caserecnumber
FROM cases c
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

-- Create delete from client visits linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_visits (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_visits (id, caserecnumber)
SELECT v.id, bcp.caserecnumber
FROM visits v
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = v.client_id;

-- Create delete from client timeline_events
CREATE TABLE IF NOT EXISTS deletions.deletions_client_timeline_events (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_timeline_events (id, caserecnumber)
SELECT e.id, bcp.caserecnumber
FROM timeline_event e
INNER JOIN deletions.base_clients_persons bcp ON bcp.caserecnumber = e.event->'payload'->>'courtReference';

-- Create delete from client supervision notes linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_supervision_notes (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_supervision_notes (id, caserecnumber)
SELECT s.id, bcp.caserecnumber
FROM supervision_notes s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

-- Create delete from deputy supervision notes linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_supervision_notes (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_supervision_notes (id, caserecnumber)
SELECT s.id, bcp.caserecnumber
FROM supervision_notes s
INNER JOIN persons dep ON dep.id = s.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from client powerofattorney linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_powerofattorney_person (person_id int);
INSERT INTO deletions.deletions_client_powerofattorney_person (person_id)
SELECT s.person_id
FROM powerofattorney_person s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

-- Create delete from deputy powerofattorney linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_powerofattorney_person (person_id int);
INSERT INTO deletions.deletions_deputy_powerofattorney_person (person_id)
SELECT s.person_id
FROM powerofattorney_person s
INNER JOIN persons dep ON dep.id = s.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from client timeline to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_person_timeline (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_person_timeline (id, caserecnumber)
SELECT s.id, bcp.caserecnumber
FROM person_timeline s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

-- Create delete from deputy timeline linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_person_timeline (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_person_timeline (id, caserecnumber)
SELECT s.id, bcp.caserecnumber
FROM person_timeline s
INNER JOIN persons dep ON dep.id = s.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from client person caseitems linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_person_caseitem (person_id int);
INSERT INTO deletions.deletions_client_person_caseitem (person_id)
SELECT s.person_id
FROM person_caseitem s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

-- Create delete from deputy bonds linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_bonds (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_bonds (id, caserecnumber)
SELECT bo.id, bcp.caserecnumber
FROM bonds bo
INNER JOIN cases c  ON c.id = bo.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id;

-- Create delete from client death linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_client_death_notifications (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_client_death_notifications (id, caserecnumber)
SELECT s.id, bcp.caserecnumber
FROM death_notifications s
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = s.person_id;

-- Create delete from deputy death linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_death_notifications (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_death_notifications (id, caserecnumber)
SELECT s.id, bcp.caserecnumber
FROM death_notifications s
INNER JOIN persons dep ON dep.id = s.person_id
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

-- Create delete from deputy persons linked to stub cases
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_person (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_deputy_person (id, caserecnumber)
SELECT dep.id, bcp.caserecnumber
FROM persons dep
INNER JOIN order_deputy od ON dep.id = od.deputy_id
INNER JOIN cases c  ON c.id = od.order_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = c.client_id
WHERE dep.id NOT IN (SELECT id FROM deletions.pilot_one_deputies);

--INSERT INTO deletions.deletions.deletions_deputy_person (id, caserecnumber)
--SELECT DISTINCT dep.id, NULL
--FROM persons dep
--LEFT JOIN order_deputy od ON od.deputy_id = dep.id
--LEFT JOIN cases c ON c.id = od.order_id
--WHERE dep.type = 'actor_deputy'
--AND c.id IS NULL

-- Create finance invoice temp table to be used in count check (no delete statement for this)
CREATE TABLE IF NOT EXISTS deletions.deletions_finance_invoice (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_finance_invoice (id, caserecnumber)
SELECT fi.id, bcp.caserecnumber
FROM finance_invoice fi
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = fi.person_id;

-- Create finance ledger temp table to be used in count check (no delete statement for this)
CREATE TABLE IF NOT EXISTS deletions.deletions_finance_ledger (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_finance_ledger (id, caserecnumber)
SELECT fl.id, bcp.caserecnumber
FROM finance_ledger fl
INNER JOIN finance_person fp ON fp.id = fl.finance_person_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = fp.person_id;

-- Create finance ledger allocation temp table to be used in count check (no delete statement for this)
CREATE TABLE IF NOT EXISTS deletions.deletions_finance_ledger_allocation (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_finance_ledger_allocation (id, caserecnumber)
SELECT fla.id, bcp.caserecnumber
FROM finance_ledger_allocation fla
INNER JOIN finance_invoice fi ON fi.id = fla.invoice_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = fi.person_id;

-- Create finance remission temp table to be used in count check (no delete statement for this)
CREATE TABLE IF NOT EXISTS deletions.deletions_finance_remission_exemption (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_finance_remission_exemption (id, caserecnumber)
SELECT fre.id, bcp.caserecnumber
FROM finance_remission_exemption fre
INNER JOIN finance_person fp ON fp.id = fre.finance_person_id
INNER JOIN deletions.base_clients_persons bcp ON bcp.id = fp.person_id;

-- Create finance order temp table to be used in count check (no delete statement for this)
CREATE TABLE IF NOT EXISTS deletions.deletions_finance_order (id int, caserecnumber varchar);
INSERT INTO deletions.deletions_finance_order (id)
SELECT fo.id
FROM finance_order fo
INNER JOIN deletions.deletions_client_cases dcc ON dcc.id = fo.order_id;