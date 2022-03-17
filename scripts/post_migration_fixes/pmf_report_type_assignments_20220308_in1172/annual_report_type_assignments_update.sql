CREATE SCHEMA IF NOT EXISTS pmf_report_type_assignments_20220308_in1172;

-- NB this uses a list of reporttypes and types we set on annual_report_type_assignments
-- when we did the migration, stored in casrec_mapping.annual_report_type_assignments;
-- it also uses a list of statuses set on annual_report_logs,
-- stored in casrec_mapping.annual_report_logs

-- record the current number of records in annual_report_type_assignments
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_counts
FROM (SELECT COUNT(1) AS arta_starting_count FROM annual_report_type_assignments) artas;

-- Delete all of the annual_report_type_assignments we incorrectly migrated;
-- we ignore whether they have been updated since the migration
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
FROM (

    SELECT arta.id AS arta_id
    FROM annual_report_type_assignments arta

    INNER JOIN casrec_mapping.annual_report_type_assignments carta
    ON arta.id = carta.sirius_id

) to_delete;

-- Audit table for deletes
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes_audit
FROM (
    SELECT * FROM annual_report_type_assignments
    WHERE id IN (
        SELECT arta_id FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
    )
) deletes;

-- Populate table with data we're going to insert;
-- no audit table for this, as the inserts table *is* the audit table
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts
FROM (

    SELECT
        nextval('annual_report_type_assignments_id_seq') AS id,
        reports.id AS annualreport_id,
        (CASE
            WHEN reports.casesupervisionlevel = 'GENERAL' THEN 'OPG102'
            WHEN reports.casesupervisionlevel = 'MINIMAL' THEN 'OPG103'
            ELSE NULL
        END) AS reporttype,
        'pfa' AS type
    FROM (
        SELECT arl.id, arl.casesupervisionlevel, arl.status
        FROM casrec_mapping.annual_report_logs carl
        INNER JOIN annual_report_logs arl
        ON carl.sirius_id = arl.id
    ) reports
    WHERE reports.status = 'PENDING'

) to_insert;

BEGIN;
    DELETE FROM annual_report_type_assignments
    WHERE id IN (
        SELECT arta_id FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
    );

    INSERT INTO annual_report_type_assignments (id, annualreport_id, reporttype, type)
    SELECT ins.id, ins.annualreport_id, ins.reporttype, ins.type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts ins
    -- only add a row if the arl row doesn't already have an arta row
    LEFT JOIN annual_report_type_assignments arta
    ON ins.annualreport_id = arta.annualreport_id
    WHERE arta.id IS NULL;

    -- Validation
    SELECT
        *,
        ("# arta start" - "# arta deleted" + "# arta inserted" = "# arta current") AS "OK?"
    FROM (
        SELECT
            (SELECT arta_starting_count FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_counts) AS "# arta start",
            (SELECT COUNT(1) FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes) AS "# arta deleted",
            (
                SELECT COUNT(1) FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts ins
                INNER JOIN annual_report_type_assignments arta
                ON ins.id = arta.id
            ) AS "# arta inserted",
            (SELECT COUNT(1) FROM annual_report_type_assignments arta) AS "# arta current"
    ) counts;

-- Manually run if validation incorrect
ROLLBACK;

-- Manually run if validation correct
COMMIT;
