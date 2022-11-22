-- addresses
INSERT INTO deleted_cases_sw6081.deleted_addresses (
    SELECT a.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN addresses a
        ON cl.id = a.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_addresses_audit (
    SELECT a.*
    FROM deleted_cases_sw6081.deleted_addresses da
    INNER JOIN addresses a
        ON da.id = a.id
    WHERE da.delete_run_id = :runId
);

-- annual_report_logs
INSERT INTO deleted_cases_sw6081.deleted_annual_report_logs (
    SELECT arl.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN annual_report_logs arl
        ON cl.id = arl.client_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_annual_report_logs_audit (
    SELECT arl.*
    FROM deleted_cases_sw6081.deleted_annual_report_logs darl
    INNER JOIN annual_report_logs arl
        ON arl.id = darl.id
    WHERE darl.delete_run_id = :runId
);

-- annual_report_letter_status
INSERT INTO deleted_cases_sw6081.deleted_annual_report_letter_status (
    SELECT arls.id, :runId
    FROM deleted_cases_sw6081.deleted_annual_report_logs arl
    INNER JOIN annual_report_letter_status arls
        ON arl.id = arls.annualreport_id
    WHERE arl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_annual_report_letter_status_audit (
    SELECT arls.*
    FROM deleted_cases_sw6081.deleted_annual_report_letter_status darls
    INNER JOIN annual_report_letter_status arls
        ON arls.id = darls.id
    WHERE darls.delete_run_id = :runId
);

-- annual_report_type_assignments
INSERT INTO deleted_cases_sw6081.deleted_annual_report_type_assignments (
    SELECT arta.id, :runId
    FROM deleted_cases_sw6081.deleted_annual_report_logs arl
    INNER JOIN annual_report_type_assignments arta
        ON arta.annualreport_id = arl.id
    WHERE arl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_annual_report_type_assignments_audit (
    SELECT arta.*
    FROM deleted_cases_sw6081.deleted_annual_report_type_assignments darta
    INNER JOIN annual_report_type_assignments arta
        ON darta.id = arta.id
    WHERE darta.delete_run_id = :runId
);

-- annual_report_lodging_details
INSERT INTO deleted_cases_sw6081.deleted_annual_report_lodging_details (
    SELECT arld.id, :runId
    FROM annual_report_lodging_details arld
    INNER JOIN deleted_cases_sw6081.deleted_annual_report_logs arl
        ON arld.annual_report_log_id = arl.id
    WHERE arl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_annual_report_lodging_details_audit (
    SELECT arld.*
    FROM deleted_cases_sw6081.deleted_annual_report_lodging_details darld
    INNER JOIN annual_report_lodging_details arld
        ON darld.id = arld.id
    WHERE darld.delete_run_id = :runId
);

-- death notifications
INSERT INTO deleted_cases_sw6081.deleted_death_notifications (
    SELECT dn.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN death_notifications dn
        ON cl.id = dn.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_death_notifications_audit (
    SELECT dn.*
    FROM deleted_cases_sw6081.deleted_death_notifications ddn
    INNER JOIN death_notifications dn
        ON dn.id = ddn.id
    WHERE ddn.delete_run_id = :runId
);

-- finance_person (supervision schema)
INSERT INTO deleted_cases_sw6081.deleted_finance_person (
    SELECT fp.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN supervision.finance_person fp
        ON cl.id = fp.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_finance_person_audit (
    SELECT fp.*
    FROM deleted_cases_sw6081.deleted_finance_person dfp
    INNER JOIN supervision.finance_person fp
        ON fp.id = dfp.id
    WHERE dfp.delete_run_id = :runId
);

-- finance_invoice (supervision schema)
INSERT INTO deleted_cases_sw6081.deleted_finance_invoice (
    SELECT fi.id, :runId
    FROM deleted_cases_sw6081.deleted_finance_person dfp
    INNER JOIN supervision.finance_invoice fi
        ON dfp.id = fi.finance_person_id
    WHERE dfp.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_finance_invoice_audit (
    SELECT fi.*
    FROM deleted_cases_sw6081.deleted_finance_invoice dfi
    INNER JOIN supervision.finance_invoice fi
        ON dfi.id = fi.id
    WHERE dfi.delete_run_id = :runId
);

-- finance_order (supervision schema)
INSERT INTO deleted_cases_sw6081.deleted_finance_order (
    SELECT fo.id, :runId
    FROM deleted_cases_sw6081.deleted_finance_person dfp
    INNER JOIN supervision.finance_order fo
        ON dfp.id = fo.finance_person_id
    WHERE dfp.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_finance_order_audit (
    SELECT fo.*
    FROM deleted_cases_sw6081.deleted_finance_order dfo
    INNER JOIN supervision.finance_order fo
        ON fo.id = dfo.id
    WHERE dfo.delete_run_id = :runId
);

-- finance_remission_exemption (supervision schema)
INSERT INTO deleted_cases_sw6081.deleted_finance_remission_exemption (
    SELECT fre.id, :runId
    FROM deleted_cases_sw6081.deleted_finance_person dfp
    INNER JOIN supervision.finance_remission_exemption fre
        ON dfp.id = fre.finance_person_id
    WHERE dfp.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_finance_remission_exemption_audit (
    SELECT fre.*
    FROM deleted_cases_sw6081.deleted_finance_remission_exemption dfre
    INNER JOIN supervision.finance_remission_exemption fre
        ON fre.id = dfre.id
    WHERE dfre.delete_run_id = :runId
);

-- finance_invoice_fee_range
INSERT INTO deleted_cases_sw6081.deleted_finance_invoice_fee_range (
    SELECT fifr.id, :runId
    FROM deleted_cases_sw6081.deleted_finance_invoice dfi
    INNER JOIN finance_invoice_fee_range fifr
        ON fifr.invoice_id = dfi.id
    WHERE dfi.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_finance_invoice_fee_range_audit (
    SELECT fifr.*
    FROM deleted_cases_sw6081.deleted_finance_invoice_fee_range dfifr
    LEFT JOIN finance_invoice_fee_range fifr
        ON fifr.id = dfifr.id
    WHERE dfifr.delete_run_id = :runId
);

-- finance_leger
INSERT INTO deleted_cases_sw6081.deleted_finance_ledger (
    SELECT fl.id, :runId
    FROM deleted_cases_sw6081.deleted_finance_person dfp
    INNER JOIN finance_ledger fl
        ON dfp.id = fl.finance_person_id
    WHERE dfp.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_finance_ledger_audit (
    SELECT fl.*
    FROM deleted_cases_sw6081.deleted_finance_ledger dfl
    INNER JOIN finance_ledger fl
        ON dfl.id = fl.id
    WHERE dfl.delete_run_id = :runId
);

-- finance_leger_allocation
INSERT INTO deleted_cases_sw6081.deleted_finance_ledger_allocation (
    SELECT fla.id, :runId
    FROM deleted_cases_sw6081.deleted_finance_ledger dfl
    INNER JOIN finance_ledger_allocation fla
        ON fla.ledger_entry_id = dfl.id
    WHERE dfl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_finance_ledger_allocation_audit (
    SELECT fla.*
    FROM deleted_cases_sw6081.deleted_finance_ledger_allocation dfla
    INNER JOIN finance_ledger_allocation fla
        ON fla.id = dfla.id
    WHERE dfla.delete_run_id = :runId
);

-- person_note
INSERT INTO deleted_cases_sw6081.deleted_person_note (
    SELECT pn.person_id, pn.note_id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN person_note pn
        ON cl.id = pn.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_person_note_audit (
    SELECT dpn.person_id, dpn.note_id
    FROM deleted_cases_sw6081.deleted_person_note dpn
    WHERE dpn.delete_run_id = :runId
);

-- notes
INSERT INTO deleted_cases_sw6081.deleted_notes (
    SELECT dpn.note_id, :runId
    FROM deleted_cases_sw6081.deleted_person_note dpn
    WHERE dpn.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_notes_audit (
    SELECT n.*
    FROM deleted_cases_sw6081.deleted_notes dn
    INNER JOIN notes n
        ON n.id = dn.id
    WHERE dn.delete_run_id = :runId
);

-- person_person_reference
INSERT INTO deleted_cases_sw6081.deleted_person_personreference (
    SELECT ppr.person_id, ppr.person_reference_id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN person_personreference ppr
        ON cl.id = ppr.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_person_personreference_audit (
    SELECT dppr.person_id, dppr.person_reference_id
    FROM deleted_cases_sw6081.deleted_person_personreference dppr
    WHERE dppr.delete_run_id = :runId
);

-- person_references
INSERT INTO deleted_cases_sw6081.deleted_person_references (
    SELECT pr.id, :runId
    FROM deleted_cases_sw6081.deleted_person_personreference dppr
    INNER JOIN person_references pr
        ON dppr.person_reference_id = pr.id
    WHERE dppr.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_person_references_audit (
    SELECT pr.*
    FROM deleted_cases_sw6081.deleted_person_references dpr
    INNER JOIN person_references pr
        ON dpr.id = pr.id
    WHERE dpr.delete_run_id = :runId
);

-- person_research_preferences
INSERT INTO deleted_cases_sw6081.deleted_person_research_preferences (
    SELECT prp.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN person_research_preferences prp
        ON cl.id = prp.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_person_research_preferences_audit (
    SELECT prp.*
    FROM deleted_cases_sw6081.deleted_person_research_preferences dprp
    INNER JOIN person_research_preferences prp
        ON dprp.id = prp.id
    WHERE dprp.delete_run_id = :runId
);

-- person_task
INSERT INTO deleted_cases_sw6081.deleted_person_task (
    SELECT pt.person_id, pt.task_id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN person_task pt
        ON cl.id = pt.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_person_task_audit (
    SELECT dpt.person_id, dpt.task_id
    FROM deleted_cases_sw6081.deleted_person_task dpt
    WHERE dpt.delete_run_id = :runId
);

-- tasks
INSERT INTO deleted_cases_sw6081.deleted_tasks (
    SELECT t.id, :runId
    FROM deleted_cases_sw6081.deleted_person_task dpt
    INNER JOIN tasks t
        ON dpt.task_id = t.id
    WHERE dpt.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_tasks_audit (
    SELECT t.*
    FROM deleted_cases_sw6081.deleted_tasks dt
    INNER JOIN tasks t
        ON t.id = dt.id
    WHERE dt.delete_run_id = :runId
);

-- person_timeline
INSERT INTO deleted_cases_sw6081.deleted_person_timeline (
    SELECT pt.id, pt.person_id, pt.timelineevent_id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN person_timeline pt
        ON cl.id = pt.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_person_timeline_audit (
    SELECT dpt.id, dpt.person_id, dpt.timelineevent_id
    FROM deleted_cases_sw6081.deleted_person_timeline dpt
    WHERE dpt.delete_run_id = :runId
);

-- timeline_event
INSERT INTO deleted_cases_sw6081.deleted_timeline_event (
    SELECT te.id, :runId
    FROM deleted_cases_sw6081.deleted_person_timeline dpt
    INNER JOIN timeline_event te
        ON dpt.timelineevent_id = te.id
    WHERE dpt.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_timeline_event_audit (
    SELECT te.*
    FROM deleted_cases_sw6081.deleted_timeline_event dte
    INNER JOIN timeline_event te
        ON te.id = dte.id
    WHERE dte.delete_run_id = :runId
);

-- person_warning
INSERT INTO deleted_cases_sw6081.deleted_person_warning (
    SELECT pw.person_id, pw.warning_id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN person_warning pw
        ON cl.id = pw.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_person_warning_audit (
    SELECT dpw.person_id, dpw.warning_id 
    FROM deleted_cases_sw6081.deleted_person_warning dpw
    WHERE dpw.delete_run_id = :runId
);

-- warnings
INSERT INTO deleted_cases_sw6081.deleted_warnings (
    SELECT w.id, :runId
    FROM deleted_cases_sw6081.deleted_person_warning dpw
    INNER JOIN warnings w
        ON dpw.warning_id = w.id
    WHERE dpw.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_warnings_audit (
    SELECT w.*
    FROM deleted_cases_sw6081.deleted_warnings dw
    INNER JOIN warnings w
        ON w.id = dw.id
    WHERE dw.delete_run_id = :runId
);

-- phonenumbers
INSERT INTO deleted_cases_sw6081.deleted_phonenumbers (
    SELECT ph.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN phonenumbers ph
        ON cl.id = ph.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_phonenumbers_audit (
    SELECT ph.*
    FROM deleted_cases_sw6081.deleted_phonenumbers dp
    INNER JOIN phonenumbers ph
        ON dp.id = ph.id
    WHERE dp.delete_run_id = :runId
);

-- supervision_notes
INSERT INTO deleted_cases_sw6081.deleted_supervision_notes (
    SELECT sn.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN supervision_notes sn
        ON cl.id = sn.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_supervision_notes_audit (
    SELECT sn.*
    FROM deleted_cases_sw6081.deleted_supervision_notes dsn
    INNER JOIN supervision_notes sn
        ON sn.id = dsn.id
    WHERE dsn.delete_run_id = :runId
);

-- visits
INSERT INTO deleted_cases_sw6081.deleted_visits (
    SELECT v.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN visits v
        ON cl.id = v.client_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_visits_audit (
    SELECT v.*
    FROM deleted_cases_sw6081.deleted_visits dv
    INNER JOIN visits v
        ON v.id = dv.id
    WHERE dv.delete_run_id = :runId
);

-- should obviously be 0, unless something has gone very wrong
-- cases
INSERT INTO deleted_cases_sw6081.deleted_cases (
    SELECT c.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN cases c
        ON cl.id = c.client_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_cases_audit (
    SELECT c.*
    FROM deleted_cases_sw6081.deleted_cases dc
    INNER JOIN cases c
        ON c.id = dc.id
    WHERE dc.delete_run_id = :runId
);

-- person_document
INSERT INTO deleted_cases_sw6081.deleted_person_document (
    SELECT pd.person_id, pd.document_id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN person_document pd
        ON cl.id = pd.person_id
    WHERE cl.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_person_document_audit (
    SELECT dpd.person_id, dpd.document_id
    FROM deleted_cases_sw6081.deleted_person_document dpd
    WHERE dpd.delete_run_id = :runId
);

-- document_pages
INSERT INTO deleted_cases_sw6081.deleted_document_pages (
    SELECT dp.id, dp.document_id, :runId
    FROM deleted_cases_sw6081.deleted_person_document dpd
    INNER JOIN document_pages dp
        ON dpd.document_id = dp.document_id
    WHERE dpd.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_document_pages_audit (
    SELECT dp.*
    FROM deleted_cases_sw6081.deleted_document_pages ddp
    INNER JOIN document_pages dp
        ON dp.id = ddp.id
    WHERE ddp.delete_run_id = :runId
);

-- document_secondaryrecipient
INSERT INTO deleted_cases_sw6081.deleted_document_secondaryrecipient (
    SELECT dsr.document_id, dsr.person_id, :runId
    FROM deleted_cases_sw6081.deleted_person_document dpd
    INNER JOIN document_secondaryrecipient dsr
        ON dsr.document_id = dpd.document_id
    WHERE dpd.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_document_secondaryrecipient_audit (
    SELECT ddsr.document_id, ddsr.person_id
    FROM deleted_cases_sw6081.deleted_document_secondaryrecipient ddsr
    WHERE ddsr.delete_run_id = :runId
);

-- documents
INSERT INTO deleted_cases_sw6081.deleted_documents (
    SELECT d.id, :runId
    FROM deleted_cases_sw6081.deleted_person_document dpd
    INNER JOIN documents d
        ON d.id = dpd.document_id
    WHERE dpd.delete_run_id = :runId
);

INSERT INTO deleted_cases_sw6081.deleted_documents_audit (
    SELECT d.*
    FROM deleted_cases_sw6081.deleted_documents dd
    INNER JOIN documents d
        ON d.id = dd.id
    WHERE dd.delete_run_id = :runId
);

-- persons (contacts)
INSERT INTO deleted_cases_sw6081.deleted_persons_contacts (
    SELECT p.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN persons p
        ON cl.id = p.client_id
    WHERE cl.delete_run_id = :runId
    AND p.type = 'actor_contact'
);

INSERT INTO deleted_cases_sw6081.deleted_persons_contacts_audit (
    SELECT p.*
    FROM deleted_cases_sw6081.deleted_persons_contacts dpc
    INNER JOIN persons p
        ON dpc.id = p.id
    WHERE dpc.delete_run_id = :runId
);

-- persons (deputies)
INSERT INTO deleted_cases_sw6081.deleted_persons_deputies (
    SELECT p.id, :runId
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN persons p
        ON cl.id = p.id
    WHERE cl.delete_run_id = :runId
    AND p.type = 'actor_deputy'
);

INSERT INTO deleted_cases_sw6081.deleted_persons_deputies_audit (
    SELECT p.*
    FROM deleted_cases_sw6081.deleted_persons_deputies dpd
    INNER JOIN persons p
        ON dpd.id = p.id
    WHERE dpd.delete_run_id = :runId
);

-- persons (clients)
INSERT INTO deleted_cases_sw6081.deleted_persons_clients_audit (
    SELECT p.*
    FROM deleted_cases_sw6081.run_clients cl
    INNER JOIN persons p
        ON cl.id = p.id
    WHERE cl.delete_run_id = :runId
    AND p.type = 'actor_client'
);

-- ================================================
-- 3. Add affected rows for each entity to results
-- ================================================

\set runColumnName run_:runId

ALTER TABLE deleted_cases_sw6081.results ADD :runColumnName int;

UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_addresses WHERE delete_run_id = :runId) WHERE delete_table = 'addresses';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_annual_report_logs WHERE delete_run_id = :runId) WHERE delete_table = 'annual_report_logs';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_annual_report_letter_status WHERE delete_run_id = :runId) WHERE delete_table = 'annual_report_letter_status';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_annual_report_type_assignments WHERE delete_run_id = :runId) WHERE delete_table = 'annual_report_type_assignments';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_annual_report_lodging_details WHERE delete_run_id = :runId) WHERE delete_table = 'annual_report_lodging_details';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_death_notifications WHERE delete_run_id = :runId) WHERE delete_table = 'death_notifications';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_finance_person WHERE delete_run_id = :runId) WHERE delete_table = 'finance_person';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_finance_invoice WHERE delete_run_id = :runId) WHERE delete_table = 'finance_invoice';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_finance_order WHERE delete_run_id = :runId) WHERE delete_table = 'finance_order';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_finance_remission_exemption WHERE delete_run_id = :runId) WHERE delete_table = 'finance_remission_exemption';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_finance_invoice_fee_range WHERE delete_run_id = :runId) WHERE delete_table = 'finance_invoice_fee_range';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_finance_ledger WHERE delete_run_id = :runId) WHERE delete_table = 'finance_ledger';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_finance_ledger_allocation WHERE delete_run_id = :runId) WHERE delete_table = 'finance_ledger_allocation';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_person_note WHERE delete_run_id = :runId) WHERE delete_table = 'person_note';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_notes WHERE delete_run_id = :runId) WHERE delete_table = 'notes';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_person_personreference WHERE delete_run_id = :runId) WHERE delete_table = 'person_personreference';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_person_references WHERE delete_run_id = :runId) WHERE delete_table = 'person_references';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_person_research_preferences WHERE delete_run_id = :runId) WHERE delete_table = 'person_research_preferences';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_person_task WHERE delete_run_id = :runId) WHERE delete_table = 'person_task';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_tasks WHERE delete_run_id = :runId) WHERE delete_table = 'tasks';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_person_timeline WHERE delete_run_id = :runId) WHERE delete_table = 'person_timeline';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_timeline_event WHERE delete_run_id = :runId) WHERE delete_table = 'timeline_event';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_person_warning WHERE delete_run_id = :runId) WHERE delete_table = 'person_warning';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_warnings WHERE delete_run_id = :runId) WHERE delete_table = 'warnings';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_phonenumbers WHERE delete_run_id = :runId) WHERE delete_table = 'phonenumbers';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_supervision_notes WHERE delete_run_id = :runId) WHERE delete_table = 'supervision_notes';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_visits WHERE delete_run_id = :runId) WHERE delete_table = 'visits';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_cases WHERE delete_run_id = :runId) WHERE delete_table = 'cases';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_person_document WHERE delete_run_id = :runId) WHERE delete_table = 'person_document';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_document_pages WHERE delete_run_id = :runId) WHERE delete_table = 'document_pages';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_document_secondaryrecipient WHERE delete_run_id = :runId) WHERE delete_table = 'document_secondaryrecipient';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_documents WHERE delete_run_id = :runId) WHERE delete_table = 'documents';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_persons_contacts WHERE delete_run_id = :runId) WHERE delete_table = 'persons_contacts';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.deleted_persons_deputies WHERE delete_run_id = :runId) WHERE delete_table = 'persons_deputies';
UPDATE deleted_cases_sw6081.results SET :runColumnName = (SELECT COUNT(1) FROM deleted_cases_sw6081.run_clients WHERE delete_run_id = :runId) WHERE delete_table = 'persons_clients_audit';