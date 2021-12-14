DROP SCHEMA IF EXISTS countverification CASCADE;
CREATE SCHEMA countverification;

CREATE TABLE IF NOT EXISTS countverification.clients (id int);
INSERT INTO countverification.clients (id)
SELECT id FROM persons p WHERE p.type = 'actor_client' AND p.caseactorgroup = 'CLIENT-PILOT-ONE';

CREATE TABLE IF NOT EXISTS countverification.cases (id int);
INSERT INTO countverification.cases (id)
SELECT cases.id FROM countverification.clients INNER JOIN cases ON cases.client_id = clients.id;

CREATE TABLE IF NOT EXISTS countverification.deputies (id int);
INSERT INTO countverification.deputies (id)
SELECT dep.id
FROM countverification.cases
    INNER JOIN order_deputy od ON od.order_id = cases.id
    INNER JOIN persons dep ON dep.id = od.deputy_id;

CREATE TABLE IF NOT EXISTS countverification.counts (
    supervision_table varchar(100),
    cp1existing int
);

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'persons' AS supervision_table,
(
    SELECT COUNT(*) FROM countverification.clients
)+(
    SELECT COUNT(*) FROM countverification.deputies
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'cases' AS supervision_table, COUNT(*) AS cp1existing
FROM countverification.cases;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'phonenumbers' AS supervision_table,
(
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.clients cli ON cli.id = pn.person_id
)+(
    SELECT COUNT(*)
    FROM phonenumbers pn
    INNER JOIN countverification.deputies dep ON dep.id = pn.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'addresses' AS supervision_table,
(
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.clients cli ON cli.id = ad.person_id
)+(
    SELECT COUNT(*)
    FROM addresses ad
    INNER JOIN countverification.deputies dep ON dep.id = ad.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'supervision_notes' AS supervision_table,
(
    SELECT COUNT(*)
    FROM supervision_notes sn
    INNER JOIN countverification.clients cli ON cli.id = sn.person_id
)+(
    SELECT COUNT(*)
    FROM supervision_notes sn
    INNER JOIN countverification.deputies dep ON dep.id = sn.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'tasks' AS supervision_table,
(
    SELECT COUNT(*)
    FROM tasks t
    INNER JOIN person_task pt ON pt.task_id = t.id
    INNER JOIN countverification.clients cli on cli.id = pt.person_id
)+(
    SELECT COUNT(*)
    FROM tasks t
    INNER JOIN person_task pt ON pt.task_id = t.id
    INNER JOIN countverification.deputies dep on dep.id = pt.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'death_notifications' AS supervision_table,
(
    SELECT COUNT(*)
    FROM death_notifications dn
    INNER JOIN countverification.clients cli on cli.id = dn.person_id
)+(
    SELECT COUNT(*)
    FROM death_notifications dn
    INNER JOIN countverification.deputies dep on dep.id = dn.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'warnings' AS supervision_table,
(
    SELECT COUNT(*)
    FROM warnings w
    INNER JOIN person_warning pw on pw.warning_id = w.id
    INNER JOIN countverification.clients cli on cli.id = pw.person_id
)+(
    SELECT COUNT(*)
    FROM warnings w
    INNER JOIN person_warning pw on pw.warning_id = w.id
    INNER JOIN countverification.deputies dep on dep.id = pw.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'powerofattorney_person' AS supervision_table,
(
    SELECT COUNT(*)
    FROM powerofattorney_person poa
    INNER JOIN countverification.clients cli on cli.id = poa.person_id
)+(
    SELECT COUNT(*)
    FROM powerofattorney_person poa
    INNER JOIN countverification.deputies dep on dep.id = poa.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'annual_report_logs' AS supervision_table,
(
    SELECT COUNT(*)
    FROM annual_report_logs al
    INNER JOIN countverification.clients cli ON cli.id = al.client_id
)+(
    SELECT COUNT(*)
    FROM annual_report_logs al
    INNER JOIN countverification.cases ON cases.id = al.order_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'visits' AS supervision_table, COUNT(*) AS cp1existing
FROM visits v
LEFT JOIN countverification.clients cli ON cli.id = v.client_id;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'order_deputy' AS supervision_table, COUNT(*) AS cp1existing
FROM order_deputy od
INNER JOIN countverification.cases ON cases.id = od.order_id;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'bonds' AS supervision_table, COUNT(*) AS cp1existing
FROM bonds bon
INNER JOIN countverification.cases ON cases.id = bon.order_id;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'feepayer_id' AS supervision_table, COUNT(*) AS cp1existing
FROM persons cli
WHERE cli.type = 'actor_client' AND cli.caseactorgroup = 'CLIENT-PILOT-ONE'
AND cli.feepayer_id IS NOT NULL;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'timeline_event' AS supervision_table,
(
    SELECT COUNT(*)
    FROM timeline_event te
    INNER JOIN person_timeline pt on pt.timelineevent_id = te.id
    INNER JOIN countverification.clients cli on cli.id = pt.person_id
)+(
    SELECT COUNT(*)
    FROM timeline_event te
    INNER JOIN person_timeline pt on pt.timelineevent_id = te.id
    INNER JOIN countverification.deputies dep on dep.id = pt.person_id
) AS cp1existing;

-- not sure how much value these person_x add

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT 'person_caseitem' AS supervision_table, COUNT(*) AS cp1existing
FROM person_caseitem pci
INNER JOIN countverification.clients cli on cli.id = pci.person_id;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'person_warning' AS supervision_table,
(
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.clients cli on cli.id = pw.person_id
)+(
    SELECT COUNT(*)
    FROM person_warning pw
    INNER JOIN countverification.deputies dep on dep.id = pw.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'person_task' AS supervision_table,
(
    SELECT COUNT(*)
    FROM person_task pt
    INNER JOIN countverification.clients cli on cli.id = pt.person_id
)+(
    SELECT COUNT(*)
    FROM person_task pt
    INNER JOIN countverification.deputies dep on dep.id = pt.person_id
) AS cp1existing;

INSERT INTO countverification.counts (supervision_table, cp1existing)
SELECT
'person_timeline' AS supervision_table,
(
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN countverification.clients cli on cli.id = pt.person_id
)+(
    SELECT COUNT(*)
    FROM person_timeline pt
    INNER JOIN countverification.deputies dep on dep.id = pt.person_id
) AS cp1existing;

DROP TABLE countverification.clients;
DROP TABLE countverification.cases;
DROP TABLE countverification.deputies;
