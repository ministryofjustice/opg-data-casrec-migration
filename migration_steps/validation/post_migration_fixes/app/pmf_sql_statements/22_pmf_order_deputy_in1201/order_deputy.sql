--@setup_tag
-- NB this reuses casrec_mapping.cases, which is set
-- up for another post-migration script
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

DROP TABLE IF EXISTS {pmf_schema}.deputies;
SELECT id, deputynumber, clientsource
INTO {pmf_schema}.deputies
FROM persons
WHERE type = 'actor_deputy'
AND (clientsource = '{client_source}' OR clientsource IS NULL);
CREATE INDEX idx_pmf1201_deputies_id ON {pmf_schema}.deputies USING btree (id);
CREATE INDEX idx_pmf1201_deputies_deputynumber ON {pmf_schema}.deputies USING btree (deputynumber);
-- END OF HELPER TABLES

WITH od_updates AS (
    SELECT DISTINCT
        od.id AS order_deputy_id,
        deputy_mapping.clientsource,
        od.maincorrespondent AS maincorrespondent,
        (CASE WHEN TRIM(ds."Corr") = 'Y' THEN True ELSE False END) AS expected_maincorrespondent
    FROM {casrec_schema}.deputyship ds
    INNER JOIN {casrec_mapping}.cases cmc
        ON cmc."Order No" = ds."Order No"
    INNER JOIN {pmf_schema}.deputies deputy_mapping
        ON deputy_mapping.deputynumber = CAST(ds."Deputy No" AS INT)
    LEFT JOIN order_deputy od
        ON od.order_id = cmc.sirius_id
        AND od.deputy_id = deputy_mapping.id
    WHERE od.id IS NOT NULL
    AND deputy_mapping.clientsource = '{client_source}'
)
SELECT *
INTO {pmf_schema}.order_deputy_updates
FROM od_updates;

-- Delete rows that don't change (simpler to do this than add even more complexity to above query)
DELETE FROM {pmf_schema}.order_deputy_updates
WHERE maincorrespondent IS NOT NULL
AND maincorrespondent = expected_maincorrespondent;

--@audit_tag
SELECT od.*
INTO {pmf_schema}.order_deputy_audit
FROM order_deputy od
INNER JOIN {pmf_schema}.order_deputy_updates u
ON od.id = u.order_deputy_id;

--@update_tag
UPDATE order_deputy od
SET maincorrespondent = u.expected_maincorrespondent
FROM {pmf_schema}.order_deputy_updates u
WHERE u.order_deputy_id = od.id;

--@validate_tag
SELECT order_deputy_id AS id, expected_maincorrespondent AS maincorrespondent
FROM {pmf_schema}.order_deputy_updates
EXCEPT
SELECT id, maincorrespondent
FROM order_deputy;
