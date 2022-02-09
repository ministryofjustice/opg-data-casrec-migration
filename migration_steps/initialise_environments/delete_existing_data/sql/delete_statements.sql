UPDATE cases SET correspondent_id = NULL
WHERE id in (
    SELECT id FROM deletions.deletions_client_cases
);

UPDATE documents SET correspondent_id = NULL
WHERE correspondent_id in (
    SELECT id FROM deletions.deletions_deputy_person
);

UPDATE cases SET donor_id = NULL
WHERE id in (
    SELECT id FROM deletions.deletions_client_cases
);

UPDATE documents SET task_id = NULL
WHERE task_id in (
    select id FROM deletions.deletions_deputy_tasks
);

UPDATE documents SET task_id = NULL
WHERE task_id in (
    select id FROM deletions.deletions_client_tasks
);

UPDATE documents SET task_id = NULL
WHERE task_id in (
    select id FROM deletions.deletions_case_tasks
);

DELETE FROM complaints a
USING deletions.deletions_client_complaints b
WHERE a.id = b.id;

DELETE FROM document_pages a
USING deletions.deletions_deputy_document_pages b
WHERE a.id = b.id;

DELETE FROM supervision_notes a
USING deletions.deletions_client_supervision_notes b
WHERE a.id = b.id;

DELETE FROM supervision_notes a
USING deletions.deletions_deputy_supervision_notes b
WHERE a.id = b.id;

DELETE FROM hold_period a
USING deletions.deletions_client_hold_period b
WHERE a.id = b.id;

DELETE FROM hold_period a
USING deletions.deletions_deputy_hold_period b
WHERE a.id = b.id;

DELETE FROM investigation a
USING deletions.deletions_client_investigation b
WHERE a.id = b.id;

DELETE FROM investigation a
USING deletions.deletions_deputy_investigation b
WHERE a.id = b.id;

DELETE FROM phonenumbers a
USING deletions.deletions_client_phonenumbers b
WHERE a.id = b.id;

DELETE FROM phonenumbers a
USING deletions.deletions_deputy_phonenumbers b
WHERE a.id = b.id;

DELETE FROM addresses a
USING deletions.deletions_client_addresses b
WHERE a.id = b.id;

DELETE FROM addresses a
USING deletions.deletions_deputy_addresses b
WHERE a.id = b.id;

DELETE FROM validation_check a
USING deletions.deletions_validation_check b
WHERE a.id = b.id;

DELETE FROM warnings a
USING deletions.deletions_client_warnings b
WHERE a.id = b.id;

DELETE FROM warnings a
USING deletions.deletions_deputy_warnings b
WHERE a.id = b.id;

DELETE FROM person_warning a
USING deletions.deletions_client_warnings b
WHERE a.warning_id = b.id;

DELETE FROM person_warning a
USING deletions.deletions_deputy_warnings b
WHERE a.warning_id = b.id;

DELETE FROM annual_report_logs a
USING deletions.deletions_client_annual_report_logs b
WHERE a.id = b.id;

DELETE FROM annual_report_logs a
USING deletions.deletions_deputy_annual_report_logs b
WHERE a.id = b.id;

DELETE FROM tasks a
USING deletions.deletions_client_tasks b
WHERE a.id = b.id;

DELETE FROM tasks a
USING deletions.deletions_deputy_tasks b
WHERE a.id = b.id;

DELETE FROM tasks a
USING deletions.deletions_case_tasks b
WHERE a.id = b.id;

DELETE FROM person_task a
USING deletions.deletions_client_tasks b
WHERE a.task_id = b.id;

DELETE FROM person_task a
USING deletions.deletions_deputy_tasks b
WHERE a.task_id = b.id;

DELETE FROM visits v
USING deletions.deletions_client_visits b
WHERE v.id = b.id;

DELETE FROM powerofattorney_person a
USING deletions.deletions_deputy_powerofattorney_person b
WHERE a.person_id = b.person_id;

DELETE FROM powerofattorney_person a
USING deletions.deletions_client_powerofattorney_person b
WHERE a.person_id = b.person_id;

DELETE FROM person_timeline a
USING deletions.deletions_client_person_timeline b
WHERE a.id = b.id;

