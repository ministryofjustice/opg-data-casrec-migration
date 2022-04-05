-- contains all orders != status of open
DROP TABLE IF EXISTS {count_schema}.casrec_orders;
CREATE TABLE IF NOT EXISTS {count_schema}.casrec_orders (
    "Order No" text,
    "Case" text
);
INSERT INTO {count_schema}.casrec_orders ("Order No", "Case")
SELECT "Order No", "Case" FROM {casrec_schema}.order WHERE "Ord Stat" != 'Open';

DROP INDEX IF EXISTS {count_schema}.filteredorder_orderno_idx;
CREATE UNIQUE INDEX filteredorder_orderno_idx ON {count_schema}.casrec_orders ("Order No");

DROP INDEX IF EXISTS {count_schema}.filteredorder_case_idx;
CREATE INDEX filteredorder_case_idx ON {count_schema}.casrec_orders ("Case");

-- We are only migrating deputies linked to cases
-- so, this is all deputies linked to a deputyship on a case as above
DROP TABLE IF EXISTS {count_schema}.casrec_deps;
CREATE TABLE IF NOT EXISTS {count_schema}.casrec_deps ("Deputy No" text);
INSERT INTO {count_schema}.casrec_deps ("Deputy No")
SELECT DISTINCT dep."Deputy No"
FROM {casrec_schema}.deputy dep
    INNER JOIN {casrec_schema}.deputyship ds
        ON ds."Deputy No" = dep."Deputy No"
    INNER JOIN {count_schema}.casrec_orders o
        ON o."Order No" = ds."Order No";

DROP INDEX IF EXISTS {count_schema}.filtereddeps_deputynumber_idx;
CREATE UNIQUE INDEX filtereddeps_deputynumber_idx ON {count_schema}.casrec_deps ("Deputy No");

DROP FUNCTION IF EXISTS {count_schema}.warning_violent_lookup;
CREATE FUNCTION {count_schema}.warning_violent_lookup(lookup_key character varying DEFAULT NULL::character varying) returns text
    language sql
as
$$
SELECT CASE
        WHEN ($1 = '4') THEN 'Marker'
        WHEN ($1 = '3') THEN 'Special'
        WHEN ($1 = 'Y') THEN 'SAAR'
        WHEN ($1 = '1') THEN 'No Debt'
        WHEN ($1 = '0') THEN ''
    END
$$;

ALTER TABLE {count_schema}.counts DROP COLUMN IF EXISTS {working_column};
ALTER TABLE {count_schema}.counts ADD COLUMN {working_column} int;

-- persons_clients
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {casrec_schema}.pat
)
WHERE supervision_table = 'persons_clients';

-- persons_deputies
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {count_schema}.casrec_deps
)
WHERE supervision_table = 'persons_deputies';

-- cases
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {count_schema}.casrec_orders
)
WHERE supervision_table = 'cases';

-- phonenumbers
UPDATE {count_schema}.counts SET {working_column} =
(
    -- client
    SELECT COUNT(*)
    FROM {casrec_schema}.pat
    WHERE "Client Phone" != ''
)+(
    -- deputy daytime
    SELECT COUNT(*)
    FROM {count_schema}.casrec_deps cd
    INNER JOIN {casrec_schema}.deputy dep ON dep."Deputy No" = cd."Deputy No"
    WHERE dep."Contact Telephone" != ''
)+(
    -- deputy evening
    SELECT COUNT(*)
    FROM {count_schema}.casrec_deps cd
    INNER JOIN {casrec_schema}.deputy dep ON dep."Deputy No" = cd."Deputy No"
    WHERE dep."Contact Tele2" != ''
)
WHERE supervision_table = 'phonenumbers';

