CREATE SCHEMA IF NOT EXISTS pmf_report_type_assignments_20220308_in1172;

-- What we're going to delete; this is all the annual_report_type_assignments
-- associated with migrated persons, minus the ones we've updated
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
FROM (
    -- All records added during migration
    SELECT arta.id AS annual_report_type_assignments_id
    FROM annual_report_type_assignments arta
    INNER JOIN annual_report_logs arl
    ON arta.annualreport_id = arl.id
    INNER JOIN persons p
    ON arl.client_id = p.id
    WHERE p.clientsource IN ('CASRECMIGRATION')
) to_delete;

-- Count current arta table and proposed deletes table
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes_audit_counts
FROM (
    SELECT
        COUNT(*) AS arta_original_count,
        COUNT(*) - (
            SELECT COUNT(*) FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
        ) AS arta_expected_count
        FROM annual_report_type_assignments
) counts;

-- Keep a record of deleted report types
SELECT arta.*
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes_audit
FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes del
INNER JOIN annual_report_type_assignments arta
ON del.annual_report_type_assignments_id = arta.id;

BEGIN;
    -- Delete inside a transaction
    DELETE FROM annual_report_type_assignments
    WHERE id IN (
        SELECT annual_report_type_assignments_id
        FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
    );

    -- Validation: check we've only removed the rows we should have
    -- (good if "Expected arta count" == "Current arta count"
    -- and "Current arta count + Deleted count" == "Original arta count")
    SELECT
        deleted_count AS "Deleted count",
        arta_current_count + deleted_count AS "Current arta count + Deleted count",
        arta_original_count AS "Original arta count",
        arta_expected_count AS "Expected arta count",
        arta_current_count AS "Current arta count",
        arta_expected_count = arta_current_count AS "All good?"
    FROM (
        SELECT
            arta_expected_count,
            arta_original_count,
            (SELECT COUNT(*) FROM annual_report_type_assignments) AS arta_current_count,
            (
                SELECT COUNT(*)
                FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes_audit
            ) AS deleted_count
        FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes_audit_counts
    ) stats;

-- Manually run if counts incorrect
ROLLBACK;

-- Manually run if counts correct
COMMIT;