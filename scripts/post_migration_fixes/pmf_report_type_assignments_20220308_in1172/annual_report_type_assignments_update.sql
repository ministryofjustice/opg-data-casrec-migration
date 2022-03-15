CREATE SCHEMA IF NOT EXISTS pmf_report_type_assignments_20220308_in1172;

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
        INNER JOIN annual_report_logs arl
        ON arta.annualreport_id = arl.id
        INNER JOIN persons p
        ON arl.client_id = p.id
        INNER JOIN cases c
        ON c.client_id = p.id
        WHERE arl.status = 'PENDING'
        AND c.type = 'order'
        AND c.orderstatus = 'ACTIVE'
        AND p.clientsource IN ('CASRECMIGRATION')
    ) AS reports

) to_update;

BEGIN;
    UPDATE annual_report_type_assignments arta
    SET type = up.type, reporttype = up.reporttype
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates up
    WHERE up.arta_id = arta.id AND up.annualreport_id = arta.annualreport_id;

    -- Validation
    SELECT arta_id, annualreport_id, reporttype, type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates
    EXCEPT
    SELECT id, annualreport_id, reporttype, type
    FROM annual_report_type_assignments;

-- Manually run if validation incorrect
ROLLBACK;

-- Manually run if validation correct
COMMIT;