-- addresses
UPDATE {count_schema}.counts SET {working_column} =
(
    -- client
    SELECT COUNT(*) FROM {casrec_schema}.pat
)+(
    -- deputy PRO
    SELECT COUNT(*) FROM (
        SELECT DISTINCT
            dl.casrec_row_id dl_id
        FROM {casrec_schema}.deplink dl
        INNER JOIN {count_schema}.casrec_deps cd
            ON dl."Deputy No" = cd."Deputy No"
        INNER JOIN {casrec_schema}.deputy d
            ON cd."Deputy No" = d."Deputy No"
        INNER JOIN {casrec_schema}.deputy_address add
            ON add."Dep Addr No" = dl."Dep Addr No"
        WHERE d."Dep Type" IN ('20','21','22','24','25','26','27','28','29','63','71')
        AND dl."Main Addr" = '1'
    ) dep_pro_count
)+(
    -- deputy Non-PRO
    -- exactly the same as Phase 1 migration with added dep type filter
    SELECT COUNT(*) FROM (
        SELECT DISTINCT
            LOWER(TRIM(COALESCE(d."Email", ''))),
            LOWER(TRIM(COALESCE(d."Dep Surname", ''))),
            LOWER(TRIM(COALESCE(add."Dep Postcode", '')))
        FROM {casrec_schema}.deputy_address add
        INNER JOIN {casrec_schema}.deputyship ds
            ON ds."Dep Addr No" = add."Dep Addr No"
        INNER JOIN {count_schema}.casrec_orders o
            ON o."Order No" = ds."Order No"
        INNER JOIN {casrec_schema}.deputy d
            ON ds."Deputy No" = d."Deputy No"
        WHERE d."Dep Type" NOT IN ('20','21','22','24','25','26','27','28','29','63','71')
    ) dep_non_pro_count
)
WHERE supervision_table = 'addresses';

-- supervision_notes
UPDATE {count_schema}.counts SET {working_column} =
(
    -- client
    SELECT COUNT(*) FROM {casrec_schema}.Remarks
)+(
    -- deputy
    SELECT COUNT(*)
    FROM {casrec_schema}.deputy_remarks rem
    INNER JOIN {count_schema}.casrec_deps dep ON dep."Deputy No" = rem."Deputy No"
)
WHERE supervision_table = 'supervision_notes';

-- tasks
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*)
    FROM {casrec_schema}.SUP_ACTIVITY act
    WHERE act."Status" IN ('ACTIVE')
    AND EXISTS (
        SELECT "Case"
        FROM {casrec_schema}.order o
        WHERE o."Case" = act."Case"
        AND "Ord Stat" != 'Open'
    )
)
WHERE supervision_table = 'tasks';

-- finance_persons
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {casrec_schema}.pat
)
WHERE supervision_table = 'finance_person';

-- death notifications
UPDATE {count_schema}.counts SET {working_column} =
(
    -- client
    SELECT COUNT(*) FROM {casrec_schema}.pat WHERE pat."Term Type" = 'D'
)+(
    -- deputy
    SELECT COUNT(*)
    FROM {count_schema}.casrec_deps cd
    INNER JOIN {casrec_schema}.deputy dep ON dep."Deputy No" = cd."Deputy No"
    AND dep."Stat" = '99'
)
WHERE supervision_table = 'death_notifications';

-- warnings
UPDATE {count_schema}.counts SET {working_column} =
(
    -- client_nodebtchase
    SELECT COUNT(*)
    FROM {casrec_schema}.pat
    WHERE {casrec_schema}.pat."Debt chase" = '1'
)+(
    -- client_saarcheck
    SELECT COUNT(*)
    FROM {casrec_schema}.pat
    WHERE {casrec_schema}.pat."SAAR Check" = 'Y'
)+(
    -- client_special
    SELECT COUNT(*)
    FROM {casrec_schema}.pat
    WHERE {casrec_schema}.pat."SIM" = '3'
)+(
    -- client_violent
    SELECT COUNT(*)
    FROM {casrec_schema}.pat
    WHERE {casrec_schema}.pat."VWM" = '4'
)+(
    -- p1_client_remarks
    SELECT COUNT(*)
    FROM {casrec_schema}.remarks rem
    WHERE rem."Pri" = '1'
)+(
    -- deputy_special
    SELECT COUNT(*)
    FROM {count_schema}.casrec_deps cd
    INNER JOIN {casrec_schema}.deputy dep ON dep."Deputy No" = cd."Deputy No"
    WHERE dep."SIM" = '3'
)+(
    -- deputy_violent
    SELECT COUNT(*)
    FROM {count_schema}.casrec_deps cd
    INNER JOIN {casrec_schema}.deputy dep ON dep."Deputy No" = cd."Deputy No"
    WHERE dep."VWM" = '4'
)
WHERE supervision_table = 'warnings';

