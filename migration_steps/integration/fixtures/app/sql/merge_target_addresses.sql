UPDATE {schema}.addresses
SET sirius_id = map.sirius_addresses_id
FROM {schema}.persons persons, {schema}.sirius_map_addresses map
WHERE persons.id = CAST(addresses.person_id AS INTEGER)
AND map.sirius_persons_id = persons.sirius_id;

UPDATE {schema}.addresses
SET sirius_person_id = persons.sirius_id
FROM {schema}.persons persons WHERE persons.id = CAST(addresses.person_id AS INTEGER)
