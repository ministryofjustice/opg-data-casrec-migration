CREATE TABLE IF NOT EXISTS countverification.cp1_clients (id int);
INSERT INTO countverification.cp1_clients (id)
SELECT id FROM persons p
WHERE p.type = 'actor_client'
  AND p.caseactorgroup = 'CLIENT-PILOT-ONE'
  AND COALESCE(p.clientsource, '') != 'CASRECMIGRATION';
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

ALTER TABLE countverification.counts DROP COLUMN IF EXISTS {working_column};
ALTER TABLE countverification.counts ADD COLUMN {working_column} int;

-- persons_clients
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverification.cp1_clients
)
WHERE supervision_table = 'persons_clients';

-- persons_deputies
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverification.cp1_deputies
)
WHERE supervision_table = 'persons_deputies';

-- persons (both)
UPDATE countverification.counts
SET {working_column} =
    (SELECT COUNT(*) FROM countverification.cp1_clients)
    +
    (SELECT COUNT(*) FROM countverification.cp1_deputies)
WHERE supervision_table = 'persons';

-- cases
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) FROM countverification.cp1_cases
)
WHERE supervision_table = 'cases';

-- phonenumbers
UPDATE countverification.counts
SET {working_column} =
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
    )
WHERE supervision_table = 'phonenumbers';

-- addresses
UPDATE countverification.counts
SET {working_column} =
    (
        -- client
        SELECT COUNT(*)
        FROM addresses ad
        INNER JOIN countverification.cp1_clients cli ON cli.id = ad.person_id
    )+(
        -- deputy
        SELECT COUNT(*)
        FROM
        (
            SELECT DISTINCT p.email, p.surname, p.firstname, ad.postcode
            FROM addresses ad
            INNER JOIN countverification.cp1_deputies dep ON dep.id = ad.person_id
            INNER JOIN persons p ON p.id = dep.id
        ) as a
    )
WHERE supervision_table = 'addresses';

-- supervision_notes
UPDATE countverification.counts
SET {working_column} =
    (
        SELECT COUNT(*)
        FROM supervision_notes sn
        INNER JOIN countverification.cp1_clients cli ON cli.id = sn.person_id
    )+(
        SELECT COUNT(*)
        FROM supervision_notes sn
        INNER JOIN countverification.cp1_deputies dep ON dep.id = sn.person_id
    )
WHERE supervision_table = 'supervision_notes';

-- tasks
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM tasks t
    INNER JOIN person_task pt ON pt.task_id = t.id
    INNER JOIN countverification.cp1_clients cli on cli.id = pt.person_id
)
WHERE supervision_table = 'tasks';

-- death_notifications
UPDATE countverification.counts
SET {working_column} =
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
    )
WHERE supervision_table = 'death_notifications';

-- warnings
UPDATE countverification.counts
SET {working_column} =
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
    )
WHERE supervision_table = 'warnings';

-- annual_report_logs
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM annual_report_logs arl
    INNER JOIN countverification.cp1_clients cli ON cli.id = arl.client_id
)
WHERE supervision_table = 'annual_report_logs';

-- annual_report_lodging_details
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) AS cp1existing
    FROM annual_report_lodging_details det
    INNER JOIN annual_report_logs arl ON arl.id = det.annual_report_log_id
    INNER JOIN countverification.cp1_clients cli ON cli.id = arl.client_id
)
WHERE supervision_table = 'annual_report_lodging_details';

-- visits
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) AS cp1existing
    FROM visits v
    INNER JOIN countverification.cp1_clients cli ON cli.id = v.client_id
)
WHERE supervision_table = 'visits';

-- bonds
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) AS cp1existing
    FROM bonds bon
    INNER JOIN countverification.cp1_cases ON cp1_cases.id = bon.order_id
)
WHERE supervision_table = 'bonds';

-- feepayer_id
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) AS cp1existing
    FROM persons p
    INNER JOIN countverification.cp1_clients cli ON cli.id = p.id
    WHERE p.feepayer_id IS NOT NULL
)
WHERE supervision_table = 'feepayer_id';

-- timeline_event
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM timeline_event
    WHERE event->'payload'->>'courtReference' IN (
        SELECT p.caserecnumber FROM persons p
        INNER JOIN countverification.cp1_clients cli ON cli.id = p.id
    )
)
WHERE supervision_table = 'timeline_event';