DELETE FROM person_timeline a
USING deletions.deletions_deputy_person_timeline b
WHERE a.id = b.id;

DELETE FROM timeline_event a
USING deletions.deletions_client_timeline_events b
WHERE a.id = b.id;

DELETE FROM person_caseitem a
USING deletions.deletions_client_person_caseitem b
WHERE a.person_id = b.person_id;

DELETE FROM bonds a
USING deletions.deletions_deputy_bonds b
WHERE a.id = b.id;

DELETE FROM death_notifications a
USING deletions.deletions_client_death_notifications b
WHERE a.id = b.id;

DELETE FROM death_notifications a
USING deletions.deletions_deputy_death_notifications b
WHERE a.id = b.id;

DELETE FROM addresses a
USING deletions.deletions_client_addresses b
WHERE a.id = b.id;

DELETE FROM addresses a
USING deletions.deletions_deputy_addresses b
WHERE a.id = b.id;

DELETE FROM person_research_preferences a
USING deletions.deletions_deputy_person b
WHERE a.person_id = b.id;

DELETE FROM person_personreference a
USING deletions.deletions_deputy_person b
WHERE a.person_id = b.id;

UPDATE persons p set feepayer_id = null
WHERE id in (
 SELECT id FROM deletions.base_clients_persons
);

UPDATE persons p set feepayer_id = null
WHERE id in (
 SELECT id FROM deletions.deletions_deputy_person
);

DELETE FROM persons a
USING deletions.deletions_deputy_person b
WHERE a.id = b.id;

DELETE FROM order_deputy a
USING deletions.deletions_deputy_person b
WHERE a.deputy_id = b.id;

DELETE FROM cases a
USING deletions.deletions_client_cases b
WHERE a.id = b.id;

DELETE FROM events e
USING deletions.deletions_client_complaints bcp
WHERE bcp.id = e.source_complaint_id;

DELETE FROM events e
USING deletions.deletions_deputy_document_pages bcp
WHERE bcp.id = e.source_page_id;

DELETE FROM events e
USING deletions.deletions_client_annual_report_logs bcp
WHERE bcp.id = e.source_annualreportlog_id;

DELETE FROM events e
USING deletions.deletions_client_hold_period bcp
WHERE bcp.id = e.source_holdperiod_id;

DELETE FROM events e
USING deletions.deletions_deputy_hold_period bcp
WHERE bcp.id = e.source_holdperiod_id;

DELETE FROM events e
USING deletions.deletions_client_investigation bcp
WHERE bcp.id = e.source_investigation_id;

DELETE FROM events e
USING deletions.deletions_deputy_investigation bcp
WHERE bcp.id = e.source_investigation_id;

DELETE FROM events e
USING deletions.deletions_client_phonenumbers bcp
WHERE bcp.id = e.source_phonenumber_id;

DELETE FROM events e
USING deletions.deletions_deputy_phonenumbers bcp
WHERE bcp.id = e.source_phonenumber_id;

DELETE FROM events e
USING deletions.deletions_client_addresses bcp
WHERE bcp.id = e.source_address_id;

DELETE FROM events e
USING deletions.deletions_deputy_addresses bcp
WHERE bcp.id = e.source_address_id;

DELETE FROM events e
USING deletions.deletions_validation_check bcp
WHERE bcp.id = e.source_validationcheck_id;

DELETE FROM events e
USING deletions.deletions_client_warnings bcp
WHERE bcp.id = e.source_warning_id;

DELETE FROM events e
USING deletions.deletions_deputy_warnings bcp
WHERE bcp.id = e.source_warning_id;

DELETE FROM events e
USING deletions.deletions_client_tasks bcp
WHERE bcp.id = e.source_task_id;

DELETE FROM events e
USING deletions.deletions_deputy_tasks bcp
WHERE bcp.id = e.source_task_id;

DELETE FROM events e
USING deletions.deletions_deputy_documents bcp
WHERE bcp.id = e.source_document_id;

DELETE FROM events e
USING deletions.deletions_client_persons bcp
WHERE bcp.id = e.owning_donor_id;

DELETE FROM events e
USING deletions.deletions_client_cases bcp
WHERE bcp.id = e.owning_case_id;
