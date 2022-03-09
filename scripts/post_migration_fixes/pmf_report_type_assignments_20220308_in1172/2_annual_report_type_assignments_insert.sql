CREATE SCHEMA IF NOT EXISTS pmf_report_type_assignments_20220308_in1172;

CREATE TABLE pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts (
    id SERIAL,
    annualreport_id int NOT NULL,
    reporttype varchar,
    type varchar
);

-- Populate table with data we're going to add
INSERT INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts (annualreport_id, reporttype, type)
SELECT annualreport_id, reporttype, type FROM (

    SELECT
        nextval('annual_report_type_assignments_id_seq') AS id,
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
        END) AS reporttype,
        'pfa' AS type
    FROM (
        SELECT
            arl.id AS annualreport_id,
            c.orderstatus AS orderstatus,
            sll.supervisionlevel AS supervisionlevel,
            sll.assetlevel AS assetlevel,
            row_number() OVER (
                PARTITION BY p.caserecnumber
                ORDER BY arl.reportingperiodenddate DESC
            ) AS rownum
        FROM annual_report_logs arl
        INNER JOIN persons p
        ON arl.client_id = p.id
        INNER JOIN cases c
        ON p.caserecnumber = c.caserecnumber
        LEFT JOIN supervision_level_log sll
        ON c.id = sll.order_id
        WHERE arl.status = 'PENDING'
        AND c.type = 'order'
        AND p.clientsource IN ('CASRECMIGRATION')
    ) AS reports
    WHERE rownum = 1

) insert_wrapper;

-- Populate audit table
SELECT annualreport_id
INTO pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts_audit
FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts;

BEGIN;
    INSERT INTO annual_report_type_assignments (id, annualreport_id, reporttype, type)
    SELECT ins.id, ins.annualreport_id, ins.reporttype, ins.type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts ins;

    -- Validation script (should be 0 rows returned after update is done)
    SELECT ins.id, ins.annualreport_id, ins.reporttype, ins.type
    FROM pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts ins
    EXCEPT
    SELECT arta.id, arta.annualreport_id, arta.reporttype, arta.type
    FROM annual_report_type_assignments arta
    INNER JOIN pmf_report_type_assignments_20220308_in1172.annual_report_type_assignments_inserts_audit au
    ON arta.annualreport_id = au.annualreport_id;

-- Run this if validation is INCORRECT (i.e. 1 or more rows returned)
ROLLBACK;

-- Otherwise run this if validation is CORRECT (i.e. 0 rows returned)
COMMIT;
