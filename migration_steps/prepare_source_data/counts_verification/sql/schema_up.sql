CREATE SCHEMA IF NOT EXISTS countverification;

CREATE TABLE IF NOT EXISTS countverification.counts (
    supervision_table varchar(100)
);

INSERT INTO countverification.counts (supervision_table)
VALUES
('addresses'),
('annual_report_lodging_details'),
('annual_report_logs'),
('bonds'),
('cases'),
('death_notifications'),
('feepayer_id'),
('finance_allocation_credits'),
('finance_exemptions'),
('finance_invoice_ad'),
('finance_invoice_non_ad'),
('finance_ledger_credits'),
('finance_order'),
('finance_person'),
('finance_remissions'),
('order_deputy'),
('person_caseitem'),
('persons'),
('persons_clients'),
('persons_deputies'),
('person_task'),
('person_timeline'),
('person_warning'),
('phonenumbers'),
('supervision_level_log'),
('supervision_notes'),
('tasks'),
('timeline_event'),
('visits'),
('warnings');

CREATE SCHEMA IF NOT EXISTS countverificationaudit;