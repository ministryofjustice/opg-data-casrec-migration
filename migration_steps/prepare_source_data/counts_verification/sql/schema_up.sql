CREATE SCHEMA IF NOT EXISTS {count_schema};

CREATE TABLE IF NOT EXISTS {count_schema}.counts (
    supervision_table varchar(100)
);

INSERT INTO {count_schema}.counts (supervision_table)
VALUES
('addresses'),
('annual_report_letter_status'),
('annual_report_lodging_details'),
('annual_report_logs'),
('annual_report_type_assignments'),
('assignee_teams'),
('assignees'),
('bonds'),
('case_timeline'),
('caseitem_document'),
('caseitem_note'),
('caseitem_paymenttype'),
('caseitem_queue'),
('caseitem_task'),
('caseitem_warning'),
('cases'),
('complaints'),
('death_notifications'),
('document_pages'),
('document_secondaryrecipient'),
('documents'),
('feepayer_id'),
('finance_allocation_credits'),
('finance_exemptions'),
('finance_invoice_ad'),
('finance_invoice_email_status'),
('finance_invoice_fee_range'),
('finance_invoice_non_ad'),
('finance_ledger_credits'),
('finance_order'),
('finance_person'),
('finance_remissions'),
('finance_report'),
('hold_period'),
('ingested_documents'),
('investigation'),
('notes'),
('opgcore_doctrine_migrations'),
('order_deputy'),
('pa_applicants'),
('pa_certificate_provider'),
('pa_notified_persons'),
('person_caseitem'),
('person_document'),
('person_note'),
('person_personreference'),
('person_references'),
('person_research_preferences'),
('person_task'),
('person_timeline'),
('person_warning'),
('persons_clients'),
('persons_deputies'),
('persons'),
('phonenumbers'),
('powerofattorney_person'),
('queue_business_rules'),
('scheduled_events'),
('supervision_level_log'),
('supervision_notes'),
('tasks'),
('timeline_event'),
('uploads'),
('validation_check'),
('visitor'),
('visits'),
('warnings'),
('total_documents'),
('deputy_person_document')
;

CREATE SCHEMA IF NOT EXISTS {count_audit_schema};
