-- dropping and recreating unexpected columns simplifies on local dev where tests may be run out of order
ALTER TABLE countverification.counts DROP COLUMN IF EXISTS expected;
ALTER TABLE countverification.counts DROP COLUMN IF EXISTS final_count;
ALTER TABLE countverification.counts DROP COLUMN IF EXISTS result;
ALTER TABLE countverification.counts DROP COLUMN IF EXISTS casrec_source;
ALTER TABLE countverification.counts ADD COLUMN casrec_source int NOT NULL DEFAULT -1;

DROP INDEX IF EXISTS countverification.filteredorder_orderno_idx;
DROP INDEX IF EXISTS countverification.filteredorder_case_idx;
DROP INDEX IF EXISTS countverification.filtereddeps_deputynumber_idx;
DROP TABLE IF EXISTS countverification.filtered_orders;
DROP TABLE IF EXISTS countverification.filtered_deps;
DROP FUNCTION IF EXISTS countverification.warning_violent_lookup;

-- contains all orders != status of open
CREATE TABLE IF NOT EXISTS countverification.filtered_orders (
    "Order No" text,
    "Case" text
);
INSERT INTO countverification.filtered_orders ("Order No", "Case")
SELECT "Order No", "Case" FROM casrec_csv.order WHERE "Ord Stat" != 'Open';
CREATE UNIQUE INDEX filteredorder_orderno_idx ON countverification.filtered_orders ("Order No");
CREATE INDEX filteredorder_case_idx ON countverification.filtered_orders ("Case");

-- We are only migrating deputies linked to cases
-- so, this is all deputies linked to a deputyship on a case as above
CREATE TABLE IF NOT EXISTS countverification.filtered_deps ("Deputy No" text);
INSERT INTO countverification.filtered_deps ("Deputy No")
SELECT DISTINCT dep."Deputy No"
FROM casrec_csv.deputy dep
    INNER JOIN casrec_csv.deputyship ds
        ON ds."Deputy No" = dep."Deputy No"
    INNER JOIN countverification.filtered_orders o
        ON o."Order No" = ds."Order No";
CREATE UNIQUE INDEX filtereddeps_deputynumber_idx ON countverification.filtered_deps ("Deputy No");

CREATE FUNCTION countverification.warning_violent_lookup(lookup_key character varying DEFAULT NULL::character varying) returns text
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

-- persons_clients
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM casrec_csv.pat
)
WHERE supervision_table = 'persons_clients';

-- persons_deputies
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM countverification.filtered_deps
)
WHERE supervision_table = 'persons_deputies';

-- cases
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM countverification.filtered_orders
)
WHERE supervision_table = 'cases';

-- phonenumbers
UPDATE countverification.counts SET casrec_source =
(
    -- client
    SELECT COUNT(*)
    FROM casrec_csv.pat
    WHERE "Client Phone" != ''
)+(
    -- deputy daytime
    SELECT COUNT(*)
    FROM countverification.filtered_deps fd
    INNER JOIN casrec_csv.deputy dep ON dep."Deputy No" = fd."Deputy No"
    WHERE dep."Contact Telephone" != ''
)+(
    -- deputy evening
    SELECT COUNT(*)
    FROM countverification.filtered_deps fd
    INNER JOIN casrec_csv.deputy dep ON dep."Deputy No" = fd."Deputy No"
    WHERE dep."Contact Tele2" != ''
)
WHERE supervision_table = 'phonenumbers';

