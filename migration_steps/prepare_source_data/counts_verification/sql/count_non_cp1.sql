-- dropping and recreating unexpected columns simplifies on local dev where tests may be run out of order
ALTER TABLE countverification.counts DROP COLUMN IF EXISTS non_cp1;
ALTER TABLE countverification.counts ADD COLUMN non_cp1 int NOT NULL DEFAULT -1;

DROP TABLE IF EXISTS countverification.non_cp1_clients;
CREATE TABLE IF NOT EXISTS countverification.non_cp1_clients (id int);
INSERT INTO countverification.non_cp1_clients (id) (
    SELECT id FROM persons p
    WHERE p.type = 'actor_client'
      AND (caseactorgroup != 'CLIENT-PILOT-ONE' OR caseactorgroup IS NULL)
);
CREATE UNIQUE INDEX non_cp1_clients_idx ON countverification.non_cp1_clients (id);

DROP TABLE IF EXISTS countverification.non_cp1_cases;
CREATE TABLE IF NOT EXISTS countverification.non_cp1_cases (id int);
INSERT INTO countverification.non_cp1_cases (id) (
    SELECT DISTINCT id
    FROM cases
    WHERE client_id IN (
        SELECT id FROM countverification.non_cp1_clients
    )
);
CREATE UNIQUE INDEX non_cp1_cases_idx ON countverification.non_cp1_cases (id);

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
    WHERE dep.type = 'actor_deputy'
    AND c.id IS NULL
);
CREATE UNIQUE INDEX non_cp1_deputies_idx ON countverification.non_cp1_deputies (id);

-- persons_clients
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM countverification.non_cp1_clients
)
WHERE supervision_table = 'persons_clients';

-- persons_deputies
UPDATE countverification.counts SET non_cp1 =
(
    SELECT (
        -- regular
        SELECT COUNT(*)
        FROM countverification.non_cp1_cases c
        INNER JOIN order_deputy od ON od.order_id = c.id
        INNER JOIN persons dep ON dep.id = od.deputy_id
        WHERE dep.type = 'actor_deputy'
    )+(
        -- plus deputies with no entry in order_deputy or case
        SELECT COUNT(*)
        FROM persons p
        LEFT JOIN order_deputy od on p.id = od.deputy_id
        LEFT JOIN cases c on c.id = od.order_id
        WHERE p.type = 'actor_deputy'
        AND c.id IS NULL
    )
)
WHERE supervision_table = 'persons_deputies';

-- cases
UPDATE countverification.counts SET non_cp1 = (
    SELECT COUNT(*)
    FROM cases
    WHERE client_id IN (
        SELECT id FROM countverification.non_cp1_clients
    )
)
WHERE supervision_table = 'cases';

-- phonenumbers
UPDATE countverification.counts SET non_cp1 =
(
    -- client
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = pn.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = pn.person_id
)
WHERE supervision_table = 'phonenumbers';

-- addresses
UPDATE countverification.counts SET non_cp1 =
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
UPDATE countverification.counts SET non_cp1 =
(
    -- client
    SELECT COUNT(*)
    FROM supervision_notes sn
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = sn.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM supervision_notes sn
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = sn.person_id
)
WHERE supervision_table = 'supervision_notes';

-- tasks
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM tasks t
    INNER JOIN person_task pt ON pt.task_id = t.id
    INNER JOIN countverification.non_cp1_clients cli on cli.id = pt.person_id
)
WHERE supervision_table = 'tasks';

-- death notifications
UPDATE countverification.counts SET non_cp1 =
(
    -- client
    SELECT COUNT(*)
    FROM death_notifications dn
    INNER JOIN countverification.non_cp1_clients cli on cli.id = dn.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM death_notifications dn
    INNER JOIN countverification.non_cp1_deputies dep on dep.id = dn.person_id
)
WHERE supervision_table = 'death_notifications';

-- warnings
UPDATE countverification.counts SET non_cp1 =
(
    -- client
    SELECT COUNT(*)
    FROM warnings w
    INNER JOIN person_warning pw on pw.warning_id = w.id
    INNER JOIN countverification.non_cp1_clients cli on cli.id = pw.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM warnings w
    INNER JOIN person_warning pw on pw.warning_id = w.id
    INNER JOIN countverification.non_cp1_deputies dep on dep.id = pw.person_id
)
WHERE supervision_table = 'warnings';

-- annual_report_logs
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM annual_report_logs arl
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = arl.client_id
)
WHERE supervision_table = 'annual_report_logs';

-- annual_report_lodging_details
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM annual_report_lodging_details det
    INNER JOIN annual_report_logs arl ON arl.id = det.annual_report_log_id
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = arl.client_id
)
WHERE supervision_table = 'annual_report_lodging_details';

-- visits
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM visits v
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = v.client_id
)
WHERE supervision_table = 'visits';

