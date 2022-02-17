ALTER TABLE countverification.counts DROP COLUMN IF EXISTS {working_column};
ALTER TABLE countverification.counts ADD COLUMN {working_column} int;

DROP TABLE IF EXISTS countverification.non_cp1_clients;
CREATE TABLE IF NOT EXISTS countverification.non_cp1_clients (id int, caserecnumber varchar);
INSERT INTO countverification.non_cp1_clients (id, caserecnumber) (
    SELECT p.id, p.caserecnumber FROM persons p
    WHERE p.type = 'actor_client'
      AND (COALESCE(caseactorgroup, '') != 'CLIENT-PILOT-ONE')
);
CREATE UNIQUE INDEX non_cp1_clients_idx ON countverification.non_cp1_clients (id);

DROP TABLE IF EXISTS countverification.non_cp1_cases;
CREATE TABLE IF NOT EXISTS countverification.non_cp1_cases (id int, caserecnumber varchar);
INSERT INTO countverification.non_cp1_cases (id, caserecnumber) (
    SELECT DISTINCT cases.id, non_cp1_clients.caserecnumber
    FROM cases
    INNER JOIN countverification.non_cp1_clients ON cases.client_id = non_cp1_clients.id
);
CREATE UNIQUE INDEX non_cp1_cases_idx ON countverification.non_cp1_cases (id);

-- Cant include caserecnumbers here as not 1 to 1 relation
DROP TABLE IF EXISTS countverification.non_cp1_deputies;
CREATE TABLE IF NOT EXISTS countverification.non_cp1_deputies (id int);
-- regular
INSERT INTO countverification.non_cp1_deputies (id) (
    SELECT DISTINCT dep.id
    FROM countverification.non_cp1_cases c
    INNER JOIN order_deputy od ON od.order_id = c.id
    INNER JOIN persons dep ON dep.id = od.deputy_id
    WHERE dep.type = 'actor_deputy'
);
-- deputies with no entry in order_deputy or case
INSERT INTO countverification.non_cp1_deputies (id) (
    SELECT DISTINCT dep.id
    FROM persons dep
    LEFT JOIN order_deputy od ON od.deputy_id = dep.id
    LEFT JOIN cases c ON c.id = od.order_id
    LEFT JOIN persons p ON p.id = c.client_id
    WHERE dep.type = 'actor_deputy'
    AND c.id IS NULL
);
CREATE UNIQUE INDEX non_cp1_deputies_idx ON countverification.non_cp1_deputies (id);

-- persons_clients
DROP TABLE IF EXISTS countverificationaudit.{working_column}_persons_clients;
SELECT id, caserecnumber INTO countverificationaudit.{working_column}_persons_clients FROM countverification.non_cp1_clients;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_persons_clients
)
WHERE supervision_table = 'persons_clients';

-- persons_deputies
DROP TABLE IF EXISTS countverificationaudit.{working_column}_persons_deputies;
SELECT id, caserecnumber INTO countverificationaudit.{working_column}_persons_deputies
FROM (
    SELECT dep.id, c.caserecnumber
    FROM countverification.non_cp1_cases c
    INNER JOIN order_deputy od ON od.order_id = c.id
    INNER JOIN persons dep ON dep.id = od.deputy_id
    WHERE dep.type = 'actor_deputy'
    UNION
    SELECT p.id, cast(p.id as varchar)
    FROM persons p
    LEFT JOIN order_deputy od on p.id = od.deputy_id
    LEFT JOIN cases c on c.id = od.order_id
    WHERE p.type = 'actor_deputy'
    AND c.id IS NULL
) as a;
UPDATE countverification.counts SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_persons_deputies
)
WHERE supervision_table = 'persons_deputies';

-- cases
DROP TABLE IF EXISTS countverificationaudit.{working_column}_cases;
SELECT id, caserecnumber INTO countverificationaudit.{working_column}_cases FROM countverification.non_cp1_cases;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_cases
)
WHERE supervision_table = 'cases';

-- phonenumbers
DROP TABLE IF EXISTS countverificationaudit.{working_column}_phonenumbers;
SELECT id, caserecnumber, deputy_id INTO countverificationaudit.{working_column}_phonenumbers
FROM (
    SELECT pn.id, cli.caserecnumber, null as deputy_id
    FROM phonenumbers pn
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = pn.person_id
    UNION
    SELECT pn.id, null, cast(dep.id as varchar)
    FROM phonenumbers pn
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = pn.person_id
) as a;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_phonenumbers
)
WHERE supervision_table = 'phonenumbers';

