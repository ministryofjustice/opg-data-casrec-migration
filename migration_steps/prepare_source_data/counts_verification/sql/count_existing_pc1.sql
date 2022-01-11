DROP SCHEMA IF EXISTS countverification CASCADE;
CREATE SCHEMA countverification;

CREATE TABLE IF NOT EXISTS countverification.cp1_clients (id int);
INSERT INTO countverification.cp1_clients (id)
SELECT id FROM persons p
WHERE p.type = 'actor_client'
  AND p.caseactorgroup = 'CLIENT-PILOT-ONE'
  AND p.clientsource != 'CASRECMIGRATION';
CREATE UNIQUE INDEX cp1_clients_idx ON countverification.cp1_clients (id);

CREATE TABLE IF NOT EXISTS countverification.cp1_cases (id int);
INSERT INTO countverification.cp1_cases (id)
SELECT cases.id FROM countverification.cp1_clients INNER JOIN cases ON cases.client_id = cp1_clients.id;
CREATE UNIQUE INDEX cp1_cases_idx ON countverification.cp1_cases (id);

CREATE TABLE IF NOT EXISTS countverification.cp1_deputies (id int);
INSERT INTO countverification.cp1_deputies (id)
SELECT DISTINCT dep.id
FROM countverification.cp1_cases
    INNER JOIN order_deputy od ON od.order_id = cp1_cases.id
    INNER JOIN persons dep ON dep.id = od.deputy_id;
CREATE UNIQUE INDEX cp1_deputies_idx ON countverification.cp1_deputies (id);

CREATE TABLE IF NOT EXISTS countverification.counts (
    supervision_table varchar(100),
    cp1existing int
);

-- persons
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'persons' AS supervision_table,
(
    SELECT COUNT(*) FROM countverification.cp1_clients
)+(
    SELECT COUNT(*) FROM countverification.cp1_deputies
) AS cp1existing;

-- cases
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'cases' AS supervision_table, COUNT(*) AS cp1existing
FROM countverification.cp1_cases;

-- phonenumbers
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'phonenumbers' AS supervision_table,
(
    -- client
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.cp1_clients cli ON cli.id = pn.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.cp1_deputies dep ON dep.id = pn.person_id
) AS cp1existing;

-- addresses
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'addresses' AS supervision_table,
(
    -- client
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.cp1_clients cli ON cli.id = ad.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.cp1_deputies dep ON dep.id = ad.person_id
) AS cp1existing;

-- supervision_notes
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'supervision_notes' AS supervision_table,
(
    SELECT COUNT(*)
    FROM supervision_notes sn
    INNER JOIN countverification.cp1_clients cli ON cli.id = sn.person_id
)+(
    SELECT COUNT(*)
    FROM supervision_notes sn
    INNER JOIN countverification.cp1_deputies dep ON dep.id = sn.person_id
) AS cp1existing;

-- tasks
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'tasks' AS supervision_table,
(
    SELECT COUNT(*)
    FROM tasks t
    INNER JOIN person_task pt ON pt.task_id = t.id
    INNER JOIN countverification.cp1_clients cli on cli.id = pt.person_id
) AS cp1existing;

-- death_notifications
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'death_notifications' AS supervision_table,
(
    -- client
    SELECT COUNT(*)
    FROM death_notifications dn
    INNER JOIN countverification.cp1_clients cli on cli.id = dn.person_id
)+(
    -- dpeuty
    SELECT COUNT(*)
    FROM death_notifications dn
    INNER JOIN countverification.cp1_deputies dep on dep.id = dn.person_id
) AS cp1existing;

-- warnings
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'warnings' AS supervision_table,
(
    --client
    SELECT COUNT(*)
    FROM warnings w
    INNER JOIN person_warning pw on pw.warning_id = w.id
    INNER JOIN countverification.cp1_clients cli on cli.id = pw.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM warnings w
    INNER JOIN person_warning pw on pw.warning_id = w.id
    INNER JOIN countverification.cp1_deputies dep on dep.id = pw.person_id
) AS cp1existing;

-- annual_report_logs
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'annual_report_logs' AS supervision_table,
(
    -- client
    SELECT COUNT(*)
    FROM annual_report_logs al
    INNER JOIN countverification.cp1_clients cli ON cli.id = al.client_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM annual_report_logs al
    INNER JOIN countverification.cp1_cases ON cp1_cases.id = al.order_id
) AS cp1existing;

-- visits
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'visits' AS supervision_table, COUNT(*) AS cp1existing
FROM visits v
INNER JOIN countverification.cp1_clients cli ON cli.id = v.client_id;