-- addresses
UPDATE countverification.counts SET casrec_source =
(
    -- client
    SELECT COUNT(*) FROM casrec_csv.pat
)+(
    -- deputy
    SELECT DISTINCT lower(d."Email"), lower(d."Dep Surname"), lower(d."Dep Forename"), lower(add."Dep Postcode")
    FROM casrec_csv.deputy_address add
    INNER JOIN casrec_csv.deputyship ds
        ON ds."Dep Addr No" = add."Dep Addr No"
    INNER JOIN countverification.filtered_orders o
        ON o."Order No" = ds."Order No"
    INNER JOIN casrec_csv.deputy d
    ON ds."Deputy No" = d."Deputy No"
    except
    SELECT DISTINCT lower(p.email), lower(p.surname), lower(p.firstname), lower(ad.postcode)
    FROM addresses ad
    INNER JOIN countverification.cp1_post_deputies dep ON dep.id = ad.person_id
    INNER JOIN persons p ON p.id = dep.id
)

    SELECT DISTINCT lower(p.email), lower(p.surname), lower(p.firstname), lower(ad.postcode)
    FROM addresses ad
    INNER JOIN countverification.cp1_post_deputies dep ON dep.id = ad.person_id
    INNER JOIN persons p ON p.id = dep.id
    WHERE lower(ad.postcode) = 'ne3 5dt'

WHERE supervision_table = 'addresses';

-- supervision_notes
UPDATE countverification.counts SET casrec_source =
(
    -- client
    SELECT COUNT(*) FROM casrec_csv.Remarks
)+(
    -- deputy
    SELECT COUNT(*)
    FROM casrec_csv.deputy_remarks rem
    INNER JOIN countverification.filtered_deps dep ON dep."Deputy No" = rem."Deputy No"
)
WHERE supervision_table = 'supervision_notes';

-- tasks
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*)
    FROM casrec_csv.SUP_ACTIVITY act
    WHERE act."Status" IN ('INACTIVE','ACTIVE')
)
WHERE supervision_table = 'tasks';

-- death notifications
UPDATE countverification.counts SET casrec_source =
(
    -- client
    SELECT COUNT(*) FROM casrec_csv.pat WHERE pat."Term Type" = 'D'
)+(
    -- deputy
    SELECT COUNT(*)
    FROM countverification.filtered_deps fd
    INNER JOIN casrec_csv.deputy dep ON dep."Deputy No" = fd."Deputy No"
    AND dep."Stat" = '99'
)
WHERE supervision_table = 'death_notifications';

-- warnings
UPDATE countverification.counts SET casrec_source =
(
    -- client_nodebtchase
    SELECT COUNT(*)
    FROM casrec_csv.pat
    WHERE casrec_csv.pat."Debt chase" = '1'
)+(
    -- client_saarcheck
    SELECT COUNT(*)
    FROM casrec_csv.pat
    WHERE casrec_csv.pat."SAAR Check" = 'Y'
)+(
    -- client_special
    SELECT COUNT(*)
    FROM casrec_csv.pat
    WHERE casrec_csv.pat."SIM" = '3'
)+(
    -- client_violent
    SELECT COUNT(*)
    FROM casrec_csv.pat
    WHERE casrec_csv.pat."VWM" = '4'
)+(
    -- p1_client_remarks
    SELECT COUNT(*)
    FROM casrec_csv.remarks rem
    WHERE rem."Pri" = '1'
)+(
    -- deputy_special
    SELECT COUNT(*)
    FROM countverification.filtered_deps fd
    INNER JOIN casrec_csv.deputy dep ON dep."Deputy No" = fd."Deputy No"
    WHERE dep."SIM" = '3'
)+(
    -- deputy_violent
    SELECT COUNT(*)
    FROM countverification.filtered_deps fd
    INNER JOIN casrec_csv.deputy dep ON dep."Deputy No" = fd."Deputy No"
    WHERE dep."VWM" = '4'
)
WHERE supervision_table = 'warnings';

