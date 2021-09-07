delete from events where source_person_id in (select id from persons where clientsource = 'SKELETON');
delete from events where owning_donor_id in (select id from persons where clientsource = 'SKELETON');
delete from document_secondaryrecipient where person_id in (select id from persons where clientsource = 'SKELETON');
delete from documents where correspondent_id in (select id from persons where clientsource = 'SKELETON');
