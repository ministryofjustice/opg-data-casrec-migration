-- automated_letters
SET datestyle = "ISO, DMY";

DROP TABLE IF EXISTS casrec_csv.exceptions_automated_letters;

CREATE TABLE casrec_csv.exceptions_automated_letters(
    caserecnumber text default NULL,
    letter_date text default NULL,
    letter_type text default NULL
);

INSERT INTO casrec_csv.exceptions_automated_letters(
    SELECT caseno as caserecnumber,
        "date"::date as letter_date,
        CASE
            WHEN "type" IN ('account_chase2an','account_chase2anl','account_chase2n','account_chase2nl') THEN 'RD1'
            WHEN "type" IN ('lodge_chase1n','lodge_chase1nl') THEN 'RD2'
            WHEN "type" IN ('lodge_chase2n','lodge_chase2nl') THEN 'RR1'
            WHEN "type" IN ('lodge_chase3n','lodge_chase3nl') THEN 'RR2'
            WHEN "type" = 'lodge_chaser' THEN 'RR3'
            WHEN "type" = 'further_chase1' THEN 'RI2-RI3-BS1-BS2'
        END AS letter_type
    FROM casrec_csv.casrec_letters

    EXCEPT

    SELECT
        caserecnumber,
        letter_date,
        CASE
            WHEN letter_type IN ('RI2','RI3','BS1','BS2') THEN 'RI2-RI3-BS1-BS2'
            ELSE letter_type
        END AS letter_type
    FROM automated_letters.sirius
);