-- annual_report_logs
UPDATE countverification.counts SET casrec_source =
(
    SELECT SUM(table_count) FROM (
        SELECT COUNT(*) AS table_count FROM casrec_csv.account

        UNION

        SELECT COUNT(*) AS table_count FROM (
            SELECT "Case" AS caserecnumber FROM casrec_csv.pat p
            INNER JOIN(
                SELECT account_case FROM casrec_csv.order o
                INNER JOIN (
                    SELECT
                        a."Case" as account_case,
                        row_number() OVER (
                            PARTITION BY a."Case"
                            ORDER BY a."End Date" DESC
                        ) AS rownum
                    FROM casrec_csv.account a
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
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM casrec_csv.account
)
WHERE supervision_table = 'annual_report_lodging_details';

-- visits
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT vis."casrec_row_id"
        FROM casrec_csv.REPVIS vis
    ) t1
)
WHERE supervision_table = 'visits';

-- bonds
UPDATE countverification.counts SET casrec_source =
(
    -- active
    SELECT COUNT(*)
    FROM casrec_csv.order o
    INNER JOIN countverification.filtered_orders fo ON fo."Order No" = o."Order No"
    WHERE o."Bond Rqd" = 'Y'
)+(
    -- dispensed
    SELECT COUNT(*)
    FROM casrec_csv.order o
    INNER JOIN countverification.filtered_orders fo ON fo."Order No" = o."Order No"
    WHERE o."Bond Rqd" = 'S'
)
WHERE supervision_table = 'bonds';

-- feepayer_id
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*)
    FROM countverification.filtered_orders o
    LEFT JOIN casrec_csv.deputyship ds ON ds."Order No" = o."Order No"
    LEFT JOIN casrec_csv.deputy d ON ds."Deputy No" = d."Deputy No"
    WHERE ds."Fee Payer" = 'Y'
    AND d."Stat" = '1'
    AND d."Disch Death" = ''
)
WHERE supervision_table = 'feepayer_id';

-- timeline_event
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM casrec_csv.pat
)
WHERE supervision_table = 'timeline_event';

-- person_timeline
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM casrec_csv.pat
)
WHERE supervision_table = 'person_timeline';

-- supervision_level_log
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*)
    FROM countverification.filtered_orders
)
WHERE supervision_table = 'supervision_level_log';

-- finance_invoice_ad
SET datestyle = "ISO, DMY";
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT "Invoice No"
        FROM casrec_csv.feeexport fx
        LEFT JOIN casrec_csv.sop_aged_debt sad ON sad."Trx Number" = fx."Invoice No"
        WHERE LEFT(fx."Invoice No", 2) = 'AD'
          AND CAST(fx."Amount" AS DOUBLE PRECISION) > 0
          AND (NULLIF(fx."Create", 'NaT')::timestamp(0) > '2019-03-31 23:59:59'::timestamp(0)
                   OR CAST(sad."Outstanding Amount" AS DOUBLE PRECISION) != 0)
    ) t1
)
WHERE supervision_table = 'finance_invoice_ad';

-- finance_invoice_non_ad
SET datestyle = "ISO, DMY";
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT "Invoice No"
        FROM casrec_csv.feeexport fx
        LEFT JOIN casrec_csv.sop_aged_debt sad ON sad."Trx Number" = fx."Invoice No"
        WHERE LEFT(fx."Invoice No", 2) <> 'AD'
            AND CAST(fx."Amount" AS DOUBLE PRECISION) > 0
            AND (NULLIF(fx."Create", 'NaT')::timestamp(0) > '2019-03-31 23:59:59'::timestamp(0)
                OR CAST(sad."Outstanding Amount" AS DOUBLE PRECISION) != 0)
    ) t1
)
WHERE supervision_table = 'finance_invoice_non_ad';

-- finance_remissions
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT
        casrec_csv.pat."Case" AS caserecnumber,
        CAST(NULLIF(NULLIF(TRIM(casrec_csv.pat."Award Date"), 'NaT'), '') AS date) AS enddate
        FROM casrec_csv.pat
        WHERE pat."Remis" <> '0'
        AND pat."Award Date"::timestamp >= '2021-04-02'::timestamp
    ) t1
)
WHERE supervision_table = 'finance_remissions';

-- finance_exemptions
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT
        casrec_csv.pat."Case" AS caserecnumber,
        CAST(NULLIF(NULLIF(TRIM(casrec_csv.pat."Award Date"), 'NaT'), '') AS date) AS enddate
        FROM casrec_csv.pat
        WHERE pat."Exempt" <> '0'
        AND pat."Award Date"::timestamp >= '2021-04-02'::timestamp
    ) t1
)
WHERE supervision_table = 'finance_exemptions';

