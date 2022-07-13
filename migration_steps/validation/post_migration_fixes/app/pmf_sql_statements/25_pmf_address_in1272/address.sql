--@setup_tag
CREATE SCHEMA IF NOT EXISTS jacktest;

-- clients P1
WITH clients_p1 AS (
    SELECT a.id AS address_id, "Case" AS caserecnumber, True AS expected, a.isairmailrequired AS actual
    FROM casrec_csv.pat
    LEFT JOIN persons p
        ON p.caserecnumber = pat."Case"
    LEFT JOIN addresses a
        ON a.person_id = p.id
    WHERE p.type = 'actor_client'
    AND clientsource = 'CASRECMIGRATION'
    AND pat."Foreign" = '1'
    AND (a.isairmailrequired IS NULL OR a.isairmailrequired != True)
)
SELECT *
INTO jacktest.client_address_updates_p1
FROM clients_p1;
-- ~100

-- clients P2
WITH clients_p2 AS (
    SELECT a.id AS address_id, "Case" AS caserecnumber, True AS expected, a.isairmailrequired AS actual
    FROM casrec_csv_p2.pat
        LEFT JOIN persons p
    ON p.caserecnumber = pat."Case"
        LEFT JOIN addresses a
    ON a.person_id = p.id
    WHERE p.type = 'actor_client'
    AND clientsource = 'CASRECMIGRATION_P2'
    AND pat."Foreign" = '1'
    AND (a.isairmailrequired IS NULL OR a.isairmailrequired != True)
)
SELECT *
INTO jacktest.client_address_updates_p2
FROM clients_p2;
-- 0

-- clients P3
WITH clients_p3 AS (
    SELECT a.id AS address_id, "Case" AS caserecnumber, True AS expected, a.isairmailrequired AS actual
    FROM casrec_csv_p3.pat
    LEFT JOIN persons p
    ON p.caserecnumber = pat."Case"
    LEFT JOIN addresses a
    ON a.person_id = p.id
    WHERE p.type = 'actor_client'
    AND clientsource = 'CASRECMIGRATION_P3'
    AND pat."Foreign" = '1'
    AND (a.isairmailrequired IS NULL OR a.isairmailrequired != True)
)
SELECT *
INTO jacktest.client_address_updates_p3
FROM clients_p3;
-- 0


--@audit_tag
-- clients P1
SELECT a.*
INTO jacktest.client_address_audit_p1
FROM addresses a
INNER JOIN jacktest.client_address_updates_p1 cli
    ON cli.address_id = a.id;

-- clients P2
SELECT a.*
INTO jacktest.client_address_audit_p2
FROM addresses a
INNER JOIN jacktest.client_address_updates_p2 cli
    ON cli.address_id = a.id;

-- clients P3
SELECT a.*
INTO jacktest.client_address_audit_p3
FROM addresses a
INNER JOIN jacktest.client_address_updates_p3 cli
    ON cli.address_id = a.id;


--@update_tag
-- clients P1
UPDATE addresses a
SET isairmailrequired = u.expected
FROM jacktest.client_address_updates_p1 u
WHERE u.address_id = a.id;

-- clients P2
UPDATE addresses a
SET isairmailrequired = u.expected
FROM jacktest.client_address_updates_p2 u
WHERE u.address_id = a.id;

-- clients P3
UPDATE addresses a
SET isairmailrequired = u.expected
FROM jacktest.client_address_updates_p3 u
WHERE u.address_id = a.id;


--@validate_tag
-- clients P1
SELECT COUNT (1) FROM (
    SELECT address_id, expected
    FROM jacktest.client_address_updates_p1
    EXCEPT
    SELECT a.id, a.isairmailrequired
    FROM addresses a
    INNER JOIN jacktest.client_address_audit_p1 aud
        ON aud.id = a.id
) t1;
-- 100

-- clients P2
SELECT COUNT (1) FROM (
    SELECT address_id, expected
    FROM jacktest.client_address_updates_p2
    EXCEPT
    SELECT a.id, a.isairmailrequired
    FROM addresses a
    INNER JOIN jacktest.client_address_audit_p2 aud
        ON aud.id = a.id
) t1;
-- 0 ZERO - NO NEED TO UPDATE

-- clients P3
SELECT COUNT (1) FROM (
    SELECT address_id, expected
    FROM jacktest.client_address_updates_p3
    EXCEPT
    SELECT a.id, a.isairmailrequired
    FROM addresses a
    INNER JOIN jacktest.client_address_audit_p3 aud
        ON aud.id = a.id
) t1;
-- 0 ZERO - NO NEED TO UPDATE


-- D E P U T I E S --

-- create a worker deputy table as the persons table is too large/slow
DROP TABLE IF EXISTS jacktest.deputies;
SELECT id, deputynumber, clientsource
INTO jacktest.deputies
FROM persons
WHERE type = 'actor_deputy'
AND clientsource LIKE 'CASRECMIGRATION%';
CREATE INDEX idx_pmf1272_deputies_id ON jacktest.deputies USING btree (id);
CREATE INDEX idx_pmf1272_deputies_deputynumber ON jacktest.deputies USING btree (deputynumber);

