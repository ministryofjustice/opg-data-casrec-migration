-- annual_report_type_assignments
-- very basic validation to check we have a type assignment for each report,
-- and that reporttype is set to NULL or a valid value;
-- this doesn't apply the logic to work out what the reporttype should be,
-- just checks that it is one of a known set of values

DROP TABLE IF EXISTS casrec_csv.exceptions_annual_report_type_assignments;

CREATE TABLE casrec_csv.exceptions_annual_report_type_assignments(
    annual_report_logs_id int,
    type varchar,
    reporttype_is_set bool
);

INSERT INTO casrec_csv.exceptions_annual_report_type_assignments(
    SELECT
        arl.id AS annual_report_logs_id,
        'pfa' AS type,
        true AS reporttype_is_set
    FROM {target_schema}.annual_report_logs arl

    EXCEPT

    SELECT
        arta.annualreport_id AS annual_report_logs_id,
        arta.type AS type,
        (arta.reporttype IN ('OPG102', 'OPG103') OR arta.reporttype IS NULL) AS reporttype_is_set
    FROM {target_schema}.annual_report_type_assignments arta
);