-- addresses
UPDATE countverification.counts SET {working_column} =
(
    -- client
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = ad.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = ad.person_id
)
WHERE supervision_table = 'addresses';

-- supervision_notes
DROP TABLE IF EXISTS countverificationaudit.{working_column}_supervision_notes;
SELECT id, caserecnumber, deputy_id INTO countverificationaudit.{working_column}_supervision_notes
FROM
(
    SELECT sn.id, cli.caserecnumber, null as deputy_id
    FROM supervision_notes sn
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = sn.person_id
    UNION
    SELECT sn.id, null, cast(dep.id as varchar)
    FROM supervision_notes sn
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = sn.person_id
) as a;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_supervision_notes
)
WHERE supervision_table = 'supervision_notes';

-- tasks
DROP TABLE IF EXISTS countverificationaudit.{working_column}_tasks;
SELECT t.id, cli.caserecnumber INTO countverificationaudit.{working_column}_tasks
FROM tasks t
INNER JOIN person_task pt ON pt.task_id = t.id
INNER JOIN countverification.non_cp1_clients cli ON cli.id = pt.person_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_tasks
)
WHERE supervision_table = 'tasks';

-- death_notifications
DROP TABLE IF EXISTS countverificationaudit.{working_column}_death_notifications;
SELECT id, caserecnumber, deputy_id INTO countverificationaudit.{working_column}_death_notifications
FROM
(
    -- client
    SELECT dn.id, cli.caserecnumber, null as deputy_id
    FROM death_notifications dn
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = dn.person_id
    UNION
    -- deputy
    SELECT dn.id, null, cast(dep.id as varchar)
    FROM death_notifications dn
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = dn.person_id
) as a;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_death_notifications
)
WHERE supervision_table = 'death_notifications';

-- warnings
DROP TABLE IF EXISTS countverificationaudit.{working_column}_warnings;
SELECT id, caserecnumber, deputy_id INTO countverificationaudit.{working_column}_warnings
FROM
(
    -- client
    SELECT w.id, cli.caserecnumber, null as deputy_id
    FROM warnings w
    INNER JOIN person_warning pw ON pw.warning_id = w.id
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = pw.person_id
    UNION
    -- deputy
    SELECT w.id, null, cast(dep.id as varchar)
    FROM warnings w
    INNER JOIN person_warning pw ON pw.warning_id = w.id
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = pw.person_id
) as a;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_warnings
)
WHERE supervision_table = 'warnings';

-- annual_report_logs
DROP TABLE IF EXISTS countverificationaudit.{working_column}_annual_report_logs;
SELECT arl.id, cli.caserecnumber INTO countverificationaudit.{working_column}_annual_report_logs
FROM annual_report_logs arl
INNER JOIN countverification.non_cp1_clients cli ON cli.id = arl.client_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_annual_report_logs
)
WHERE supervision_table = 'annual_report_logs';

-- annual_report_lodging_details
DROP TABLE IF EXISTS countverificationaudit.{working_column}_annual_report_lodging_details;
SELECT det.id, cli.caserecnumber INTO countverificationaudit.{working_column}_annual_report_lodging_details
FROM annual_report_lodging_details det
INNER JOIN annual_report_logs arl ON arl.id = det.annual_report_log_id
INNER JOIN countverification.non_cp1_clients cli ON cli.id = arl.client_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_annual_report_lodging_details
)
WHERE supervision_table = 'annual_report_lodging_details';

-- visits
DROP TABLE IF EXISTS countverificationaudit.{working_column}_visits;
SELECT v.id, cli.caserecnumber INTO countverificationaudit.{working_column}_visits
FROM visits v
INNER JOIN countverification.non_cp1_clients cli ON cli.id = v.client_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_visits
)
WHERE supervision_table = 'visits';

-- bonds
DROP TABLE IF EXISTS countverificationaudit.{working_column}_bonds;
SELECT bon.id, non_cp1_cases.caserecnumber INTO countverificationaudit.{working_column}_bonds
FROM bonds bon
INNER JOIN countverification.non_cp1_cases ON non_cp1_cases.id = bon.order_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_bonds
)
WHERE supervision_table = 'bonds';