-- bonds
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM bonds b
    INNER JOIN countverification.non_cp1_cases c ON c.id = b.order_id
)
WHERE supervision_table = 'bonds';

-- feepayer_id
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM countverification.non_cp1_clients cli
    INNER JOIN persons p ON p.id = cli.id
    WHERE p.feepayer_id IS NOT NULL
)
WHERE supervision_table = 'feepayer_id';

-- timeline_event
-- might be slow because of data in timeline_event table
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM timeline_event
    WHERE event->'payload'->>'type' = 'Case note'
      AND event->'payload'->>'courtReference' IN (
        SELECT p.caserecnumber FROM persons p
        INNER JOIN countverification.non_cp1_clients cli ON cli.id = p.id
    )
)
WHERE supervision_table = 'timeline_event';
-- -- timeline_event alternative
-- -- might be faster, but relies on person_timeline table
-- UPDATE countverification.counts SET non_cp1 =
-- (
--     SELECT COUNT(*)
--     FROM timeline_event te
--     INNER JOIN person_timeline pt ON pt.timelineevent_id = te.id
--     INNER JOIN countverification.non_cp1_clients cli ON cli.id = pt.person_id
-- )
-- WHERE supervision_table = 'timeline_event';

-- person_timeline
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN countverification.non_cp1_clients cli on cli.id = pt.person_id
)
WHERE supervision_table = 'person_timeline';

-- supervision_level_log
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM supervision_level_log sll
    INNER JOIN countverification.non_cp1_cases c ON c.id = sll.order_id
)
WHERE supervision_table = 'supervision_level_log';

-- finance_invoice_ad
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM finance_invoice inv
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = inv.person_id
    WHERE inv.feetype = 'AD'
)
WHERE supervision_table = 'finance_invoice_ad';

-- finance_invoice_non_ad
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM finance_invoice inv
    INNER JOIN countverification.non_cp1_clients cli ON cli.id = inv.person_id
    WHERE inv.feetype <> 'AD'
)
WHERE supervision_table = 'finance_invoice_non_ad';

-- finance_remissions
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM finance_remission_exemption rem
    LEFT JOIN finance_person fp ON fp.id = rem.finance_person_id
    INNER JOIN countverification.non_cp1_clients cli on cli.id = fp.person_id
    WHERE rem.discounttype = 'REMISSION'
)
WHERE supervision_table = 'finance_remissions';

-- finance_exemptions
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM finance_remission_exemption rem
    LEFT JOIN finance_person fp ON fp.id = rem.finance_person_id
    INNER JOIN countverification.non_cp1_clients cli on cli.id = fp.person_id
    WHERE rem.discounttype = 'EXEMPTION'
)
WHERE supervision_table = 'finance_exemptions';

-- finance_ledger_credits
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM finance_ledger lgr
    LEFT JOIN finance_person fp ON fp.id = lgr.finance_person_id
    INNER JOIN countverification.non_cp1_clients cli on cli.id = fp.person_id
)
WHERE supervision_table = 'finance_ledger_credits';

-- finance_allocation_credits
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM finance_ledger_allocation fla
    LEFT JOIN finance_invoice inv ON inv.id = fla.invoice_id
    INNER JOIN countverification.non_cp1_clients cli on cli.id = inv.person_id
)
WHERE supervision_table = 'finance_allocation_credits';

-- finance_person
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM finance_person fp
    INNER JOIN countverification.non_cp1_clients cli on cli.id = fp.person_id
)
WHERE supervision_table = 'finance_person';

-- finance_order
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM finance_order fo
    INNER JOIN countverification.non_cp1_cases c ON c.id = fo.order_id
)
WHERE supervision_table = 'finance_order';

-- order_deputy
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM order_deputy od
    INNER JOIN countverification.non_cp1_deputies dep ON dep.id = od.deputy_id
)
WHERE supervision_table = 'order_deputy';

-- person_caseitem
UPDATE countverification.counts SET non_cp1 =
(
    SELECT COUNT(*)
    FROM person_caseitem pci
    INNER JOIN countverification.non_cp1_clients cli on cli.id = pci.person_id
)
WHERE supervision_table = 'person_caseitem';

-- person_warning
UPDATE countverification.counts SET non_cp1 =
(
    -- client
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.non_cp1_clients cli on cli.id = pw.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.non_cp1_deputies dep on dep.id = pw.person_id
)
WHERE supervision_table = 'person_warning';

-- person_task
UPDATE countverification.counts SET non_cp1 =
(
    -- client
    SELECT COUNT(*)
    FROM person_task pt
    INNER JOIN countverification.non_cp1_clients cli on cli.id = pt.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM person_task pt
    INNER JOIN countverification.non_cp1_deputies dep on dep.id = pt.person_id
)
WHERE supervision_table = 'person_task';
