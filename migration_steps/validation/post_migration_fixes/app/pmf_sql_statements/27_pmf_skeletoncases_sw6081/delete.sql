-- addresses
DELETE FROM addresses a
USING deleted_cases_sw6081.deleted_addresses da
WHERE a.id = da.id
AND da.delete_run_id = :runId;

-- annual_report_logs
DELETE FROM annual_report_logs arl
USING deleted_cases_sw6081.deleted_annual_report_logs darl
WHERE darl.id = arl.id
AND darl.delete_run_id = :runId;

-- DELETE FROM
-- annual_report_letter_status
-- deleted_cases_sw6081.deleted_annual_report_letter_status deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- DELETE FROM
-- annual_report_type_assignments
-- deleted_cases_sw6081.deleted_annual_report_type_assignments deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- annual_report_lodging_details
DELETE FROM annual_report_lodging_details arld
USING deleted_cases_sw6081.deleted_annual_report_lodging_details darld
WHERE darld.id = arld.id
AND darld.delete_run_id = :runId;

-- death_notifications
DELETE FROM death_notifications dn
USING deleted_cases_sw6081.deleted_death_notifications ddn
WHERE ddn.id = dn.id
AND ddn.delete_run_id = :runId;

-- finance_invoice
DELETE FROM supervision.finance_invoice fi
USING deleted_cases_sw6081.deleted_finance_invoice dfi
WHERE dfi.id = fi.id
AND dfi.delete_run_id = :runId;

-- DELETE FROM
-- finance_order
-- deleted_cases_sw6081.deleted_finance_order deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- DELETE FROM
-- finance_remission_exemption
-- deleted_cases_sw6081.deleted_finance_remission_exemption deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- DELETE FROM
-- finance_invoice_fee_range
-- deleted_cases_sw6081.deleted_finance_invoice_fee_range deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- DELETE FROM
-- finance_ledger
-- deleted_cases_sw6081.deleted_finance_ledger deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- DELETE FROM
-- finance_ledger_allocation
-- deleted_cases_sw6081.deleted_finance_ledger_allocation deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- finance_person
DELETE FROM supervision.finance_person fp
USING deleted_cases_sw6081.deleted_finance_person dfp
WHERE dfp.id = fp.id
AND dfp.delete_run_id = :runId;

-- person_note
DELETE FROM person_note pn
USING deleted_cases_sw6081.deleted_person_note dpn
WHERE dpn.person_id = pn.person_id
AND dpn.note_id = pn.note_id
AND dpn.delete_run_id = :runId;

-- notes
DELETE FROM notes
USING
deleted_cases_sw6081.deleted_notes dn
WHERE dn.id = notes.id
AND dn.delete_run_id = :runId;

-- DELETE FROM
-- person_personreference
-- deleted_cases_sw6081.deleted_person_personreference deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- DELETE FROM
-- person_references
-- deleted_cases_sw6081.deleted_person_references deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- DELETE FROM
-- person_research_preferences
-- deleted_cases_sw6081.deleted_person_research_preferences deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- person_task
DELETE FROM person_task pt
USING deleted_cases_sw6081.deleted_person_task dpt
WHERE dpt.person_id = pt.person_id
AND dpt.task_id = pt.task_id
AND dpt.delete_run_id = :runId;

-- tasks
DELETE FROM tasks t
USING deleted_cases_sw6081.deleted_tasks dt
WHERE dt.id = t.id
AND dt.delete_run_id = :runId;

-- person_timeline
DELETE FROM person_timeline pt
USING deleted_cases_sw6081.deleted_person_timeline dpt
WHERE dpt.id = pt.id
AND dpt.delete_run_id = :runId;

-- timeline_event
DELETE FROM timeline_event te
USING deleted_cases_sw6081.deleted_timeline_event dte
WHERE dte.id = te.id
AND dte.delete_run_id = :runId;

-- person_warning
DELETE FROM person_warning pw
USING deleted_cases_sw6081.deleted_person_warning dpw
WHERE dpw.person_id = pw.person_id
AND dpw.warning_id = pw.warning_id
AND dpw.delete_run_id = :runId;

-- warnings
DELETE FROM warnings w
USING deleted_cases_sw6081.deleted_warnings dw
WHERE dw.id = w.id
AND dw.delete_run_id = :runId;

-- phonenumbers
DELETE FROM phonenumbers pn
USING deleted_cases_sw6081.deleted_phonenumbers dpn
WHERE dpn.id = pn.id
AND dpn.delete_run_id = :runId;

-- supervision_notes
DELETE FROM supervision_notes sn
USING deleted_cases_sw6081.deleted_supervision_notes dsn
WHERE dsn.id = sn.id
AND dsn.delete_run_id = :runId;

DELETE FROM visits v
USING deleted_cases_sw6081.deleted_visits dv
WHERE dv.id = v.id
AND dv.delete_run_id = :runId;

-- DELETE FROM
-- cases
-- deleted_cases_sw6081.deleted_cases deletetable
-- WHERE delete_table.delete_run_id = :runId;

DELETE FROM person_document pd
USING deleted_cases_sw6081.deleted_person_document dpd
WHERE dpd.person_id = pd.person_id
AND dpd.document_id = pd.document_id
AND dpd.delete_run_id = :runId;

-- document_pages
DELETE FROM document_pages dp
USING deleted_cases_sw6081.deleted_document_pages ddp
WHERE ddp.id = dp.id
AND ddp.delete_run_id = :runId;

-- DELETE FROM
-- document_secondaryrecipient
-- deleted_cases_sw6081.deleted_document_secondaryrecipient deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- persons_contacts
-- 1. remove links to contacts from within persons table
UPDATE persons p SET executor_id = NULL
WHERE p.id IN (
    SELECT dpca.client_id
    FROM deleted_cases_sw6081.deleted_persons_contacts dpc
    INNER JOIN deleted_cases_sw6081.deleted_persons_contacts_audit dpca
        ON dpca.id = dpc.id
    WHERE dpc.delete_run_id = :runId
)
AND p.type='actor_client';

DELETE FROM persons p
USING deleted_cases_sw6081.deleted_persons_contacts dpc
WHERE dpc.id = p.id
AND dpc.delete_run_id = :runId
AND p.type='actor_contact';

-- persons_deputies
-- DELETE FROM
-- persons_deputies
-- deleted_cases_sw6081.deleted_persons_deputies deletetable
-- WHERE delete_table.delete_run_id = :runId;

-- persons_clients
DELETE FROM persons p
USING deleted_cases_sw6081.run_clients rc
WHERE rc.id = p.id
AND rc.delete_run_id = :runId;