-- bonds
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'bonds' AS supervision_table, COUNT(*) AS cp1existing
FROM bonds bon
INNER JOIN countverification.cp1_cases ON cp1_cases.id = bon.order_id;

-- feepayer_id
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'feepayer_id' AS supervision_table, COUNT(*) AS cp1existing
FROM persons p
INNER JOIN countverification.cp1_clients cli ON cli.id = p.id
WHERE p.feepayer_id IS NOT NULL;

-- timeline_event
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'timeline_event' AS supervision_table,
(
    -- client
    SELECT COUNT(*)
    FROM timeline_event te
    INNER JOIN person_timeline pt on pt.timelineevent_id = te.id
    INNER JOIN countverification.cp1_clients cli on cli.id = pt.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM timeline_event te
    INNER JOIN person_timeline pt on pt.timelineevent_id = te.id
    INNER JOIN countverification.cp1_deputies dep on dep.id = pt.person_id
) AS cp1existing;

-- supervision_level_log
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'supervision_level_log' AS supervision_table, COUNT(*) AS cp1existing
FROM supervision_level_log sll
INNER JOIN countverification.cp1_cases ON cp1_cases.id = sll.order_id;

-- finance_invoice_ad
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'finance_invoice_ad' AS supervision_table, COUNT(*) AS cp1existing
FROM finance_invoice inv
INNER JOIN countverification.cp1_clients cli on cli.id = inv.person_id
WHERE inv.source = 'CASRECMIGRATION'
AND inv.feetype <> 'AD';

-- finance_invoice_non_ad
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'finance_invoice_non_ad' AS supervision_table, COUNT(*) AS cp1existing
FROM finance_invoice inv
INNER JOIN countverification.cp1_clients cli on cli.id = inv.person_id
WHERE inv.source = 'CASRECMIGRATION'
AND inv.feetype = 'AD';

-- finance_remissions
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'finance_remissions' AS supervision_table, COUNT(*) AS cp1existing
FROM finance_remission_exemption rem
LEFT JOIN finance_person fp ON fp.id = rem.finance_person_id
INNER JOIN countverification.cp1_clients cli on cli.id = fp.person_id
WHERE rem.discounttype = 'REMISSION';

-- finance_exemptions
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'finance_exemptions' AS supervision_table, COUNT(*) AS cp1existing
FROM finance_remission_exemption rem
LEFT JOIN finance_person fp ON fp.id = rem.finance_person_id
INNER JOIN countverification.cp1_clients cli on cli.id = fp.person_id
WHERE rem.discounttype = 'EXEMPTION';

-- finance_ledger_credits
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'finance_ledger_credits' AS supervision_table, COUNT(*)
FROM finance_ledger lgr
LEFT JOIN finance_person fp ON fp.id = lgr.finance_person_id
INNER JOIN countverification.cp1_clients cli on cli.id = fp.person_id;

-- finance_allocation_credits
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'finance_allocation_credits' AS supervision_table, COUNT(*)
FROM finance_ledger_allocation fla
LEFT JOIN finance_invoice inv ON inv.id = fla.invoice_id
INNER JOIN countverification.cp1_clients cli on cli.id = inv.person_id;

-- order_deputy
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'order_deputy' AS supervision_table, COUNT(*) AS cp1existing
FROM order_deputy od
INNER JOIN countverification.cp1_cases ON cp1_cases.id = od.order_id;

-- person_caseitem
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'person_caseitem' AS supervision_table, COUNT(*) AS cp1existing
FROM person_caseitem pci
INNER JOIN countverification.cp1_clients cli on cli.id = pci.person_id;

-- person_warning
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'person_warning' AS supervision_table,
(
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.cp1_clients cli on cli.id = pw.person_id
)+(
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.cp1_deputies dep on dep.id = pw.person_id
) AS cp1existing;

-- person_task
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'person_task' AS supervision_table,
(
    -- client
    SELECT COUNT(*)
    FROM person_task pt
    INNER JOIN countverification.cp1_clients cli on cli.id = pt.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM person_task pt
    INNER JOIN countverification.cp1_deputies dep on dep.id = pt.person_id
) AS cp1existing;

-- person_timeline
INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'person_timeline' AS supervision_table,
(
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN countverification.cp1_clients cli on cli.id = pt.person_id
)+(
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN countverification.cp1_deputies dep on dep.id = pt.person_id
) AS cp1existing;

DROP INDEX countverification.cp1_clients_idx;
DROP INDEX countverification.cp1_cases_idx;
DROP INDEX countverification.cp1_deputies_idx;

DROP TABLE countverification.cp1_clients;
DROP TABLE countverification.cp1_cases;
DROP TABLE countverification.cp1_deputies;
