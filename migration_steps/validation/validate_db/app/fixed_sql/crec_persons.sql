-- crec_persons
DROP TABLE IF EXISTS casrec_csv.exceptions_crec_persons;

CREATE TABLE casrec_csv.exceptions_crec_persons(
    caserecnumber text default NULL,
    risk_score text default NULL
);

INSERT INTO casrec_csv.exceptions_crec_persons(
    SELECT
    caserecnumber,
    CAST(risk_score as INT)
    FROM (
      SELECT ROW_NUMBER() OVER (PARTITION by caserecnumber order by sortdate desc) as rown,
      caserecnumber,
      risk_score
      FROM (
        SELECT
        casrec_csv.pat."Case" AS caserecnumber,
        casrec_csv.crec_lookup(casrec_csv.crec."Score") AS risk_score,
        to_timestamp(CONCAT(CASE WHEN crec."Modify" = '' THEN '1900-01-01' ELSE crec."Modify" END, ' ', crec."at.1"), 'YYYY-MM-DD HH24:MI:SS.US') AS sortdate
        FROM casrec_csv.crec
        LEFT JOIN casrec_csv.pat
        ON pat."Case" = crec."Case"
    ) as crec_with_rowns) as crec_all WHERE rown = 1
    EXCEPT
    SELECT * FROM (
        SELECT DISTINCT
            persons.caserecnumber AS caserecnumber,
            persons.risk_score AS risk_score
        FROM {target_schema}.persons
        WHERE persons.type = 'actor_client'
        AND persons.clientsource = 'CASRECMIGRATION'
        ORDER BY caserecnumber ASC
    ) as sirius_data
);
