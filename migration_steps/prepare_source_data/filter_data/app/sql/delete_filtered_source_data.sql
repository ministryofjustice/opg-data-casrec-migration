-- These are ordered!
-- e.g. you need the pat table to construct the other queries so delete from that last

-- Add to this file as we implement each entity and understand link to client caseref.

-- Filters Crec
DELETE FROM {casrec_schema}.crec WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters deputyships
DELETE FROM {casrec_schema}.deputyship WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters:
-- deputy
-- "deputy_persons",
-- "deputy_death_notifications",
-- "deputy_special_warnings",
-- "deputy_violent_warnings",
-- "deputy_daytime_phonenumbers",
-- "deputy_evening_phonenumbers",
DELETE FROM {casrec_schema}.deputy WHERE NOT EXISTS (
    SELECT 1 FROM {casrec_schema}.deputyship WHERE deputyship."Deputy No" = deputy."Deputy No"
);

-- Filters deputy_addresses
DELETE FROM {casrec_schema}.deputy_address WHERE NOT EXISTS (
    SELECT 1 FROM {casrec_schema}.deputyship WHERE deputyship."Dep Addr No" = deputy_address."Dep Addr No"
);

-- Filters deputy_notes
DELETE FROM {casrec_schema}.deputy_remarks WHERE NOT EXISTS (
    SELECT 1 FROM {casrec_schema}.deputyship WHERE deputyship."Deputy No" = deputy_remarks."Deputy No"
);

-- Filters:
-- "cases",
-- "supervision_level_log"
DELETE FROM {casrec_schema}.order WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters:
-- "supervision_notes"
-- "warnings" (P1 client remarks)
DELETE FROM {casrec_schema}.remarks WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters visits
DELETE FROM {casrec_schema}.repvis WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters:
-- "annual_report_logs"
-- "annual_report_lodging_details"
DELETE FROM {casrec_schema}.account WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters:
-- "finance_invoice"
-- "finance_ledger"
-- "finance_ledger_allocation"
DELETE FROM {casrec_schema}.feeexport WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters tasks
DELETE FROM {casrec_schema}.sup_activity WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters:
-- "client",
-- "client_addresses",
-- "client_persons",
-- "client_phonenumbers",
-- "client_death_notifications",
-- "client_nodebtchase_warnings",
-- "client_saarcheck_warnings",
-- "client_special_warnings",
-- "client_violent_warnings",
-- "finance_remissions",
-- "finance_exemptions",
DELETE FROM {casrec_schema}.pat WHERE "Case" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);

-- Filters casrec_letters (only used for validation purposes)
DELETE FROM {casrec_schema}.casrec_letters WHERE "caseno" IN (
    SELECT DISTINCT caserecnumber FROM {casrec_schema}.cases_to_filter_out
);