-- deputies P1
WITH overseas_deputies AS (
    SELECT DISTINCT * FROM (
        SELECT
            d.id,
            ds."Case",
            ds."Deputy No",
            row_number() over (PARTITION BY ds."Case", ds."Deputy No") AS rownum
        FROM casrec_csv.deputy_address da
        INNER JOIN casrec_csv.deputyship ds
            ON ds."Dep Addr No" = da."Dep Addr No"
        INNER JOIN jacktest.deputies d
            ON d.deputynumber = CAST(ds."Deputy No" AS INT)
            AND d.clientsource = 'CASRECMIGRATION'
        WHERE da."Foreign" = '1'
    ) t1 WHERE rownum = 1
)
SELECT
    a.id AS address_id,
    od."Case",
    True AS expected,
    a.isairmailrequired AS actual
INTO jacktest.deputy_address_updates_p1
FROM addresses a
INNER JOIN overseas_deputies od
    ON od.id = a.person_id
WHERE (a.isairmailrequired IS NULL OR a.isairmailrequired != True);
-- 543

-- deputies P2
WITH overseas_deputies AS (
    SELECT DISTINCT * FROM (
        SELECT
            d.id,
            ds."Case",
            ds."Deputy No",
            row_number() over (PARTITION BY ds."Case", ds."Deputy No") AS rownum
        FROM casrec_csv_p2.deputy_address da
        INNER JOIN casrec_csv_p2.deputyship ds
            ON ds."Dep Addr No" = da."Dep Addr No"
        INNER JOIN jacktest.deputies d
            ON d.deputynumber = CAST(ds."Deputy No" AS INT)
            AND d.clientsource = 'CASRECMIGRATION_P2'
        WHERE da."Foreign" = '1'
    ) t1 WHERE rownum = 1
)
SELECT
    a.id AS address_id,
    od."Case",
    True AS expected,
    a.isairmailrequired AS actual
INTO jacktest.deputy_address_updates_p2
FROM addresses a
INNER JOIN overseas_deputies od
    ON od.id = a.person_id
WHERE (a.isairmailrequired IS NULL OR a.isairmailrequired != True);
-- 0

-- deputies P3
WITH overseas_deputies AS (
    SELECT DISTINCT * FROM (
        SELECT
            d.id,
            ds."Case",
            ds."Deputy No",
            row_number() over (PARTITION BY ds."Case", ds."Deputy No") AS rownum
        FROM casrec_csv_p3.deputy_address da
        INNER JOIN casrec_csv_p3.deputyship ds
            ON ds."Dep Addr No" = da."Dep Addr No"
        INNER JOIN jacktest.deputies d
            ON d.deputynumber = CAST(ds."Deputy No" AS INT)
            AND d.clientsource = 'CASRECMIGRATION_P3'
        WHERE da."Foreign" = '1'
    ) t1 WHERE rownum = 1
)
SELECT
    a.id AS address_id,
    od."Case",
    True AS expected,
    a.isairmailrequired AS actual
INTO jacktest.deputy_address_updates_p3
FROM addresses a
INNER JOIN overseas_deputies od
    ON od.id = a.person_id
WHERE (a.isairmailrequired IS NULL OR a.isairmailrequired != True);
-- 0

--@audit_tag
-- deputy addresses P1
SELECT a.*
INTO jacktest.deputy_address_audit_p1
FROM addresses a
INNER JOIN jacktest.deputy_address_updates_p1 dau
    ON dau.address_id = a.id;

-- deputy addresses P2
SELECT a.*
INTO jacktest.deputy_address_audit_p2
FROM addresses a
INNER JOIN jacktest.deputy_address_updates_p2 dau
    ON dau.address_id = a.id;

-- deputy addresses P3
SELECT a.*
INTO jacktest.deputy_address_audit_p3
FROM addresses a
INNER JOIN jacktest.deputy_address_updates_p3 dau
    ON dau.address_id = a.id;


--@update_tag
-- deputies P1
UPDATE addresses a
SET isairmailrequired = u.expected
FROM jacktest.deputy_address_updates_p1 u
WHERE u.address_id = a.id;

-- deputies P2
UPDATE addresses a
SET isairmailrequired = u.expected
FROM jacktest.deputy_address_updates_p2 u
WHERE u.address_id = a.id;

-- deputies P3
UPDATE addresses a
SET isairmailrequired = u.expected
FROM jacktest.deputy_address_updates_p3 u
WHERE u.address_id = a.id;


--@validate_tag
-- deputies P1
SELECT COUNT(1) FROM (
    SELECT DISTINCT address_id, expected
    FROM jacktest.deputy_address_updates_p1
    EXCEPT
    SELECT DISTINCT a.id, a.isairmailrequired
    FROM addresses a
    INNER JOIN jacktest.deputy_address_audit_p1 aud
        ON aud.id = a.id
) t1;
-- 540

-- deputies P2
SELECT COUNT(1) FROM (
    SELECT DISTINCT address_id, expected
    FROM jacktest.deputy_address_updates_p2
    EXCEPT
    SELECT DISTINCT a.id, a.isairmailrequired
    FROM addresses a
    INNER JOIN jacktest.deputy_address_audit_p2 aud
        ON aud.id = a.id
) t1;
-- 0

-- deputies P3
SELECT COUNT(1) FROM (
    SELECT address_id, expected
    FROM jacktest.deputy_address_updates_p3
    EXCEPT
    SELECT a.id, a.isairmailrequired
    FROM addresses a
    INNER JOIN jacktest.deputy_address_audit_p3 aud
        ON aud.id = a.id
) t1;
-- 0