-- finance_ledger_credits
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*)
    FROM casrec_csv.feeexport
    WHERE CAST(feeexport."Amount" AS DOUBLE PRECISION) < 0
    AND EXISTS (
        SELECT 1
        FROM casrec_csv.feeexport fe
        LEFT JOIN casrec_csv.sop_aged_debt sad
            ON sad."Trx Number" = fe."Invoice No"
        WHERE fe."Invoice No" = casrec_csv.feeexport."Orig Invoice"
            AND CAST(fe."Amount" AS DOUBLE PRECISION) > 0
            AND (NULLIF(fe."Create", 'NaT')::timestamp(0) > '2019-03-31 23:59:59'::timestamp(0)
                OR CAST(sad."Outstanding Amount" AS DOUBLE PRECISION) != 0)
    )
)
WHERE supervision_table = 'finance_ledger_credits';

-- finance_allocation_credits
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*)
    FROM casrec_csv.feeexport
    LEFT JOIN casrec_csv.pat ON casrec_csv.pat."Case" = casrec_csv.feeexport."Case"
    LEFT JOIN casrec_csv.sop_feecheckcredits ON casrec_csv.sop_feecheckcredits."Invoice Number" = casrec_csv.feeexport."Invoice No"
    WHERE CAST(feeexport."Amount" AS DOUBLE PRECISION) < 0
    AND EXISTS (
        SELECT 1
        FROM casrec_csv.feeexport fe
        LEFT JOIN casrec_csv.sop_aged_debt sad
            ON sad."Trx Number" = fe."Invoice No"
        WHERE fe."Invoice No" = casrec_csv.feeexport."Orig Invoice"
            AND CAST(fe."Amount" AS DOUBLE PRECISION) > 0
            AND (NULLIF(fe."Create", 'NaT')::timestamp(0) > '2019-03-31 23:59:59'::timestamp(0)
                OR CAST(sad."Outstanding Amount" AS DOUBLE PRECISION) != 0)
    )
)
WHERE supervision_table = 'finance_allocation_credits';

-- finance_order
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM (
        SELECT DISTINCT
            casrec_csv.pat."Case" AS caserecnumber,
            ra.start_date AS billing_start_date
        FROM casrec_csv.order
        LEFT JOIN (
            SELECT MIN(NULLIF("Start Date", '')::date) AS start_date,
            "Order No"
            FROM casrec_csv.risk_assessment
            GROUP BY "Order No"
        ) ra
            ON ra."Order No" = casrec_csv.order."Order No"
        LEFT JOIN casrec_csv.pat ON pat."Case" = casrec_csv.order."Case"
        WHERE casrec_csv.order."Ord Type" IN ('1','2','40','41')
          AND casrec_csv.order."Ord Stat" <> 'Open'
          AND casrec_csv.order."Ord Risk Lvl" <> ''
    ) t1
)
WHERE supervision_table = 'finance_order';

-- order_deputy
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM casrec_csv.deputyship ds
    INNER JOIN countverification.filtered_orders fo ON fo."Order No" = ds."Order No"
)
WHERE supervision_table = 'order_deputy';

-- person_caseitem
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*) FROM countverification.filtered_orders
)
WHERE supervision_table = 'person_caseitem';

-- person_task
UPDATE countverification.counts SET casrec_source =
(
    SELECT COUNT(*)
    FROM casrec_csv.SUP_ACTIVITY act
    INNER JOIN casrec_csv.pat ON pat."Case" = act."Case"
    WHERE act."Status" IN ('INACTIVE','ACTIVE')
)
WHERE supervision_table = 'person_task';

-- person_warning
UPDATE countverification.counts SET casrec_source =
(
    SELECT counts.casrec_source FROM countverification.counts WHERE supervision_table = 'warnings'
)
WHERE supervision_table = 'person_warning';