ALTER TABLE {schema}.persons ADD IF NOT EXISTS sirius_id int;
ALTER TABLE {schema}.addresses ADD IF NOT EXISTS sirius_id int;
ALTER TABLE {schema}.addresses ADD IF NOT EXISTS sirius_person_id int;
-- ALTER TABLE {schema}.cases ADD IF NOT EXISTS sirius_id int;
-- ALTER TABLE {schema}.cases ADD IF NOT EXISTS sirius_client_id int;
-- ALTER TABLE {schema}.notes ADD IF NOT EXISTS sirius_id int;
-- ALTER TABLE {schema}.person_caseitem ADD IF NOT EXISTS sirius_case_id int;
-- ALTER TABLE {schema}.person_caseitem ADD IF NOT EXISTS sirius_person_id int;
-- ALTER TABLE {schema}.person_note ADD IF NOT EXISTS sirius_person_id int;

DROP TABLE IF EXISTS {schema}.sirius_map_clients;
CREATE TABLE {schema}.sirius_map_clients
(
    caserecnumber     text,
    sirius_persons_id integer
);
ALTER TABLE {schema}.sirius_map_clients owner to casrec;

DROP TABLE IF EXISTS {schema}.sirius_map_addresses;
CREATE TABLE {schema}.sirius_map_addresses
(
    sirius_addresses_id integer,
    sirius_persons_id   integer
);
ALTER TABLE {schema}.sirius_map_addresses owner to casrec;