-- annual_report_logs
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT SUM(table_count) FROM (
        SELECT COUNT(*) AS table_count FROM {casrec_schema}.account

        UNION

        SELECT COUNT(*) AS table_count FROM (
            SELECT "Case" AS caserecnumber FROM {casrec_schema}.pat p
            INNER JOIN(
                SELECT account_case FROM {casrec_schema}.order o
                INNER JOIN (
                    SELECT
                        a."Case" as account_case,
                        row_number() OVER (
                            PARTITION BY a."Case"
                            ORDER BY a."End Date" DESC
                        ) AS rownum
                    FROM {casrec_schema}.account a
                ) AS cases
                ON o."Case" = cases.account_case
                WHERE cases.rownum = 1
                AND o."Ord Stat" = 'Active'
            ) AS active_cases
            ON p."Case" = active_cases.account_case
            WHERE p."Report Due" != ''
        ) pending_cases
    ) sums
)
WHERE supervision_table = 'annual_report_logs';

-- annual_report_lodging_details
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {casrec_schema}.account
)
WHERE supervision_table = 'annual_report_lodging_details';

-- visits
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT vis."casrec_row_id"
        FROM {casrec_schema}.REPVIS vis
    ) t1
)
WHERE supervision_table = 'visits';

-- bonds
UPDATE {count_schema}.counts SET {working_column} =
(
    -- active
    SELECT COUNT(*)
    FROM {casrec_schema}.order o
    INNER JOIN {count_schema}.casrec_orders co ON co."Order No" = o."Order No"
    WHERE o."Bond Rqd" = 'Y'
)+(
    -- dispensed
    SELECT COUNT(*)
    FROM {casrec_schema}.order o
    INNER JOIN {count_schema}.casrec_orders co ON co."Order No" = o."Order No"
    WHERE o."Bond Rqd" = 'S'
)
WHERE supervision_table = 'bonds';

-- feepayer_id (logic in transforms look like this should be here but it does not work):
-- AND d."Disch Death" = ''
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*)
    FROM {count_schema}.casrec_orders o
    LEFT JOIN {casrec_schema}.deputyship ds ON ds."Order No" = o."Order No"
    LEFT JOIN {casrec_schema}.deputy d ON ds."Deputy No" = d."Deputy No"
    WHERE ds."Fee Payer" = 'Y'
    AND d."Stat" = '1'
)
WHERE supervision_table = 'feepayer_id';

-- timeline_event
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {casrec_schema}.pat
)
WHERE supervision_table = 'timeline_event';

-- person_timeline
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {casrec_schema}.pat
)
WHERE supervision_table = 'person_timeline';

-- supervision_level_log
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*)
    FROM {count_schema}.casrec_orders
)
WHERE supervision_table = 'supervision_level_log';

-- finance_invoice_ad
SET datestyle = "ISO, DMY";
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT "Invoice No"
        FROM {casrec_schema}.feeexport fx
        LEFT JOIN {casrec_schema}.sop_aged_debt sad ON sad."Trx Number" = fx."Invoice No"
        WHERE LEFT(fx."Invoice No", 2) = 'AD'
          AND CAST(fx."Amount" AS DOUBLE PRECISION) > 0
          AND (NULLIF(fx."Create", 'NaT')::timestamp(0) > '2019-03-31 23:59:59'::timestamp(0)
                   OR CAST(sad."Outstanding Amount" AS DOUBLE PRECISION) != 0)
    ) t1
)
WHERE supervision_table = 'finance_invoice_ad';

