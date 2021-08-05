UPDATE {schema}.persons persons
SET sirius_id = map.sirius_persons_id
FROM {schema}.sirius_map_clients map
WHERE map.caserecnumber = persons.caserecnumber
