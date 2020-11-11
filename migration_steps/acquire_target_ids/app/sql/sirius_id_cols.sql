ALTER TABLE etl3.addresses ADD IF NOT EXISTS sirius_id int;
ALTER TABLE etl3.addresses ADD IF NOT EXISTS sirius_person_id int;
-- ALTER TABLE etl3.cases ADD IF NOT EXISTS sirius_id int;
-- ALTER TABLE etl3.cases ADD IF NOT EXISTS sirius_client_id int;
-- ALTER TABLE etl3.notes ADD IF NOT EXISTS sirius_id int;
-- ALTER TABLE etl3.person_caseitem ADD IF NOT EXISTS sirius_case_id int;
-- ALTER TABLE etl3.person_caseitem ADD IF NOT EXISTS sirius_person_id int;
-- ALTER TABLE etl3.person_note ADD IF NOT EXISTS sirius_person_id int;
ALTER TABLE etl3.persons ADD IF NOT EXISTS sirius_id int;
