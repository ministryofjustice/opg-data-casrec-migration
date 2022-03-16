CREATE SCHEMA IF NOT EXISTS pmf_report_type_assignments_20220308_in1172;

-- NB this uses a list of reporttypes and types we set on annual_report_type_assignments
-- when we did the migration, stored in casrec_mapping.annual_report_type_assignments;
-- it also uses a list of statuses set on annual_report_logs,
-- stored in casrec_mapping.annual_report_logs

-- record the current number of records in annual_report_type_assignments
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_counts
FROM (SELECT COUNT(id) AS arta_starting_count FROM annual_report_type_assignments) artas;

-- Populate table with data we're going to update
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates
FROM (

    SELECT
        arta_id,
        annualreport_id,
        (CASE
            WHEN supervisionlevel = 'GENERAL' THEN 'OPG102'
            WHEN supervisionlevel = 'MINIMAL' THEN 'OPG103'
            ELSE NULL
        END) AS reporttype,
        type
    FROM (
        SELECT
            arta.id AS arta_id,
            arl.id AS annualreport_id,
            arl.casesupervisionlevel AS supervisionlevel,
            c.casesubtype AS type
        FROM annual_report_type_assignments arta

        -- only include annual_report_type_assignments where
        -- the reporttype and type have not changed since migration
        INNER JOIN casrec_mapping.annual_report_type_assignments carta
        ON arta.id = carta.sirius_id
        AND carta.reporttype = arta.reporttype
        AND carta.type = arta.type

        -- only change annual_report_type_assignments for PENDING reports
        INNER JOIN annual_report_logs arl
        ON arta.annualreport_id = arl.id
        AND arl.status = 'PENDING'

        -- only update annual_report_type_assignments where the status
        -- hasn't changed since the migration
        INNER JOIN casrec_mapping.annual_report_logs carl
        ON arl.id = carl.sirius_id
        AND carl.status = arl.status

        INNER JOIN cases c
        ON arl.order_id = c.id
    ) AS reports

) to_update;

-- Audit table for updates
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates_audit
FROM (
    SELECT * FROM annual_report_type_assignments
    WHERE id IN (
        SELECT arta_id FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates
    )
) updates;

-- Delete the non-PENDING annual_report_type_assignments we incorrectly migrated
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
FROM (

    SELECT arta.id AS arta_id, arl.client_id
    FROM annual_report_type_assignments arta

    -- only include annual_report_type_assignments where
    -- the reporttype and type have not changed since migration
    INNER JOIN casrec_mapping.annual_report_type_assignments carta
    ON arta.id = carta.sirius_id
    AND carta.reporttype = arta.reporttype
    AND carta.type = arta.type

    -- delete type assignments for non-PENDING reports only
    INNER JOIN annual_report_logs arl
    ON arta.annualreport_id = arl.id
    AND arl.status != 'PENDING'

    INNER JOIN persons p
    ON arl.client_id = p.id

    -- only delete annual_report_type_assignments where the status
    -- hasn't changed since the migration
    INNER JOIN casrec_mapping.annual_report_logs carl
    ON arl.id = carl.sirius_id
    AND carl.status = arl.status

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

BEGIN;
    UPDATE annual_report_type_assignments arta
    SET type = up.type, reporttype = up.reporttype
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates up
    WHERE up.arta_id = arta.id AND up.annualreport_id = arta.annualreport_id;

    DELETE FROM annual_report_type_assignments
    WHERE id IN (
        SELECT arta_id FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
    );

    -- Validation: check updates look OK
    SELECT arta_id, annualreport_id, reporttype, type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates
    EXCEPT
    SELECT id, annualreport_id, reporttype, type
    FROM annual_report_type_assignments
    WHERE id IN (
        SELECT id FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes_audit
    );

    -- Validation: check we haven't deleted too many rows, or updated too many
    SELECT
        *,
        ("# arta start" = "# arta current" + "# arta deleted") AS "Deletes OK?"
    FROM (
        SELECT
            (SELECT arta_starting_count FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_counts) AS "# arta start",
            (SELECT COUNT(arta.id) FROM annual_report_type_assignments arta) AS "# arta current",
            (SELECT COUNT(arta_id) FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes) AS "# arta deleted",
            (SELECT COUNT(arta_id) FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates) AS "# arta updated"
    ) counts;

-- Manually run if validation incorrect
ROLLBACK;

-- Manually run if validation correct
COMMIT;