-- supervision_level_log
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM supervision_level_log sll
    INNER JOIN countverification.cp1_cases ON cp1_cases.id = sll.order_id
)
WHERE supervision_table = 'supervision_level_log';

-- finance_invoice_ad
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM finance_invoice inv
    INNER JOIN countverification.cp1_clients cli on cli.id = inv.person_id
    WHERE inv.source = 'CASRECMIGRATION'
    AND inv.feetype = 'AD'
)
WHERE supervision_table = 'finance_invoice_ad';

-- finance_invoice_non_ad
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM finance_invoice inv
    INNER JOIN countverification.cp1_clients cli on cli.id = inv.person_id
    WHERE inv.source = 'CASRECMIGRATION'
    AND inv.feetype <> 'AD'
)
WHERE supervision_table = 'finance_invoice_non_ad';

-- finance_remissions
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM finance_remission_exemption rem
    LEFT JOIN finance_person fp ON fp.id = rem.finance_person_id
    INNER JOIN countverification.cp1_clients cli on cli.id = fp.person_id
    WHERE rem.discounttype = 'REMISSION'
)
WHERE supervision_table = 'finance_remissions';

-- finance_exemptions
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*) AS cp1existing
    FROM finance_remission_exemption rem
    LEFT JOIN finance_person fp ON fp.id = rem.finance_person_id
    INNER JOIN countverification.cp1_clients cli on cli.id = fp.person_id
    WHERE rem.discounttype = 'EXEMPTION'
)
WHERE supervision_table = 'finance_exemptions';

-- finance_ledger_credits
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM finance_ledger lgr
    LEFT JOIN finance_person fp ON fp.id = lgr.finance_person_id
    INNER JOIN countverification.cp1_clients cli on cli.id = fp.person_id
)
WHERE supervision_table = 'finance_ledger_credits';

-- finance_allocation_credits
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM finance_ledger_allocation fla
    LEFT JOIN finance_invoice inv ON inv.id = fla.invoice_id
    INNER JOIN countverification.cp1_clients cli on cli.id = inv.person_id
)
WHERE supervision_table = 'finance_allocation_credits';

-- finance_person
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM finance_person fp
    INNER JOIN countverification.cp1_clients cli on cli.id = fp.person_id
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
        INNER JOIN countverification.cp1_cases
        ON cp1_cases.id = fo.order_id
        INNER JOIN finance_person fp
        ON fp.id = fo.finance_person_id
        INNER JOIN persons p
        ON p.id = fp.person_id
    ) as a;
)
WHERE supervision_table = 'finance_order';

-- order_deputy
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM order_deputy od
    INNER JOIN countverification.cp1_cases ON cp1_cases.id = od.order_id
)
WHERE supervision_table = 'order_deputy';

-- person_caseitem
UPDATE countverification.counts
SET {working_column} = (
    SELECT COUNT(*)
    FROM person_caseitem pci
    INNER JOIN countverification.cp1_clients cli on cli.id = pci.person_id
)
WHERE supervision_table = 'person_caseitem';

-- person_warning
UPDATE countverification.counts
SET {working_column} =
    (
        SELECT COUNT(*)
        FROM person_warning pw
        INNER JOIN countverification.cp1_clients cli on cli.id = pw.person_id
    )+(
        SELECT COUNT(*)
        FROM person_warning pw
        INNER JOIN countverification.cp1_deputies dep on dep.id = pw.person_id
    )
WHERE supervision_table = 'person_warning';

-- person_task
UPDATE countverification.counts
SET {working_column} =
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
)
WHERE supervision_table = 'person_task';

-- person_timeline
UPDATE countverification.counts
SET {working_column} =
    (
        SELECT COUNT(*)
        FROM person_timeline pt
        INNER JOIN countverification.cp1_clients cli on cli.id = pt.person_id
    )+(
        SELECT COUNT(*)
        FROM person_timeline pt
        INNER JOIN countverification.cp1_deputies dep on dep.id = pt.person_id
    )
WHERE supervision_table = 'person_timeline';

DROP INDEX countverification.cp1_clients_idx;
DROP INDEX countverification.cp1_cases_idx;
DROP INDEX countverification.cp1_deputies_idx;

DROP TABLE countverification.cp1_clients;
DROP TABLE countverification.cp1_cases;
DROP TABLE countverification.cp1_deputies;
