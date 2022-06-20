
DELETE FROM public.bond_providers where id not in (select distinct bond_provider_id from public.bonds);

INSERT INTO public.bond_providers (id, name, uid) VALUES (185, 'HOWDEN', 'HOWDEN_dev') ON CONFLICT DO NOTHING ;
INSERT INTO public.bond_providers (id, name, uid) VALUES (186, 'DBS', 'DBS_dev') ON CONFLICT DO NOTHING ;
INSERT INTO public.bond_providers (id, name, uid) VALUES (187, 'MARSH', 'MARSH_dev') ON CONFLICT DO NOTHING ;
INSERT INTO public.bond_providers (id, name, uid) VALUES (43745, 'OTHER', 'OTHER_dev') ON CONFLICT DO NOTHING ;
INSERT INTO public.bond_providers (id, name, uid) VALUES (43757, 'OTHER', 'OTHER2_dev') ON CONFLICT DO NOTHING ;

INSERT INTO public.assignees (id,parent_id,"name","type",email,surname,roles,suspended,groupname,phonenumber,deleted,teamtype,updateddate,permanent) VALUES
((SELECT max(id) + 1 from assignees),NULL,'Public Authority Deputy Team','assignee_user',NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,false),
((SELECT max(id) + 2 from assignees),NULL,'Supervision Closed Cases team','assignee_user',NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,false),
((SELECT max(id) + 3 from assignees),NULL,'Legal Team Deputyships','assignee_user',NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,false),
((SELECT max(id) + 4 from assignees),NULL,'Health and Welfare Team','assignee_user',NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,false),
((SELECT max(id) + 5 from assignees),NULL,'Lay Team 1','assignee_user',NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,false),
((SELECT max(id) + 6 from assignees),NULL,'Professional Team 1','assignee_user',NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,false),
(8730,NULL,'Supervision Closed Cases','assignee_user',NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,false),
((SELECT max(id) + 7 from assignees),NULL,'Deputyship Investigations','assignee_user',NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,false)