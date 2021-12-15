CREATE SCHEMA IF NOT EXISTS countverification;
CREATE TABLE IF NOT EXISTS countverification.counts (
    supervision_table varchar(100),
    cp1existing int,
    casrec_source int,
    expected int
);
ALTER TABLE countverification.counts ADD IF NOT EXISTS final_count int;

CREATE TABLE IF NOT EXISTS countverification.clients (id int);
INSERT INTO countverification.clients (id)
SELECT id FROM persons p WHERE p.type = 'actor_client' AND p.caseactorgroup = 'CLIENT-PILOT-ONE';
CREATE UNIQUE INDEX cp1clients_idx ON countverification.clients (id);

CREATE TABLE IF NOT EXISTS countverification.cases (id int);
INSERT INTO countverification.cases (id)
SELECT cases.id FROM countverification.clients INNER JOIN cases ON cases.client_id = clients.id;
CREATE UNIQUE INDEX cp1cases_idx ON countverification.cases (id);

CREATE TABLE IF NOT EXISTS countverification.deputies (id int);
INSERT INTO countverification.deputies (id)
SELECT DISTINCT dep.id
FROM countverification.cases
    INNER JOIN order_deputy od ON od.order_id = cases.id
    INNER JOIN persons dep ON dep.id = od.deputy_id;
CREATE UNIQUE INDEX cp1deputies_idx ON countverification.deputies (id);


-- persons
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*) FROM countverification.clients
)+(
    SELECT COUNT(*) FROM countverification.deputies
)
WHERE supervision_table = 'persons';

-- cases
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*) FROM countverification.cases
)
WHERE supervision_table = 'cases';

-- phonenumbers
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.clients cli ON cli.id = pn.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.deputies dep ON dep.id = pn.person_id
)
WHERE supervision_table = 'phonenumbers';

-- addresses
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.clients cli ON cli.id = ad.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.deputies dep ON dep.id = ad.person_id
)
WHERE supervision_table = 'addresses';

-- supervision_notes
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM supervision_notes sn
    INNER JOIN countverification.clients cli ON cli.id = sn.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM supervision_notes sn
    INNER JOIN countverification.deputies dep ON dep.id = sn.person_id
)
WHERE supervision_table = 'supervision_notes';

-- tasks
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*)
    FROM tasks t
    INNER JOIN person_task pt ON pt.task_id = t.id
    INNER JOIN countverification.clients cli on cli.id = pt.person_id
)
WHERE supervision_table = 'tasks';

-- death notifications
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM death_notifications dn
    INNER JOIN countverification.clients cli on cli.id = dn.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM death_notifications dn
    INNER JOIN countverification.deputies dep on dep.id = dn.person_id
)
WHERE supervision_table = 'death_notifications';

-- warnings
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM warnings w
    INNER JOIN person_warning pw on pw.warning_id = w.id
    INNER JOIN countverification.clients cli on cli.id = pw.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM warnings w
    INNER JOIN person_warning pw on pw.warning_id = w.id
    INNER JOIN countverification.deputies dep on dep.id = pw.person_id
)
WHERE supervision_table = 'warnings';

-- annual_report_logs
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM annual_report_logs al
    INNER JOIN countverification.clients cli ON cli.id = al.client_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM annual_report_logs al
    INNER JOIN countverification.cases ON cases.id = al.order_id
)
WHERE supervision_table = 'annual_report_logs';

-- visits
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*)
    FROM visits v
    LEFT JOIN countverification.clients cli ON cli.id = v.client_id
)
WHERE supervision_table = 'visits';

-- bonds
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*)
    FROM bonds bon
    INNER JOIN countverification.cases ON cases.id = bon.order_id
)
WHERE supervision_table = 'bonds';

-- feepayer_id
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*)
    FROM persons cli
    WHERE cli.type = 'actor_client' AND cli.caseactorgroup = 'CLIENT-PILOT-ONE'
    AND cli.feepayer_id IS NOT NULL
)
WHERE supervision_table = 'feepayer_id';

-- timeline_event
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM timeline_event te
    INNER JOIN person_timeline pt on pt.timelineevent_id = te.id
    INNER JOIN countverification.clients cli on cli.id = pt.person_id
)+(
    -- dpeuty
    SELECT COUNT(*)
    FROM timeline_event te
    INNER JOIN person_timeline pt on pt.timelineevent_id = te.id
    INNER JOIN countverification.deputies dep on dep.id = pt.person_id
)
WHERE supervision_table = 'timeline_event';

-- not sure how much value these person_x add

-- order_deputy
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*)
    FROM order_deputy od
    INNER JOIN countverification.cases ON cases.id = od.order_id
)
WHERE supervision_table = 'order_deputy';

-- person_caseitem
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*)
    FROM person_caseitem pci
    INNER JOIN countverification.clients cli on cli.id = pci.person_id
)
WHERE supervision_table = 'person_caseitem';

-- person_warning
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.clients cli on cli.id = pw.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.deputies dep on dep.id = pw.person_id
)
WHERE supervision_table = 'person_warning';

-- person_task
UPDATE countverification.counts SET final_count =
(
    -- client
    SELECT COUNT(*)
    FROM person_task pt
    INNER JOIN countverification.clients cli on cli.id = pt.person_id
)+(
    -- deputy
    SELECT COUNT(*)
    FROM person_task pt
    INNER JOIN countverification.deputies dep on dep.id = pt.person_id
)
WHERE supervision_table = 'person_task';

-- person_timeline
UPDATE countverification.counts SET final_count =
(
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN countverification.clients cli on cli.id = pt.person_id
)+(
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN countverification.deputies dep on dep.id = pt.person_id
)
WHERE supervision_table = 'person_timeline';


DROP INDEX countverification.cp1clients_idx;
DROP INDEX countverification.cp1cases_idx;
DROP INDEX countverification.cp1deputies_idx;

DROP TABLE countverification.clients;
DROP TABLE countverification.cases;
DROP TABLE countverification.deputies;

ALTER TABLE countverification.counts ADD result varchar(10);
UPDATE countverification.counts SET result = CASE WHEN final_count=expected THEN 'OK' ELSE 'ERROR' END;
