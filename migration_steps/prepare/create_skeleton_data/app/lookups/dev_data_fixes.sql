
DELETE FROM public.bond_providers where id not in (select distinct bond_provider_id from public.bonds);

INSERT INTO public.bond_providers (id, name, uid) VALUES (185, 'HOWDEN', 'HOWDEN_dev') ON CONFLICT DO NOTHING ;
INSERT INTO public.bond_providers (id, name, uid) VALUES (186, 'DBS', 'DBS_dev') ON CONFLICT DO NOTHING ;
INSERT INTO public.bond_providers (id, name, uid) VALUES (187, 'MARSH', 'MARSH_dev') ON CONFLICT DO NOTHING ;
INSERT INTO public.bond_providers (id, name, uid) VALUES (43745, 'OTHER', 'OTHER_dev') ON CONFLICT DO NOTHING ;
INSERT INTO public.bond_providers (id, name, uid) VALUES (43757, 'OTHER', 'OTHER2_dev') ON CONFLICT DO NOTHING ;

