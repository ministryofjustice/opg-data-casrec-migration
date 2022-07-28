--Purpose: Some hybrid cases don't have any deputies linked to one of the two active orders
-- this script identifies those and copys the order_deputy link(s) from one order onto the other.
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

-- The setup SQL
-- dual_orders, save for audit
SELECT
       p.id AS person_id,
       c1.id AS order_id_hw,
       c2.id AS order_id_pfa
INTO {pmf_schema}.hybrd_cases
FROM persons p
INNER JOIN cases c1 ON c1.client_id = p.id
INNER JOIN cases c2 ON c2.client_id = p.id
WHERE c1.casesubtype = 'hw'
AND c2.casesubtype = 'pfa'
AND c1.orderstatus = 'ACTIVE'
AND c2.orderstatus = 'ACTIVE'
AND p.clientsource LIKE 'CASRECMIGRATION%';
--1674

-- orders missing an order_deputy, save for audit
SELECT *
INTO {pmf_schema}.hybrd_cases_missing_orderdeputy
FROM (
    SELECT DISTINCT
        hyb.person_id AS person_id,
        od_pfa.id AS orderdeputy_id,
        hyb.order_id_hw AS order_id,
        od_pfa.id AS od_pfa_id,
        od_hw.id AS od_hw_id
    FROM {pmf_schema}.hybrd_cases hyb
    LEFT JOIN order_deputy od_hw ON od_hw.order_id = hyb.order_id_hw
    LEFT JOIN order_deputy od_pfa ON od_pfa.order_id = hyb.order_id_pfa
    WHERE od_hw.id IS NULL AND od_pfa.id IS NOT NULL
    UNION ALL
    SELECT DISTINCT
        hyb.person_id AS person_id,
        od_hw.id AS orderdeputy_id,
        hyb.order_id_pfa AS order_id,
        od_pfa.id AS od_pfa_id,
        od_hw.id AS od_hw_id
    FROM {pmf_schema}.hybrd_cases hyb
    LEFT JOIN order_deputy od_hw ON od_hw.order_id = hyb.order_id_hw
    LEFT JOIN order_deputy od_pfa ON od_pfa.order_id = hyb.order_id_pfa
    WHERE od_pfa.id IS NULL
      AND od_hw.id IS NOT NULL
) missing_od;
--2360

-- order_deputies to insert
SELECT
    nextval('order_deputy_id_seq') as order_deputy_id,
    mo.person_id,
    mo.order_id,
    od.deputy_id,
    od.deputytype,
    od.statusoncase,
    od.relationshiptoclient,
    od.relationshipother,
    od.maincorrespondent,
    od.statusoncaseoverride,
    od.statuschangedate,
    od.statusnotes
INTO {pmf_schema}.order_deputy_inserts
FROM {pmf_schema}.hybrd_cases_missing_orderdeputy mo
INNER JOIN order_deputy od ON id = mo.orderdeputy_id;

--@update_tag
INSERT INTO order_deputy (
    order_id,
    deputy_id,
    id,
    deputytype,
    statusoncase,
    relationshiptoclient,
    relationshipother,
    maincorrespondent,
    statusoncaseoverride,
    statuschangedate,
    statusnotes
)
SELECT
    order_id,
    deputy_id,
    order_deputy_id,
    deputytype,
    statusoncase,
    relationshiptoclient,
    relationshipother,
    maincorrespondent,
    statusoncaseoverride,
    statuschangedate,
    statusnotes
FROM {pmf_schema}.order_deputy_inserts;

-- Some checking SQL.. this isn't validation
--@validate_tag
SELECT
    order_id,
    deputy_id,
    order_deputy_id,
    deputytype,
    statusoncase,
    relationshiptoclient,
    relationshipother,
    maincorrespondent,
    statusoncaseoverride,
    statuschangedate,
    statusnotes
FROM {pmf_schema}.order_deputy_inserts
EXCEPT
SELECT
    order_id,
    deputy_id,
    id,
    deputytype,
    statusoncase,
    relationshiptoclient,
    relationshipother,
    maincorrespondent,
    statusoncaseoverride,
    statuschangedate,
    statusnotes
FROM order_deputy;