-- feepayer_id
DROP TABLE IF EXISTS countverificationaudit.{working_column}_feepayer_id;
SELECT p.id, cli.caserecnumber INTO countverificationaudit.{working_column}_feepayer_id
FROM persons p
INNER JOIN countverification.non_cp1_clients cli ON cli.id = p.id
WHERE p.feepayer_id IS NOT NULL;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_feepayer_id
)
WHERE supervision_table = 'feepayer_id';

-- timeline_event
DROP TABLE IF EXISTS countverificationaudit.{working_column}_timeline_event;
SELECT e.id as event_id, pt.id as person_id INTO countverificationaudit.{working_column}_timeline_event
FROM timeline_event e
INNER JOIN person_timeline pt on e.id = pt.timelineevent_id
INNER JOIN countverification.non_cp1_clients cli ON cli.id = pt.person_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_timeline_event
)
WHERE supervision_table = 'timeline_event';

-- supervision_level_log
DROP TABLE IF EXISTS countverificationaudit.{working_column}_supervision_level_log;
SELECT sll.id, non_cp1_cases.caserecnumber INTO countverificationaudit.{working_column}_supervision_level_log
FROM supervision_level_log sll
INNER JOIN countverification.non_cp1_cases ON non_cp1_cases.id = sll.order_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_supervision_level_log
)
WHERE supervision_table = 'supervision_level_log';

-- finance_invoice_ad
DROP TABLE IF EXISTS countverificationaudit.{working_column}_finance_invoice_ad;
SELECT inv.id, cli.caserecnumber INTO countverificationaudit.{working_column}_finance_invoice_ad
FROM finance_invoice inv
INNER JOIN countverification.non_cp1_clients cli ON cli.id = inv.person_id
WHERE inv.source = 'CASRECMIGRATION'
AND inv.feetype = 'AD';
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_finance_invoice_ad
)
WHERE supervision_table = 'finance_invoice_ad';

-- finance_invoice_non_ad
DROP TABLE IF EXISTS countverificationaudit.{working_column}_finance_invoice_non_ad;
SELECT inv.id, cli.caserecnumber INTO countverificationaudit.{working_column}_finance_invoice_non_ad
FROM finance_invoice inv
INNER JOIN countverification.non_cp1_clients cli ON cli.id = inv.person_id
WHERE inv.source = 'CASRECMIGRATION'
AND inv.feetype <> 'AD';
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_finance_invoice_non_ad
)
WHERE supervision_table = 'finance_invoice_non_ad';

-- finance_remissions
DROP TABLE IF EXISTS countverificationaudit.{working_column}_finance_remissions;
SELECT rem.id, cli.caserecnumber INTO countverificationaudit.{working_column}_finance_remissions
FROM finance_remission_exemption rem
LEFT JOIN finance_person fp ON fp.id = rem.finance_person_id
INNER JOIN countverification.non_cp1_clients cli ON cli.id = fp.person_id
WHERE rem.discounttype = 'REMISSION';
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_finance_remissions
)
WHERE supervision_table = 'finance_remissions';

-- finance_exemptions
DROP TABLE IF EXISTS countverificationaudit.{working_column}_finance_exemptions;
SELECT rem.id, cli.caserecnumber INTO countverificationaudit.{working_column}_finance_exemptions
FROM finance_remission_exemption rem
LEFT JOIN finance_person fp ON fp.id = rem.finance_person_id
INNER JOIN countverification.non_cp1_clients cli ON cli.id = fp.person_id
WHERE rem.discounttype = 'EXEMPTION';
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) from countverificationaudit.{working_column}_finance_exemptions
)
WHERE supervision_table = 'finance_exemptions';

-- finance_ledger_credits
DROP TABLE IF EXISTS countverificationaudit.{working_column}_finance_ledger_credits;
SELECT lgr.id, cli.caserecnumber INTO countverificationaudit.{working_column}_finance_ledger_credits
FROM finance_ledger lgr
LEFT JOIN finance_person fp ON fp.id = lgr.finance_person_id
INNER JOIN countverification.non_cp1_clients cli ON cli.id = fp.person_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_finance_ledger_credits
)
WHERE supervision_table = 'finance_ledger_credits';

