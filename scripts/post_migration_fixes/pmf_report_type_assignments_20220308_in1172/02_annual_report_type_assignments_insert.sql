CREATE SCHEMA IF NOT EXISTS pmf_report_type_assignments_20220308_in1172;

-- Populate table with data we're going to add
SELECT *
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates
FROM (

    SELECT
        nextval(),
        annualreport_id,
        (CASE
            WHEN
                orderstatus = 'ACTIVE' AND supervisionlevel = 'GENERAL'
            THEN
                CASE
                    WHEN assetlevel IN ('HIGH', 'UNKNOWN') THEN 'OPG102'
                    WHEN assetlevel = 'LOW' THEN 'OPG103'
                    ELSE NULL
                END
            ELSE
                NULL
        END) AS expected_reporttype,
        type AS original_type,
        'pfa' AS expected_type
    FROM (
        SELECT
            arl.id AS annualreport_id,
            c.id AS order_id,
            c.orderstatus AS orderstatus,
            arl.reportingperiodenddate,
            sll.appliesfrom,
            row_number() OVER (
                PARTITION BY p.caserecnumber
                ORDER BY arl.reportingperiodenddate DESC, sll.appliesfrom DESC
            ) AS rownum,
            sll.supervisionlevel AS supervisionlevel,
            sll.assetlevel AS assetlevel
        FROM annual_report_logs arl
        INNER JOIN persons p
        ON arl.client_id = p.id
        INNER JOIN cases c
        ON c.client_id = p.id
        LEFT JOIN supervision_level_log sll
        ON sll.order_id = c.id
        WHERE arl.status = 'PENDING'
        AND c.type = 'order'
        AND p.clientsource IN ('CASRECMIGRATION')
    ) AS reports
    WHERE rownum = 1

) to_update;

-- Populate audit table
SELECT arta.*
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates_audit
FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates up
INNER JOIN annual_report_type_assignments arta
ON up.annual_report_type_assignments_id = arta.id;

BEGIN;
    UPDATE annual_report_type_assignments
    SET reporttype = up.expected_reporttype, type = up.expected_type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates up
    WHERE id = up.annual_report_type_assignments_id;

    -- Validation script (should be 0 rows returned after update is done)
    SELECT annual_report_type_assignments_id, expected_reporttype, expected_type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates up
    EXCEPT
    SELECT arta.id, arta.reporttype, arta.type
    FROM annual_report_type_assignments arta
    INNER JOIN pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_updates_audit au
    ON arta.id = au.id;

-- Manually run if counts incorrect
ROLLBACK;

-- Manually run if counts correct
COMMIT;
