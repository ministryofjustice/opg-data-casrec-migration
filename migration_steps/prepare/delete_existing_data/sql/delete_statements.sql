delete from visits where client_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);



delete from supervision_notes where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from supervision_notes where source_clientriskscore_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from powerofattorney_person where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from phonenumbers where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from person_warning where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from person_timeline where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from person_task where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from persons where parent_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from persons where executor_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
update persons set client_id = null where id in (select id from persons where client_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null));
delete from persons where client_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from person_research_preferences where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from person_personreference where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from person_note where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from person_document where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from person_caseitem where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from pa_notified_persons where notified_person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from pa_certificate_provider where certificate_provider_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from pa_applicants where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from order_deputy where deputy_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from investigation where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from epa_personnotifydonor where personnotifydonor_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from death_notifications where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from cases where donor_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from cases where feepayer_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from cases where correspondent_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from annual_report_logs where client_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from addresses where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from bonds where order_id in (select id from cases where client_id in (select id from persons where (type in ('actor_client', 'actor_deputy') and caseactorgroup is null) or clientsource = 'CASRECMIGRATION'));
delete from document_secondaryrecipient where person_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from documents where correspondent_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
delete from cases where client_id in (select id from persons where type in ('actor_client', 'actor_deputy') and caseactorgroup is null);
