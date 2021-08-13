-- crec_persons
DROP TABLE IF EXISTS casrec_csv.exceptions_crec_persons;

CREATE TABLE casrec_csv.exceptions_crec_persons(
    caserecnumber text default NULL,
    risk_score text default NULL
);

INSERT INTO casrec_csv.exceptions_crec_persons(
    SELECT * FROM(
         SELECT
             caserecnumber,
             risk_score
         FROM (
            SELECT DISTINCT on (pat."Case")
                casrec_csv.pat."Case" AS caserecnumber,
                casrec_csv.crec_lookup(casrec_csv.crec."Score") AS risk_score,
                to_timestamp(CONCAT(crec."Create", ' ', crec."at"), 'YYYY-MM-DD HH24:MI:SS.US') AS sortdate
            FROM casrec_csv.crec
            LEFT JOIN casrec_csv.pat
                ON pat."Case" = crec."Case"
            ORDER BY caserecnumber ASC, sortdate DESC
            ) AS casrec
         ORDER BY caserecnumber ASC
     ) as csv_data
    EXCEPT
    SELECT * FROM(
        SELECT DISTINCT
            persons.caserecnumber AS caserecnumber,
            persons.risk_score AS risk_score
        FROM {target_schema}.persons
        WHERE persons.type = 'actor_client'
        AND persons.clientsource = 'CASRECMIGRATION'
        ORDER BY caserecnumber ASC
     ) as sirius_data
);
