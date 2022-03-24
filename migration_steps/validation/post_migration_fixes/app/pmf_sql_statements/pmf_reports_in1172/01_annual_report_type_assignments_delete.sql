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

--@update_tag
DELETE FROM annual_report_type_assignments
WHERE id IN (
    SELECT arta_id FROM {pmf_schema}.arta_deletes
);

--@validate_tag
SELECT arta.id FROM annual_report_type_assignments arta
INNER JOIN {casrec_mapping}.annual_report_type_assignments carta
ON arta.id = carta.sirius_id;
