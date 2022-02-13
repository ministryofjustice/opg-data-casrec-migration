INSERT INTO deletions.base_clients_persons (id, caserecnumber)
SELECT distinct p.id, p.caserecnumber
FROM persons p
WHERE p.type = 'actor_client' AND COALESCE(caseactorgroup, '') <> 'CLIENT-PILOT-ONE';

select a.id as ids_bad_delete
from
(
    SELECT s.id
    FROM person_timeline s
    INNER JOIN persons bcp ON bcp.id = s.person_id
    WHERE bcp.type = 'actor_client' AND COALESCE(bcp.caseactorgroup, '') <> 'CLIENT-PILOT-ONE'
    union
    SELECT s.id
    FROM person_timeline s
    INNER JOIN persons dep ON dep.id = s.person_id
    INNER JOIN order_deputy od ON dep.id = od.deputy_id
    INNER JOIN cases c  ON c.id = od.order_id
    INNER JOIN persons bcp ON bcp.id = c.client_id
    WHERE bcp.type = 'actor_client' AND COALESCE(bcp.caseactorgroup, '') <> 'CLIENT-PILOT-ONE'
    AND dep.id NOT IN (
        SELECT distinct dep.id
        FROM persons dep
        INNER JOIN order_deputy od ON dep.id = od.deputy_id
        INNER JOIN cases c  ON c.id = od.order_id
        INNER JOIN persons p ON p.id = c.client_id
        WHERE p.type = 'actor_client' and p.caseactorgroup = 'CLIENT-PILOT-ONE'
        UNION
        SELECT distinct p.feepayer_id
        FROM persons p
        WHERE p.type = 'actor_client' and p.caseactorgroup = 'CLIENT-PILOT-ONE'
    )
) as a
inner join
(
    SELECT pt.id
    FROM persons p
    INNER JOIN person_timeline pt ON pt.person_id = p.id
    WHERE p.type = 'actor_client'
    AND p.caseactorgroup = 'CLIENT-PILOT-ONE'
    union
    SELECT pt.id
    FROM persons p
    INNER JOIN cases c ON c.client_id = p.id
    INNER JOIN order_deputy od ON od.order_id = c.id
    INNER JOIN persons dep ON dep.id = od.deputy_id
    INNER JOIN person_timeline pt ON pt.person_id = dep.id
    WHERE p.type = 'actor_client'
    AND p.caseactorgroup = 'CLIENT-PILOT-ONE'
) as b ON a.id = b.id;



SELECT id FROM persons p
INNER JOIN cases c ON c.client_id = p.id
INNER JOIN order_deputy od ON od.order_id = c.id
INNER JOIN persons dep ON dep.id = od.deputy_id;
WHERE p.type = 'actor_client'
AND p.caseactorgroup = 'CLIENT-PILOT-ONE';

select max(id)
from (
    SELECT pt.id
    FROM persons p
    INNER JOIN person_timeline pt ON pt.person_id = p.id
    WHERE p.type = 'actor_client'
    AND p.caseactorgroup = 'CLIENT-PILOT-ONE'
    AND coalesce(p.clientsource, '') != 'CASRECMIGRATION'
    union
    SELECT pt.id
    FROM persons p
    INNER JOIN cases c ON c.client_id = p.id
    INNER JOIN order_deputy od ON od.order_id = c.id
    INNER JOIN persons dep ON dep.id = od.deputy_id
    INNER JOIN person_timeline pt ON pt.person_id = dep.id
    WHERE p.type = 'actor_client'
    AND p.caseactorgroup = 'CLIENT-PILOT-ONE'
    AND coalesce(p.clientsource, '') != 'CASRECMIGRATION'
) as a;



-- CP1 person_timeline ids
SELECT pt.id
FROM persons p
INNER JOIN person_timeline pt ON pt.person_id = p.id
WHERE p.type = 'actor_client'
AND p.caseactorgroup = 'CLIENT-PILOT-ONE'
union
SELECT pt.id
FROM persons p
INNER JOIN cases c ON c.client_id = p.id
INNER JOIN order_deputy od ON od.order_id = c.id
INNER JOIN persons dep ON dep.id = od.deputy_id
INNER JOIN person_timeline pt ON pt.person_id = dep.id
WHERE p.type = 'actor_client'
AND p.caseactorgroup = 'CLIENT-PILOT-ONE';



    (
        SELECT COUNT(*)
        FROM person_timeline pt
        INNER JOIN countverification.cp1_clients cli ON cli.id = pt.person_id
    )+(
        SELECT COUNT(*)
        FROM person_timeline pt
        INNER JOIN countverification.cp1_deputies dep ON dep.id = pt.person_id
    )



SELECT id into countverification.tl_events
FROM timeline_event
WHERE event->'payload'->>'courtReference' IN (
    SELECT p.caserecnumber FROM persons p
    WHERE p.type = 'actor_client'
    AND p.caseactorgroup = 'CLIENT-PILOT-ONE'
    AND coalesce(p.clientsource, '') != 'CASRECMIGRATION'
);