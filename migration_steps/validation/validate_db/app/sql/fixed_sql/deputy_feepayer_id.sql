-- deputy_feepayer_id
DROP TABLE IF EXISTS {casrec_schema}.exceptions_deputy_feepayer_id;

CREATE TABLE {casrec_schema}.exceptions_deputy_feepayer_id(
    caserecnumber text default NULL,
    feepayer_id text default NULL
);

INSERT INTO {casrec_schema}.exceptions_deputy_feepayer_id(
    SELECT * FROM(
        SELECT DISTINCT
            pat."Case" AS caserecnumber,
            deputy.sirius_id AS feepayer_id
        FROM {casrec_schema}.pat
        LEFT JOIN {casrec_schema}.deputyship
            ON deputyship."Case" = pat."Case"
        LEFT JOIN {casrec_schema}.order
            ON "order"."Order No" = deputyship."Order No"
        LEFT JOIN {casrec_schema}.deputy
            ON deputy."Deputy No" = deputyship."Deputy No"
        WHERE True
            AND deputy."Stat" = '1'
            AND deputy."Disch Death" = ''
            AND "order"."Ord Stat" <> 'Open'
            AND deputyship."Fee Payer" = 'Y'
            AND pat."Case" NOT IN (
                    '11065340',
                    '13097967',
                    '11854030'
                )
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
            AND persons.clientsource = '{client_source}'
            AND persons.caserecnumber NOT IN (
                    '11065340',
                    '13097967',
                    '11854030'
                )
        ORDER BY caserecnumber ASC
     ) as sirius_data
);
