DROP TABLE IF EXISTS casrec_csv.exceptions_annual_report_type_assignments;

CREATE TABLE casrec_csv.exceptions_annual_report_type_assignments(
    annualreport_id int,
    reporttype varchar default NULL,
    type varchar default NULL,
    order_id int
);

INSERT INTO casrec_csv.exceptions_annual_report_type_assignments(
    SELECT * FROM (
        -- annual_report_logs we expect to have a type assignment;
        -- this SQL comes direct from the transform
        SELECT
            annualreport_id,
            reporttype,
            (CASE
                WHEN reporttype IN ('OPG102', 'OPG103') THEN 'pfa'
                ELSE '-'
            END) AS type,
            order_id
        FROM (
            SELECT
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
                order_id
            FROM (
                SELECT arl.id AS annualreport_id,
                c.id AS order_id,
                c.orderstatus AS orderstatus,
                row_number() OVER (
                    PARTITION BY p.caserecnumber
                    ORDER BY arl.reportingperiodenddate DESC
                ) AS rownum,
                sll.supervisionlevel AS supervisionlevel,
                sll.assetlevel AS assetlevel
                FROM {target_schema}.annual_report_logs arl
                INNER JOIN {target_schema}.persons p
                ON arl.client_id = p.id
                INNER JOIN {target_schema}.cases c
                ON p.caserecnumber = c.caserecnumber
                LEFT JOIN {target_schema}.supervision_level_log sll
                ON c.id = sll.order_id
                WHERE arl.status = 'PENDING'
                AND c.type = 'order'
                AND p.clientsource = 'CASRECMIGRATION'
            ) AS reports
            WHERE rownum = 1
        ) AS pending_reports

        EXCEPT

        -- annual_report_type_assignments associated with
        -- annual_report_logs we've migrated
        SELECT * FROM (
            SELECT arta.annualreport_id AS annualreport_id, arta.reporttype, arta.type, c.id AS order_id
            FROM {target_schema}.annual_report_logs arl
            INNER JOIN {target_schema}.annual_report_type_assignments arta
            ON arl.id = arta.annualreport_id
            INNER JOIN {target_schema}.persons p
            ON arl.client_id = p.id
            INNER JOIN {target_schema}.cases c
            ON p.caserecnumber = c.caserecnumber
            AND c.type = 'order'
            AND p.clientsource = 'CASRECMIGRATION'
        ) as report_type_assignments
    ) exceptions
);
