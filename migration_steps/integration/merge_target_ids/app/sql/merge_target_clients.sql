UPDATE {schema}.persons persons
SET sirius_id = map.sirius_id
FROM {schema}.sirius_map_client_persons map
WHERE map.caserecnumber = persons.caserecnumber
