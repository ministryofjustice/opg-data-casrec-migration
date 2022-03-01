CREATE SCHEMA IF NOT EXISTS automated_letters;

DROP TABLE IF EXISTS automated_letters.sirius;

CREATE TABLE automated_letters.sirius(
    report_log_id int default NULL,
    letter_type text default NULL,
    letter_date date default NULL,
    caserecnumber text default NULL
);
