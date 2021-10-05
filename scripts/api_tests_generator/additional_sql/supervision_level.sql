-- Always picks latest so we can use this to find latest
SELECT * FROM (
SELECT ROW_NUMBER() OVER (partition by persons.caserecnumber order by supervision_level_log.appliesfrom desc) as rown,
persons.caserecnumber, supervisionlevel, assetlevel
FROM public.supervision_level_log
LEFT JOIN public.cases ON cases.id = supervision_level_log.order_id
LEFT JOIN public.persons ON persons.id = cases.client_id
WHERE persons.clientsource = 'CASRECMIGRATION'
AND supervisionlevel = 'MINIMAL' AND assetlevel = 'UNKNOWN') as a
WHERE a.rown = 1
limit 5;
