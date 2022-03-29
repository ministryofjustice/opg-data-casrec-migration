-- Purpose: Update order_deputy.statusoncase to 'CLOSED' if the related
-- order (case in Sirius) has orderstatus = 'CLOSED'.
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

-- Assumptions:
-- 1. Any manual changes since migration can be overwritten by this script.
-- 2. Don't updated order_deputy.statusoncase if it's already 'CLOSED'
-- 3. If order_deputy.statusoncase = 'DECEASED', but cases.orderstatus
--    is 'CLOSED', statusoncase stays as 'DECEASED'.
WITH order_deputy_updates AS (
    SELECT
        od.id,
        od.statusoncase AS original_statusoncase,
        'CLOSED' AS expected_statusoncase
    FROM order_deputy od
    INNER JOIN cases c
    ON od.order_id = c.id
    INNER JOIN persons p
    ON od.deputy_id = p.id
    WHERE p.clientsource = '{client_source}'
    AND c.orderstatus = 'CLOSED'
    AND (
        od.statusoncase IS NULL
        OR
        od.statusoncase NOT IN ('CLOSED', 'DECEASED')
    )
)
SELECT *
INTO {pmf_schema}.order_deputy_updates
FROM order_deputy_updates;

--@audit_tag
SELECT od.*
INTO {pmf_schema}.order_deputy_audit
FROM {pmf_schema}.order_deputy_updates u
INNER JOIN order_deputy od
ON u.id = od.id;

--@update_tag
UPDATE order_deputy od SET statusoncase = u.expected_statusoncase
FROM {pmf_schema}.order_deputy_updates u
WHERE od.id = u.id;

--@validate_tag
SELECT id, expected_statusoncase AS statusoncase
FROM {pmf_schema}.order_deputy_updates
EXCEPT
SELECT id, statusoncase FROM order_deputy;
