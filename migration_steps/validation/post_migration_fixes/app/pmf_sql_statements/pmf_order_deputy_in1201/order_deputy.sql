--@setup_tag
-- NB this reuses casrec_mapping.cases, which is set
-- up for another post-migration script
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

WITH od_updates AS (
    SELECT DISTINCT
        od.id AS od_id,
        od.maincorrespondent AS original_maincorrespondent,
        (CASE WHEN TRIM(ds."Corr") = 'Y' THEN True ELSE False END) AS expected_maincorrespondent
    FROM order_deputy od
    INNER JOIN {casrec_mapping}.cases cmc
    ON od.order_id = cmc.sirius_id
    INNER JOIN {casrec_mapping}.deputyship cmds
    ON od.deputy_id = cmds.sirius_id
    INNER JOIN {casrec_schema}.deputyship ds
    ON cmc."Order No" = ds."Order No"
    AND cmds."Deputy No" = ds."Deputy No"
)
SELECT *
INTO {pmf_schema}.order_deputy_updates
FROM od_updates;

--@audit_tag
SELECT od.*
INTO {pmf_schema}.order_deputy_audit
FROM order_deputy od
INNER JOIN {pmf_schema}.order_deputy_updates u
ON od.id = u.od_id;

--@update_tag
UPDATE order_deputy od
SET maincorrespondent = u.expected_maincorrespondent
FROM {pmf_schema}.order_deputy_updates u
WHERE u.od_id = od.id;

--@validate_tag
SELECT od_id AS id, expected_maincorrespondent AS maincorrespondent
FROM {pmf_schema}.order_deputy_updates
EXCEPT
SELECT id, maincorrespondent
FROM order_deputy;