-- finance_allocation_credits
DROP TABLE IF EXISTS countverificationaudit.{working_column}_finance_allocation_credits;
SELECT fla.id, cli.caserecnumber INTO countverificationaudit.{working_column}_finance_allocation_credits
FROM finance_ledger_allocation fla
LEFT JOIN finance_invoice inv ON inv.id = fla.invoice_id
INNER JOIN countverification.non_cp1_clients cli ON cli.id = inv.person_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_finance_allocation_credits
)
WHERE supervision_table = 'finance_allocation_credits';

-- finance_person
DROP TABLE IF EXISTS countverificationaudit.{working_column}_finance_person;
SELECT fp.id, cli.caserecnumber INTO countverificationaudit.{working_column}_finance_person
FROM finance_person fp
INNER JOIN countverification.non_cp1_clients cli ON cli.id = fp.person_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_finance_person

)
WHERE supervision_table = 'finance_person';

-- finance_order
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM
    (
        SELECT distinct p.caserecnumber, fo.billing_start_date
        FROM finance_order fo
        INNER JOIN countverification.non_cp1_cases
        ON non_cp1_cases.id = fo.order_id
        INNER JOIN finance_person fp
        ON fp.id = fo.finance_person_id
        INNER JOIN persons p
        ON p.id = fp.person_id
    ) AS a
)
WHERE supervision_table = 'finance_order';

-- order_deputy
DROP TABLE IF EXISTS countverificationaudit.{working_column}_order_deputy;
SELECT od.id, non_cp1_cases.caserecnumber INTO countverificationaudit.{working_column}_order_deputy
FROM order_deputy od
INNER JOIN countverification.non_cp1_cases ON non_cp1_cases.id = od.order_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_order_deputy
)
WHERE supervision_table = 'order_deputy';

-- person_caseitem
DROP TABLE IF EXISTS countverificationaudit.{working_column}_person_caseitem;
SELECT pci.caseitem_id, cli.caserecnumber INTO countverificationaudit.{working_column}_person_caseitem
FROM person_caseitem pci
INNER JOIN countverification.non_cp1_clients cli ON cli.id = pci.person_id;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_person_caseitem
)
WHERE supervision_table = 'person_caseitem';

-- person_warning
DROP TABLE IF EXISTS countverificationaudit.{working_column}_person_warning;
SELECT warning_id, caserecnumber, deputy_id INTO countverificationaudit.{working_column}_person_warning
FROM (
    SELECT pw.warning_id, cli.caserecnumber, null as deputy_id
    FROM person_warning pw
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = pw.person_id
    UNION
    SELECT pw.warning_id, null, cast(dep.id as varchar)
    FROM person_warning pw
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = pw.person_id
) as a;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_person_warning
)
WHERE supervision_table = 'person_warning';

-- person_task
DROP TABLE IF EXISTS countverificationaudit.{working_column}_person_task;
SELECT task_id, caserecnumber, deputy_id INTO countverificationaudit.{working_column}_person_task
FROM (
    SELECT pt.task_id, cli.caserecnumber, null as deputy_id
    FROM person_task pt
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = pt.person_id
    UNION
    SELECT pt.task_id, null, cast(dep.id as varchar)
    FROM person_task pt
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = pt.person_id
) as a;
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_person_task
)
WHERE supervision_table = 'person_task';

-- person_timeline
DROP TABLE IF EXISTS countverificationaudit.{working_column}_person_timeline;
SELECT id, caserecnumber, deputy_id INTO countverificationaudit.{working_column}_person_timeline
FROM (
    SELECT pt.id, cli.caserecnumber, null as deputy_id
        FROM person_timeline pt
        INNER JOIN countverification.non_cp1_clients cli ON cli.id = pt.person_id
    UNION
    SELECT pt.id, null, cast(dep.id as varchar)
        FROM person_timeline pt
        INNER JOIN countverification.non_cp1_deputies dep ON dep.id = pt.person_id
) as a;
UPDATE countverification.counts
SET {working_column} =(
    SELECT COUNT(*) FROM countverificationaudit.{working_column}_person_timeline
)
WHERE supervision_table = 'person_timeline';
