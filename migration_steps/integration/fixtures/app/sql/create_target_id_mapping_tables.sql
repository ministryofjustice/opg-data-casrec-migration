DROP TABLE IF EXISTS sirius.sirius_map_clients;
CREATE TABLE sirius.sirius_map_clients
(
    caserecnumber     text,
    sirius_persons_id integer
);
alter table sirius.sirius_map_clients owner to casrec;
