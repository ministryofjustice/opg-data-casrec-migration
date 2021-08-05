SELECT firstname,
--        CONCAT(surname, ' (LIVELINK SKELETON)') as surname,
       surname,
       type,
       caserecnumber,
       'SKELETON'                              as clientsource,
       10                                      as supervisioncaseowner_id
FROM {schema}.persons
ORDER BY id ASC
LIMIT 10
