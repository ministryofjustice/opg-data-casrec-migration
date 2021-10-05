-- deputy_feepayer_id
DROP TABLE IF EXISTS casrec_csv.exceptions_deputy_feepayer_id;

CREATE TABLE casrec_csv.exceptions_deputy_feepayer_id(
    caserecnumber text default NULL,
    feepayer_id text default NULL
);

INSERT INTO casrec_csv.exceptions_deputy_feepayer_id(
    SELECT * FROM(
        SELECT DISTINCT
            pat."Case" AS caserecnumber,
            deputy.sirius_id AS feepayer_id
        FROM casrec_csv.pat
        LEFT JOIN casrec_csv.deputyship
            ON deputyship."Case" = pat."Case"
            AND deputyship."Fee Payer" = 'Y'
        LEFT JOIN casrec_csv.deputy
            ON deputy."Deputy No" = deputyship."Deputy No"
            AND deputy."Stat" = '1'
        WHERE True
        ORDER BY pat."Case"
     ) as csv_data
    EXCEPT
    SELECT * FROM(
        SELECT DISTINCT
            persons.caserecnumber AS caserecnumber,
            persons.feepayer_id AS feepayer_id
        FROM {target_schema}.persons
        WHERE True
            AND persons.type = 'actor_client'
            AND persons.clientsource = 'CASRECMIGRATION'
        ORDER BY caserecnumber ASC
     ) as sirius_data
);
