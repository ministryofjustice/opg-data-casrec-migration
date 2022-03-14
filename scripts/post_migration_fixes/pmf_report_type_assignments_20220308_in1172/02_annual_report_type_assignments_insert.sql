CREATE SCHEMA IF NOT EXISTS pmf_report_type_assignments_20220308_in1172;

-- Populate table with data we're going to add
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts
FROM (

    SELECT
        nextval('annual_report_type_assignments_id_seq') AS id,
        annualreport_id,
        (CASE
            WHEN supervisionlevel = 'GENERAL' THEN 'OPG102'
            WHEN supervisionlevel = 'MINIMAL' THEN 'OPG103'
            ELSE NULL
        END) AS reporttype,
        'pfa' AS type
    FROM (
        SELECT
            arl.id AS annualreport_id,
            arl.casesupervisionlevel AS supervisionlevel
        FROM annual_report_logs arl
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
    INSERT INTO annual_report_type_assignments (id, annualreport_id, reporttype, type)
    SELECT id, annualreport_id, reporttype, type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts;

    -- Validation
    SELECT annualreport_id, reporttype, type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts
    EXCEPT
    SELECT annualreport_id, reporttype, type
    FROM annual_report_type_assignments;

-- Manually run if validation incorrect
ROLLBACK;

-- Manually run if validation correct
COMMIT;
