-- crec_persons
DROP TABLE IF EXISTS casrec_csv.exceptions_crec_persons;

CREATE TABLE casrec_csv.exceptions_crec_persons(
    caserecnumber text default NULL,
    risk_score text default NULL
);

-- List of cases that have NaT for all entries in Modify for risk score (manual update based on casrec needed on these)
INSERT INTO casrec_csv.exceptions_crec_persons(
    SELECT
    caserecnumber,
    CAST(risk_score as INT)
    FROM (
      SELECT ROW_NUMBER() OVER (PARTITION by caserecnumber order by sortdate desc, risk_score desc) as rown,
      caserecnumber,
      risk_score
      FROM (
        SELECT
        casrec_csv.pat."Case" AS caserecnumber,
        casrec_csv.crec."Score" AS risk_score,
        to_timestamp(CONCAT(CASE WHEN crec."Modify" = '' THEN '1900-01-01' WHEN crec."Modify" = 'NaT' THEN '1900-01-01' ELSE LEFT(crec."Modify", 10) END, ' ', crec."at"), 'YYYY-MM-DD HH24:MI:SS.US') AS sortdate
        FROM casrec_csv.crec
        LEFT JOIN casrec_csv.pat
        ON pat."Case" = crec."Case"
    ) as crec_with_rowns) as crec_all
    WHERE rown = 1
    AND caserecnumber not in (
    '13308696',
    '1318577T',
    '12827293',
    '12541619'
    )
    EXCEPT
    SELECT * FROM (
        SELECT DISTINCT
            persons.caserecnumber AS caserecnumber,
            persons.risk_score AS risk_score
        FROM {target_schema}.persons
        WHERE persons.type = 'actor_client'
        AND persons.clientsource = '{clientsource}'
        ORDER BY caserecnumber ASC
    ) as sirius_data
);
