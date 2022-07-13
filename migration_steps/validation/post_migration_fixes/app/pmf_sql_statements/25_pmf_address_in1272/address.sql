--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

-- create a worker deputy table as the persons table is too large/slow
SELECT id, deputynumber, clientsource
INTO {pmf_schema}.deputies
FROM persons
WHERE type = 'actor_deputy'
AND clientsource LIKE '{client_source}';
CREATE INDEX idx_pmf1272_deputies_id ON {pmf_schema}.deputies USING btree (id);
CREATE INDEX idx_pmf1272_deputies_deputynumber ON {pmf_schema}.deputies USING btree (deputynumber);

-- client addresses
WITH clients AS (
    SELECT a.id AS address_id, "Case" AS caserecnumber, True AS expected, a.isairmailrequired AS actual
    FROM {casrec_schema}.pat
    LEFT JOIN persons p
        ON p.caserecnumber = pat."Case"
    LEFT JOIN addresses a
        ON a.person_id = p.id
    WHERE p.type = 'actor_client'
    AND clientsource = '{client_source}'
    AND pat."Foreign" = '1'
    AND (a.isairmailrequired IS NULL OR a.isairmailrequired != True)
)
SELECT *
INTO {pmf_schema}.client_address_updates
FROM clients;
-- ~100

-- deputy addresses
WITH overseas_deputies AS (
    SELECT DISTINCT * FROM (
        SELECT
            d.id,
            ds."Case",
            ds."Deputy No",
            row_number() over (PARTITION BY ds."Case", ds."Deputy No") AS rownum
        FROM {casrec_schema}.deputy_address da
        INNER JOIN {casrec_schema}.deputyship ds
            ON ds."Dep Addr No" = da."Dep Addr No"
        INNER JOIN {pmf_schema}.deputies d
            ON d.deputynumber = CAST(ds."Deputy No" AS INT)
            AND d.clientsource = '{client_source}'
        WHERE da."Foreign" = '1'
    ) t1 WHERE rownum = 1
)
SELECT
    a.id AS address_id,
    od."Case",
    True AS expected,
    a.isairmailrequired AS actual
INTO  {pmf_schema}.deputy_address_updates
FROM addresses a
INNER JOIN overseas_deputies od
    ON od.id = a.person_id
WHERE (a.isairmailrequired IS NULL OR a.isairmailrequired != True);
-- 543


--@audit_tag
-- client addresses
SELECT a.*
INTO {pmf_schema}.client_address_audit
FROM addresses a
INNER JOIN {pmf_schema}.client_address_updates cli
    ON cli.address_id = a.id;

-- deputy addresses
SELECT a.*
INTO {pmf_schema}.deputy_address_audit
FROM addresses a
INNER JOIN {pmf_schema}.deputy_address_updates dau
    ON dau.address_id = a.id;


--@update_tag
-- client addresses
UPDATE addresses a
SET isairmailrequired = u.expected
FROM {pmf_schema}.client_address_updates u
WHERE u.address_id = a.id;

-- deputy addresses
UPDATE addresses a
SET isairmailrequired = u.expected
FROM {pmf_schema}.deputy_address_updates u
WHERE u.address_id = a.id;


--@validate_tag
-- client addresses
SELECT COUNT (1) FROM (
    SELECT address_id, expected
    FROM {pmf_schema}.client_address_updates
    EXCEPT
    SELECT a.id, a.isairmailrequired
    FROM addresses a
    INNER JOIN {pmf_schema}.client_address_audit aud
        ON aud.id = a.id
) t1;
-- 100

-- deputy addresses
SELECT COUNT(1) FROM (
    SELECT DISTINCT address_id, expected
    FROM {pmf_schema}.deputy_address_updates
    EXCEPT
    SELECT DISTINCT a.id, a.isairmailrequired
    FROM addresses a
    INNER JOIN {pmf_schema}.deputy_address_audit aud
        ON aud.id = a.id
) t1;
-- 540