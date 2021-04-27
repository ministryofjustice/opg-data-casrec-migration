-- These are ordered!
-- e.g. you need the pat table to construct the other queries so delete from that last

-- Add to this file as we implement each entity and understand link to client caseref.

-- deputy
DELETE FROM casrec_csv.deputy WHERE "Deputy No" IN (
    SELECT deputyship."Deputy No" FROM casrec_csv.deputyship WHERE deputyship."Case" IN (
        SELECT casrec_csv.pat."Case" FROM casrec_csv.pat WHERE casrec_csv.pat."Lay Team" != '{team}'
    )
);
SELECT COUNT(*) FROM casrec_csv.deputy;

-- deputyships
DELETE FROM casrec_csv.deputyship WHERE deputyship."Case" IN (
    SELECT casrec_csv.pat."Case" FROM casrec_csv.pat WHERE casrec_csv.pat."Lay Team" != '{team}'
);
SELECT COUNT(*) FROM casrec_csv.deputyship;

-- order table (cases)
DELETE FROM casrec_csv.order
USING casrec_csv.pat
WHERE pat."Case" = casrec_csv.order."Case"
AND casrec_csv.pat."Lay Team" != '{team}';
SELECT COUNT(*) FROM casrec_csv.order;

-- pat
DELETE FROM casrec_csv.pat WHERE "Lay Team" != '{team}';
