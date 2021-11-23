select count(*), 'cases' from persons p inner join cases a on a.client_id = p.id where p.id = 43016497 union all
select count(*), 'cases' from persons p inner join cases a on a.correspondent_id = p.id where p.id = 43016497 union all
select count(*), 'cases' from persons p inner join cases a on a.donor_id = p.id where p.id = 43016497 union all
select count(*), 'cases' from persons p inner join cases a on a.feepayer_id = p.id where p.id = 43016497 union all
select count(*), 'death_notifications' from persons p inner join death_notifications a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'pa_notified_persons' from persons p inner join pa_notified_persons a on a.notified_person_id = p.id where p.id = 43016497 union all
select count(*), 'visits' from persons p inner join visits a on a.client_id = p.id where p.id = 43016497 union all
select count(*), 'person_note' from persons p inner join person_note a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'person_document' from persons p inner join person_document a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'person_research_preferences' from persons p inner join person_research_preferences a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'annual_report_logs' from persons p inner join annual_report_logs a on a.client_id = p.id where p.id = 43016497 union all
select count(*), 'events' from persons p inner join events a on a.source_person_id = p.id where p.id = 43016497 union all
select count(*), 'events' from persons p inner join events a on a.owning_donor_id = p.id where p.id = 43016497 union all
select count(*), 'person_personreference' from persons p inner join person_personreference a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'pa_certificate_provider' from persons p inner join pa_certificate_provider a on a.certificate_provider_id = p.id where p.id = 43016497 union all
select count(*), 'person_caseitem' from persons p inner join person_caseitem a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'person_warning' from persons p inner join person_warning a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'supervision_notes' from persons p inner join supervision_notes a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'supervision_notes' from persons p inner join supervision_notes a on a.source_clientriskscore_id = p.id where p.id = 43016497 union all
select count(*), 'addresses' from persons p inner join addresses a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'pa_applicants' from persons p inner join pa_applicants a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'phonenumbers' from persons p inner join phonenumbers a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'persons' from persons p inner join persons a on a.client_id = p.id where p.id = 43016497 union all
select count(*), 'persons' from persons p inner join persons a on a.parent_id = p.id where p.id = 43016497 union all
select count(*), 'persons' from persons p inner join persons a on a.feepayer_id = p.id where p.id = 43016497 union all
select count(*), 'documents' from persons p inner join documents a on a.correspondent_id = p.id where p.id = 43016497 union all
select count(*), 'powerofattorney_person' from persons p inner join powerofattorney_person a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'investigation' from persons p inner join investigation a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'persons' from persons p inner join persons a on a.executor_id = p.id where p.id = 43016497 union all
select count(*), 'document_secondaryrecipient' from persons p inner join document_secondaryrecipient a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'person_timeline' from persons p inner join person_timeline a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'person_task' from persons p inner join person_task a on a.person_id = p.id where p.id = 43016497 union all
select count(*), 'epa_personnotifydonor' from persons p inner join epa_personnotifydonor a on a.personnotifydonor_id = p.id where p.id = 43016497 union all
select count(*), 'order_deputy' from persons p inner join order_deputy a on a.deputy_id = p.id where p.id = 43016497;

select count(*) from persons p inner join persons on p.client_id = persons.id where p.caserecnumber = '12112938';
select count(*) from persons p inner join persons on p.parent_id = persons.id where p.caserecnumber = '12112938';
select count(*) from persons p inner join assignees on p.supervisioncaseowner_id = assignees.id where p.caserecnumber = '12112938';
select count(*) from persons p inner join persons on p.feepayer_id = persons.id where p.caserecnumber = '12112938';
select count(*) from persons p inner join assignees on p.executivecasemanager_id = assignees.id where p.caserecnumber = '12112938';
select count(*) from persons p inner join persons on p.executor_id = persons.id where p.caserecnumber = '12112938';


select p.caserecnumber, fp.caserecnumber, fp.surname
from persons p
inner join persons fp on fp.feepayer_id = p.id
where p.clientsource = 'CASRECMIGRATION'
and fp.id = 43016497;

select * from persons where fee 12499758

UPDATE finance_person
SET batchnumber = '2693'
FROM finance_person fp
INNER JOIN persons p on fp.person_id = p.id
WHERE p.type = 'actor_client'
AND p.clientsource = 'CASRECMIGRATION'
AND fp.batchnumber IS NULL;

UPDATE finance_person set batchnumber = '2693'
where id in
(SELECT fp.id
FROM finance_person fp
INNER JOIN persons p on fp.person_id = p.id
WHERE p.type = 'actor_client'
AND p.clientsource = 'CASRECMIGRATION'
AND batchnumber IS NULL);

CREATE TABLE finance_p_ids (
    id     integer
);


insert into finance_p_ids (id)
SELECT fp.id
FROM finance_person fp
INNER JOIN persons p on fp.person_id = p.id
WHERE p.type = 'actor_client'
AND p.clientsource = 'CASRECMIGRATION'
AND batchnumber IS NULL;


ORDER by fp.id OFFSET 0 LIMIT 10000;

CREATE INDEX jim_idx ON finance_person (person_id);

select fp.*
from persons p
inner join finance_person fp on fp.person_id = p.id
WHERE p.type = 'actor_client'
AND p.clientsource = 'CASRECMIGRATION';
