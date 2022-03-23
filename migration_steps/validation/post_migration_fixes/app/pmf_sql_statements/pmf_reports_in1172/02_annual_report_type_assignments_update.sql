--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

-- Select data we're going to insert
SELECT *
INTO {pmf_schema}.annual_report_type_assignments_inserts
FROM (

    SELECT
        reports.id AS annualreport_id,
        (CASE
            WHEN reports.casesupervisionlevel = 'GENERAL' THEN 'OPG102'
            WHEN reports.casesupervisionlevel = 'MINIMAL' THEN 'OPG103'
            ELSE NULL
        END) AS reporttype,
        'pfa' AS type
    FROM (
        SELECT arl.id, arl.casesupervisionlevel, arl.status
        FROM {casrec_mapping}.annual_report_logs carl
        INNER JOIN annual_report_logs arl
        ON carl.sirius_id = arl.id
        WHERE arl.status = 'PENDING'
    ) reports

) to_insert;

-- This audit table is populated inside the update transaction, as it
-- stores the actual IDs we're inserting
CREATE TABLE IF NOT EXISTS {pmf_schema}.annual_report_type_assignments_inserts_audit (
    id int PRIMARY KEY,
    annualreport_id int,
    reporttype varchar,
    type varchar
);

--@audit_tag
-- Keep a record of which annual_report_logs should have an
-- annual_report_type_assignments row after insert, i.e. arls we migrated
-- with a status of 'PENDING'
SELECT *
INTO {pmf_schema}.annual_report_type_assignments_inserts_expected
FROM (
    SELECT arl.id, arl.status
    FROM annual_report_logs arl
    INNER JOIN persons p
    ON arl.client_id = p.id
    WHERE p.clientsource = '{client_source}'
    AND arl.status = 'PENDING'
) pending_reports;

--@update_tag
-- Audit table for inserts; these are the inserts we'll actually do, along with their IDs;
-- note this audit table has to be constructed inside the transaction, as we're
-- setting IDs
INSERT INTO {pmf_schema}.annual_report_type_assignments_inserts_audit
SELECT
    nextval('annual_report_type_assignments_id_seq') AS id,
    ins.*
FROM {pmf_schema}.annual_report_type_assignments_inserts ins;

-- The insert uses the audit table, as this has IDs in it
INSERT INTO annual_report_type_assignments (id, annualreport_id, reporttype, type)
SELECT *
FROM {pmf_schema}.annual_report_type_assignments_inserts_audit;

--@validate_tag
-- Have we now got an arta for each arl we expected to, and is there the same
-- number of those artas as the number we actually inserted?
SELECT * FROM (
    SELECT
        (
            SELECT COUNT(1)
            FROM {pmf_schema}.annual_report_type_assignments_inserts_audit
        ) AS casrec_counter,
        (
            SELECT COUNT(1) FROM {pmf_schema}.annual_report_type_assignments_inserts_expected
        ) AS sirius_counter,
        (
            SELECT COUNT(1)
            FROM annual_report_type_assignments arta
            INNER JOIN annual_report_logs arl
            ON arta.annualreport_id = arl.id
            INNER JOIN persons p
            ON arl.client_id = p.id
            WHERE p.clientsource = '{client_source}'
            AND arl.status = 'PENDING'
        ) AS arta_counter
) counted
WHERE casrec_counter != sirius_counter
OR casrec_counter != arta_counter;