-- finance_invoice_non_ad
SET datestyle = "ISO, DMY";
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT "Invoice No"
        FROM {casrec_schema}.feeexport fx
        LEFT JOIN {casrec_schema}.sop_aged_debt sad ON sad."Trx Number" = fx."Invoice No"
        WHERE LEFT(fx."Invoice No", 2) <> 'AD'
            AND CAST(fx."Amount" AS DOUBLE PRECISION) > 0
            AND (NULLIF(fx."Create", 'NaT')::timestamp(0) > '2019-03-31 23:59:59'::timestamp(0)
                OR CAST(sad."Outstanding Amount" AS DOUBLE PRECISION) != 0)
    ) t1
)
WHERE supervision_table = 'finance_invoice_non_ad';

-- finance_remissions
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT
        {casrec_schema}.pat."Case" AS caserecnumber,
        CAST(NULLIF(NULLIF(TRIM({casrec_schema}.pat."Award Date"), 'NaT'), '') AS date) AS enddate
        FROM {casrec_schema}.pat
        WHERE pat."Remis" <> '0'
        AND pat."Award Date"::timestamp >= '2021-04-02'::timestamp
    ) t1
)
WHERE supervision_table = 'finance_remissions';

-- finance_exemptions
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT
        {casrec_schema}.pat."Case" AS caserecnumber,
        CAST(NULLIF(NULLIF(TRIM({casrec_schema}.pat."Award Date"), 'NaT'), '') AS date) AS enddate
        FROM {casrec_schema}.pat
        WHERE pat."Exempt" <> '0'
        AND pat."Award Date"::timestamp >= '2021-04-02'::timestamp
    ) t1
)
WHERE supervision_table = 'finance_exemptions';

-- finance_ledger_credits
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*)
    FROM {casrec_schema}.feeexport
    WHERE CAST(feeexport."Amount" AS DOUBLE PRECISION) < 0
    AND EXISTS (
        SELECT 1
        FROM {casrec_schema}.feeexport fe
        LEFT JOIN {casrec_schema}.sop_aged_debt sad
            ON sad."Trx Number" = fe."Invoice No"
        WHERE fe."Invoice No" = {casrec_schema}.feeexport."Orig Invoice"
            AND CAST(fe."Amount" AS DOUBLE PRECISION) > 0
            AND (NULLIF(fe."Create", 'NaT')::timestamp(0) > '2019-03-31 23:59:59'::timestamp(0)
                OR CAST(sad."Outstanding Amount" AS DOUBLE PRECISION) != 0)
    )
)
WHERE supervision_table = 'finance_ledger_credits';

-- finance_allocation_credits
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*)
    FROM {casrec_schema}.feeexport
    LEFT JOIN {casrec_schema}.pat ON {casrec_schema}.pat."Case" = {casrec_schema}.feeexport."Case"
    LEFT JOIN {casrec_schema}.sop_feecheckcredits ON {casrec_schema}.sop_feecheckcredits."Invoice Number" = {casrec_schema}.feeexport."Invoice No"
    WHERE CAST(feeexport."Amount" AS DOUBLE PRECISION) < 0
    AND EXISTS (
        SELECT 1
        FROM {casrec_schema}.feeexport fe
        LEFT JOIN {casrec_schema}.sop_aged_debt sad
            ON sad."Trx Number" = fe."Invoice No"
        WHERE fe."Invoice No" = {casrec_schema}.feeexport."Orig Invoice"
            AND CAST(fe."Amount" AS DOUBLE PRECISION) > 0
            AND (NULLIF(fe."Create", 'NaT')::timestamp(0) > '2019-03-31 23:59:59'::timestamp(0)
                OR CAST(sad."Outstanding Amount" AS DOUBLE PRECISION) != 0)
    )
)
WHERE supervision_table = 'finance_allocation_credits';

