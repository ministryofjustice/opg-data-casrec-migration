DELETE FROM events e
USING deletions.deletions_client_complaints bcp bcp
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
