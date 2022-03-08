CREATE SCHEMA IF NOT EXISTS pmf_report_type_assignments_20220308_in1172;

-- What we're going to delete
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
FROM (
    SELECT arta.id AS annual_report_type_assignments_id
    FROM annual_report_type_assignments arta
    INNER JOIN annual_report_logs arl
    ON arta.annualreport_id = arl.id
    INNER JOIN persons p
    ON arl.client_id = p.id
    WHERE arl.status != 'PENDING'
    AND p.clientsource IN ('CASRECMIGRATION')
) to_delete;

-- Count current arta table and proposed deletes table
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes_audit
FROM (
    SELECT
        COUNT(arta.*) AS arta_original_count,
        COUNT(arta.*) - (
            SELECT COUNT(*) FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
        ) AS arta_expected_count,
        (
            SELECT COUNT(*) FROM annual_report_logs arl
            INNER JOIN persons p
            ON arl.client_id = p.id
            WHERE arl.status = 'PENDING'
            AND p.clientsource IN ('CASRECMIGRATION')
        ) AS arl_pending_reports
        FROM annual_report_type_assignments arta
) counts;

BEGIN;
    -- Delete inside a transaction
    DELETE FROM annual_report_type_assignments
    WHERE id IN (
        SELECT annual_report_type_assignments_id
        FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes
    );

    -- Validation: check we've only removed the rows we should have
    -- (good if "Expected arta count" == "Actual arta count" == "Number of migrated PENDING reports")
    SELECT
        arta_original_count AS "Original arta count",
        arl_pending_reports AS "Number of migrated PENDING reports",
        arta_expected_count AS "Expected arta count",
        (SELECT COUNT(arta.*) FROM annual_report_type_assignments arta) AS "Actual arta count"
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_deletes_audit;

-- Manually run if counts incorrect
ROLLBACK;

-- Manually run if counts correct
COMMIT;