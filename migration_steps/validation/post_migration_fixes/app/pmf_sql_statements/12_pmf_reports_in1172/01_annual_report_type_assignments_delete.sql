--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

-- Select for delete: all of the annual_report_type_assignments
-- we incorrectly migrated; we ignore whether they have been updated
-- since the migration
SELECT *
INTO {pmf_schema}.arta_deletes
FROM (

    SELECT arta.id AS arta_id
    FROM annual_report_type_assignments arta

    INNER JOIN {casrec_mapping}.annual_report_type_assignments carta
    ON arta.id = carta.sirius_id

) to_delete;

--@audit_tag
-- Records we are planning to delete
SELECT *
INTO {pmf_schema}.arta_deletes_audit_via_casrec_mapping
FROM (
    SELECT * FROM annual_report_type_assignments
    WHERE id IN (
        SELECT arta_id FROM {pmf_schema}.arta_deletes
    )
) via_casrec_mapping;

-- Manually find all arta rows we added during migration (ignoring the mapping
-- table and going directly from annual_report_logs)
SELECT *
INTO {pmf_schema}.arta_deletes_audit_via_sirius
FROM (
    SELECT arta.id
    FROM annual_report_type_assignments arta
    INNER JOIN annual_report_logs arl
    ON arta.annualreport_id = arl.id
    INNER JOIN persons p
    ON arl.client_id = p.id
    WHERE p.clientsource = '{client_source}'
) via_sirius;

--@update_tag
DELETE FROM annual_report_type_assignments
WHERE id IN (
    SELECT arta_id FROM {pmf_schema}.arta_deletes
);

--@validate_tag
-- Ensure that we have the same number in the
-- deletes_from_casrec_mapping_audit table, and the
-- deletes_from_sirius table, and that there are no
-- arta rows left from the migration
SELECT *
FROM (
    SELECT
        (
            SELECT COUNT(1)
            FROM {pmf_schema}.arta_deletes_audit_via_casrec_mapping
        ) AS "# deletes via casrec_mapping",
        (
            SELECT COUNT(1)
            FROM {pmf_schema}.arta_deletes_audit_via_sirius
        ) AS "# deletes via Sirius",
        (
            SELECT COUNT(1)
            FROM annual_report_type_assignments arta
            INNER JOIN annual_report_logs arl
            ON arta.annualreport_id = arl.id
            INNER JOIN persons p
            ON arl.client_id = p.id
            WHERE p.clientsource = '{client_source}'
        ) AS "# remaining migrated arta rows"
) counted
WHERE "# deletes via casrec_mapping" != "# deletes via Sirius"
OR "# remaining migrated arta rows" > 0;
