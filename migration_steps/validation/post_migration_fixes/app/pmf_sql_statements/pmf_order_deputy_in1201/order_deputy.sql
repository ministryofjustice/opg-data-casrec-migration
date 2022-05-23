--@setup_tag
-- NB this reuses casrec_mapping.cases, which is set
-- up for another post-migration script
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

-- NOTE - HELPER TABLES IN SETUP ARE VALID FOR BOTH MIGRATION PHASES
-- START OF HELPER TABLES

CREATE TABLE IF NOT EXISTS {pmf_schema}.split_deputies_final (
    caserecnumber varchar,
    original_deputy_name varchar,
    original_deputy_number int,
    new_deputy_name varchar,
    organisation_deputy varchar,
    split_deputy_ecm varchar,
    add1 varchar,
    add2 varchar,
    add3 varchar,
    city_town varchar,
    county varchar,
    postcode varchar,
    country varchar,
    tel_day varchar,
    tel_mobile varchar,
    tel_evening varchar,
    email varchar
);
\copy {pmf_schema}.split_deputies_final FROM 'IN1201_split_deputies_final.csv' CSV HEADER;
-- file source: https://opgtransform.atlassian.net/browse/SW-5461

CREATE TABLE IF NOT EXISTS {pmf_schema}.new_deputies (
    deputy_number int,
    deputy_name varchar,
    city_town varchar
);
\copy {pmf_schema}.new_deputies FROM 'IN1201_new_deputies.csv' CSV HEADER;
-- file source: s3://async-upload.casrecdmpq.eu-west-1.sirius.opg.justice.gov.uk/post-migration-files/new_deputies.csv

-- make a mapping table from the two imported documents
DROP TABLE IF EXISTS {pmf_schema}.changed_deputies;
SELECT DISTINCT caserecnumber, deputy_number, COALESCE(non_org_deputy_id, org_deputy_id) AS new_deputy_id
INTO {pmf_schema}.changed_deputies
FROM (
    SELECT
    sd.caserecnumber,
    sd.original_deputy_number deputy_number,
    CONCAT(sd.original_deputy_name,' ',sd.city_town),
    sd.new_deputy_name,
    nd_non_orgs.deputy_id AS non_org_deputy_id,
    nd_orgs.deputy_id AS org_deputy_id
    FROM {pmf_schema}.split_deputies_final sd
    LEFT JOIN (
        SELECT DISTINCT
        replace(CONCAT(p.firstname,' ',p.othernames,' ',p.surname,' ',nd.city_town), '  ', ' ') AS join_name,
        p.id AS deputy_id
        FROM {pmf_schema}.new_deputies nd
        LEFT JOIN {pmf_schema}.deputies deputy_mapping
            ON deputy_mapping.deputynumber = nd.deputy_number
        LEFT JOIN persons p
            ON p.id = deputy_mapping.id
        WHERE deputy_mapping.clientsource IS NULL
    ) nd_non_orgs
        ON nd_non_orgs.join_name = CONCAT(sd.original_deputy_name,' ',sd.city_town)
    LEFT JOIN (
        SELECT DISTINCT
        nd.deputy_name AS join_name,
        deputy_mapping.id AS deputy_id
        FROM {pmf_schema}.new_deputies nd
        LEFT JOIN {pmf_schema}.deputies deputy_mapping
            ON deputy_mapping.deputynumber = nd.deputy_number
        WHERE deputy_mapping.clientsource IS NULL
    ) nd_orgs
        ON nd_orgs.join_name = sd.new_deputy_name
) t1;

DROP TABLE IF EXISTS {pmf_schema}.deputies;
SELECT id, deputynumber, clientsource
INTO {pmf_schema}.deputies
FROM persons
WHERE type = 'actor_deputy'
AND (clientsource LIKE 'CASRECMIGRATION%' OR clientsource IS NULL);
CREATE INDEX idx_pmf1201_deputies_id ON {pmf_schema}.deputies USING btree (id);
CREATE INDEX idx_pmf1201_deputies_deputynumber ON {pmf_schema}.deputies USING btree (deputynumber);

-- END OF HELPER TABLES

WITH od_updates AS (
    SELECT DISTINCT
        order_deputy_id,
        maincorrespondent,
        expected_maincorrespondent
    FROM (
        SELECT DISTINCT
            ds."Deputy No",
            ds."Order No",
            ds."Case",
            cmc.sirius_id order_id,
            deputy_mapping.id deputy_id_original,
            COALESCE(od2.id, od.id) AS order_deputy_id,
            COALESCE(od2.maincorrespondent, od.maincorrespondent) AS maincorrespondent,
            (CASE WHEN TRIM(ds."Corr") = 'Y' THEN True ELSE False END) AS expected_maincorrespondent
        FROM {casrec_schema}.deputyship ds
        INNER JOIN {casrec_mapping}.cases cmc
            ON cmc."Order No" = ds."Order No"
        INNER JOIN {pmf_schema}.deputies deputy_mapping
            ON deputy_mapping.deputynumber = CAST(ds."Deputy No" AS INT)
        LEFT JOIN {pmf_schema}.changed_deputies
            ON changed_deputies.caserecnumber = ds."Case"
            AND changed_deputies.deputy_number = deputy_mapping.deputynumber
        LEFT JOIN order_deputy od
            ON od.order_id = cmc.sirius_id
            AND od.deputy_id = deputy_mapping.id
        LEFT JOIN order_deputy od2
            ON od2.order_id = cmc.sirius_id
            AND od2.deputy_id = changed_deputies.new_deputy_id
        WHERE od.id IS NOT NULL OR od2.id IS NOT NULL
        AND deputy_mapping.clientsource = '{client_source}'
    ) t1
)
SELECT *
INTO {pmf_schema}.order_deputy_updates
FROM od_updates;

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
WHERE u.od_id = od.id;

--@validate_tag
SELECT od_id AS id, expected_maincorrespondent AS maincorrespondent
FROM {pmf_schema}.order_deputy_updates
EXCEPT
SELECT id, maincorrespondent
FROM order_deputy;
