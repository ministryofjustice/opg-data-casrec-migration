-- These are ordered!
-- e.g. you need the pat table to construct the other queries so delete from that last

-- Add to this file as we implement each entity and understand link to client caseref.

-- added for testing
UPDATE casrec_csv.pat SET "Lay Team" = 'T1' WHERE "Lay Team" != '';
UPDATE casrec_csv.pat SET "Lay Team" = 'T2' WHERE "Case" IN (
 '10004637',
 '10004741',
 '99368551',
 '99351724',
 '99370843',
 '99370768',
 '1254463T',
 '1358321T',
 '1201357T',
 '99368551',
 '99370768',
 '1254463T',
 '1358321T',
 '1201357T',
 '12109482',
 '96825507',
 '97528955',
 '99329333',
 '13017047',
 '13458991',
 '10255945',
 '1048587T',
 '98400045',
 '11010609',
 '11365139',
 '99385168',
 '13336386',
 '99384332',
 '13109368',
 '99374412',
 '11188625',
 '99378315',
 '10248689',
 '13493614',
 '98646339',
 '94021339',
 '12591582',
 '11519774',
 '11749830',
 '10146500',
 '94071935',
 '99382896',
 '10025768'
);

-- deputy
DELETE FROM casrec_csv.deputy WHERE "Deputy No" IN (
    SELECT deputyship."Deputy No" FROM casrec_csv.deputyship WHERE deputyship."Case" IN (
        SELECT casrec_csv.pat."Case" FROM casrec_csv.pat WHERE casrec_csv.pat."Lay Team" != '{team}'
    )
);

-- deputyships
DELETE FROM casrec_csv.deputyship WHERE deputyship."Case" IN (
    SELECT casrec_csv.pat."Case" FROM casrec_csv.pat WHERE casrec_csv.pat."Lay Team" != '{team}'
);

-- order table (cases)
DELETE FROM casrec_csv.order
USING casrec_csv.pat
WHERE pat."Case" = casrec_csv.order."Case"
AND casrec_csv.pat."Lay Team" != '{team}';

-- pat
DELETE FROM casrec_csv.pat WHERE "Lay Team" != '{team}';