-- finance_order
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT
            {casrec_schema}.pat."Case" AS caserecnumber,
            ra.start_date AS billing_start_date
        FROM {casrec_schema}.order
        LEFT JOIN (
            SELECT MIN(NULLIF("Start Date", '')::date) AS start_date,
            "Order No"
            FROM {casrec_schema}.risk_assessment
            GROUP BY "Order No"
        ) ra
            ON ra."Order No" = {casrec_schema}.order."Order No"
        LEFT JOIN {casrec_schema}.pat ON pat."Case" = {casrec_schema}.order."Case"
        WHERE {casrec_schema}.order."Ord Type" IN ('1','2','40','41')
          AND {casrec_schema}.order."Ord Stat" <> 'Open'
          AND {casrec_schema}.order."Ord Risk Lvl" <> ''
    ) t1
)
WHERE supervision_table = 'finance_order';

-- order_deputy
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {casrec_schema}.deputyship ds
    INNER JOIN {count_schema}.casrec_orders co ON co."Order No" = ds."Order No"
)
WHERE supervision_table = 'order_deputy';

-- person_caseitem
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*) FROM {count_schema}.casrec_orders
)
WHERE supervision_table = 'person_caseitem';

-- person_task
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT COUNT(*)
    FROM {casrec_schema}.SUP_ACTIVITY act
    WHERE act."Status" IN ('ACTIVE')
    AND EXISTS (
        SELECT "Case"
        FROM {casrec_schema}.order o
        WHERE o."Case" = act."Case"
        AND "Ord Stat" != 'Open'
    )
)
WHERE supervision_table = 'person_task';

-- person_warning
UPDATE {count_schema}.counts SET {working_column} =
(
    SELECT counts.{working_column} FROM {count_schema}.counts WHERE supervision_table = 'warnings'
)
WHERE supervision_table = 'person_warning';

-- annual_report_letter_status
UPDATE {count_schema}.counts
SET {working_column} = 0
WHERE supervision_table = 'annual_report_letter_status';

-- annual_report_type_assignments
UPDATE {count_schema}.counts
SET {working_column} =
(
    SELECT SUM(table_count) FROM (
        SELECT COUNT(*) AS table_count FROM {casrec_schema}.account
        UNION
        SELECT COUNT(*) AS table_count FROM (
            SELECT "Case" AS caserecnumber FROM {casrec_schema}.pat p
            INNER JOIN(
                SELECT account_case FROM {casrec_schema}.order o
                INNER JOIN (
                    SELECT
                        a."Case" as account_case,
                        row_number() OVER (
                            PARTITION BY a."Case"
                            ORDER BY a."End Date" DESC
                        ) AS rownum
                    FROM {casrec_schema}.account a
                ) AS cases
                ON o."Case" = cases.account_case
                WHERE cases.rownum = 1
                AND o."Ord Stat" = 'Active'
            ) AS active_cases
            ON p."Case" = active_cases.account_case
            WHERE p."Report Due" != ''
        ) pending_cases
    ) sums
)
WHERE supervision_table = 'annual_report_type_assignments';

-- deputy_person_document (not migrating)
UPDATE {count_schema}.counts
SET {working_column} = 0
WHERE supervision_table = 'deputy_person_document';

-- deputy_person_document (not migrating)
UPDATE {count_schema}.counts
SET {working_column} = 0
WHERE supervision_table = 'person_document';

-- caseitem_document (not migrating)
UPDATE {count_schema}.counts
SET {working_column} = 0
WHERE supervision_table = 'caseitem_document';

DROP INDEX IF EXISTS {count_schema}.filteredorder_orderno_idx;
DROP INDEX IF EXISTS {count_schema}.filteredorder_case_idx;
DROP INDEX IF EXISTS {count_schema}.filtereddeps_deputynumber_idx;

DROP TABLE IF EXISTS {count_schema}.casrec_orders;
DROP TABLE IF EXISTS {count_schema}.casrec_deps;

DROP FUNCTION IF EXISTS {count_schema}.warning_violent_lookup;
