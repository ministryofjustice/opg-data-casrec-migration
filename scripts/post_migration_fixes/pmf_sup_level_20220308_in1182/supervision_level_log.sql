CREATE SCHEMA IF NOT EXISTS pmf_sup_level_20220308_in1182;

-- DROP TABLE IF EXISTS pmf_sup_level_20220308_in1182.supervision_level_log_audit;
-- DROP TABLE IF EXISTS pmf_sup_level_20220308_in1182.supervision_level_log_keep;
-- DROP TABLE IF EXISTS pmf_sup_level_20220308_in1182.supervision_level_log_deletes;
-- DROP TABLE IF EXISTS pmf_sup_level_20220308_in1182.supervision_level_log_inserts;

SET datestyle = "ISO, DMY";

SELECT sll.*
INTO pmf_sup_level_20220308_in1182.supervision_level_log_audit
FROM supervision_level_log sll
INNER JOIN cases c ON c.id = sll.order_id
INNER JOIN persons p ON p.id = c.client_id
WHERE p.clientsource = 'CASRECMIGRATION';

WITH migrated_sup_levels AS (
    SELECT sll.*
    FROM supervision_level_log sll
    INNER JOIN cases c ON c.id = sll.order_id
    INNER JOIN persons p ON p.id = c.client_id
    WHERE p.clientsource = 'CASRECMIGRATION'
)
SELECT *
INTO pmf_sup_level_20220308_in1182.supervision_level_log_keep
FROM (
    SELECT msl.*
    FROM migrated_sup_levels msl
    WHERE msl.appliesfrom <> '2022-03-05'::date
       OR msl.createddate <> '2022-03-05'::timestamp(0)
       OR msl.notes <> 'placeholder note'
    UNION
    SELECT id, order_id, appliesfrom, createddate, supervisionlevel, notes, assetlevel
    FROM (
        SELECT *, ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_id, id) as row_number
        FROM migrated_sup_levels
    ) numbered_logs
    WHERE numbered_logs.row_number <> 1
) logs;

SELECT audit.*
INTO pmf_sup_level_20220308_in1182.supervision_level_log_deletes
FROM pmf_sup_level_20220308_in1182.supervision_level_log_audit audit
LEFT JOIN pmf_sup_level_20220308_in1182.supervision_level_log_keep keep ON audit.id = keep.id
WHERE keep.id IS NULL;

WITH casrec_supervision_levels AS (
    SELECT a.*, ROW_NUMBER() OVER (ORDER BY a."Order No", a."Start Date"::date) AS row_number
    FROM (
        SELECT DISTINCT ON ("Order No", "Start Date"::date)
               "Order No",
               "Start Date",
               "Date Create",
               "Asmt Lvl"
        FROM casrec_csv.risk_assessment
        WHERE "Start Date" <> ''
          AND "Asmt Lvl" <> ''
        ORDER BY "Order No", "Start Date"::date, COALESCE(NULLIF("Date Create", ''), "Start Date")::date DESC
    ) a
)
SELECT c.id as order_id,
       csl1."Start Date"::date as appliesfrom,
       COALESCE(NULLIF(csl1."Date Create", ''), csl1."Start Date")::date as createddate,
       CASE WHEN csl1."Asmt Lvl" = '3' THEN 'MINIMAL' ELSE 'GENERAL' END as supervisionlevel,
       CASE WHEN csl1."Asmt Lvl" = '3' THEN 'LOW' ELSE 'HIGH' END as assetlevel,
       'Migrated from Casrec' as notes
INTO pmf_sup_level_20220308_in1182.supervision_level_log_inserts
FROM casrec_supervision_levels csl1
LEFT JOIN casrec_supervision_levels csl2
    ON csl1.row_number = csl2.row_number + 1 AND csl1."Order No" = csl2."Order No"
INNER JOIN casrec_mapping.cases cmc ON cmc."Order No" = csl1."Order No"
INNER JOIN cases c ON c.id = cmc.sirius_id
WHERE csl1."Asmt Lvl" <> csl2."Asmt Lvl" or csl2."Asmt Lvl" is null
ORDER BY csl1.row_number;

BEGIN;
    DELETE FROM supervision_level_log sll
    USING pmf_sup_level_20220308_in1182.supervision_level_log_deletes del
    WHERE sll.id = del.id;

    INSERT INTO supervision_level_log (id, order_id, appliesfrom, createddate, supervisionlevel, notes, assetlevel)
    SELECT nextval('supervision_level_log_id_seq'), slli.order_id, slli.appliesfrom, slli.createddate, slli.supervisionlevel, slli.notes, slli.assetlevel
    FROM pmf_sup_level_20220308_in1182.supervision_level_log_inserts slli;
-- Run if counts incorrect
ROLLBACK;
-- Run if counts correct
COMMIT;

-- Validation script (should be 0)
WITH sirius_side AS (
    SELECT sll.order_id, sll.appliesfrom, sll.createddate, sll.supervisionlevel, sll.notes, sll.assetlevel
    FROM supervision_level_log sll
    INNER JOIN cases c ON c.id = sll.order_id
    INNER JOIN persons p ON p.id = c.client_id
    WHERE p.clientsource = 'CASRECMIGRATION'
),
casrec_side AS (
    SELECT order_id, appliesfrom, createddate, supervisionlevel, notes, assetlevel
    FROM pmf_sup_level_20220308_in1182.supervision_level_log_inserts
),
not_deleted AS (
    SELECT order_id, appliesfrom, createddate, supervisionlevel, notes, assetlevel
    FROM pmf_sup_level_20220308_in1182.supervision_level_log_keep
)
SELECT 'not in Sirius' as validation, * FROM (
    SELECT * FROM casrec_side
    EXCEPT
    SELECT * FROM sirius_side
) validation1
UNION
SELECT 'not in Casrec' as validation, * FROM (
    SELECT * FROM sirius_side
    EXCEPT
    SELECT * FROM casrec_side
    EXCEPT
    SELECT * FROM not_deleted
) validation2
UNION
SELECT 'erroneously deleted' as validation, * FROM (
    SELECT * FROM not_deleted
    EXCEPT
    SELECT * FROM sirius_side
) validation3;
