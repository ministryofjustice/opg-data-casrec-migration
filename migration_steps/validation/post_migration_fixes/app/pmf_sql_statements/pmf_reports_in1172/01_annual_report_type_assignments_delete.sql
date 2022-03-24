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
INTO {pmf_schema}.arta_deletes_audit
FROM (
    SELECT * FROM annual_report_type_assignments
    WHERE id IN (
        SELECT arta_id FROM {pmf_schema}.arta_deletes
    )
) via_casrec_mapping;

-- annual_report_type_assignments belonging to
-- annual_report_logs we migrated which have 2+ artas;
-- all but one of these will have been added since migration;
-- these shouldn't be an issue as the ones we added have
-- an invalid type '-', so removing them should have no effect
SELECT *
INTO {pmf_schema}.arta_migrated_arls_with_multiple_artas_audit
FROM (
    SELECT arta.*, carta.sirius_id AS casrec_mapping_sirius_id
    FROM annual_report_type_assignments arta
    LEFT JOIN {casrec_mapping}.annual_report_type_assignments carta
    ON arta.id = carta.sirius_id
    WHERE arta.annualreport_id IN (
        SELECT arl.id
        FROM annual_report_logs arl
        INNER JOIN {casrec_mapping}.annual_report_logs carl
        ON arl.id = carl.sirius_id
        INNER JOIN annual_report_type_assignments arta
        ON arl.id = arta.annualreport_id
        GROUP BY arl.id
        HAVING count(arta.*) > 1
    )
) AS migrated_arls_with_multiple_artas;

--@update_tag
DELETE FROM annual_report_type_assignments
WHERE id IN (
    SELECT arta_id FROM {pmf_schema}.arta_deletes
);

--@validate_tag
SELECT arta.id FROM annual_report_type_assignments arta
INNER JOIN {casrec_mapping}.annual_report_type_assignments carta
ON arta.id = carta.sirius_id;
