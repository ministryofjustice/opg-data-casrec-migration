--Purpose: Set DEATH_CONFIRMED where proof of death exists (logic now changed in business rules)
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

SELECT
p.caserecnumber,
p.clientstatus,
p.clientsource,
p.type,
dn.proofofdeathreceived,
dn.datenotified,
p.id,
'DEATH_CONFIRMED' as expected_value
INTO {pmf_schema}.persons_updates
FROM persons p
inner join death_notifications dn on dn.person_id = p.id
where p.clientsource = 'CASRECMIGRATION' --HARD CODED AS ONLY APPLIES TO P1
and dn.proofofdeathreceived is TRUE
and dn.datenotified is not null
and p.clientstatus != 'DEATH_CONFIRMED'
and p.type = 'actor_client';

--@audit_tag
SELECT p.*
INTO {pmf_schema}.persons_audit
FROM persons p
INNER JOIN {pmf_schema}.persons_updates u on u.id = p.id;

--@update_tag
UPDATE persons p SET clientstatus = u.expected_value
FROM {pmf_schema}.persons_updates u
WHERE u.id = p.id;

--@validate_tag
SELECT id, expected_value
FROM {pmf_schema}.persons_updates
EXCEPT
SELECT p.id, p.clientstatus
FROM persons p
INNER JOIN {pmf_schema}.persons_audit pu on p.id = pu.id;
