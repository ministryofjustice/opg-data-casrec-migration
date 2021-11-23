-- Example SQL for finding a case that matches each lookup you may be interested in
-- This is for visits but modify as you see fit

select caserecnumber, 'visit_type', lookup
from (
select persons.caserecnumber as caserecnumber, visits.visittype as lookup,
row_number() over (partition by visits.visittype order by caserecnumber) as rown
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION') as subquery
where rown = 1
union all
select caserecnumber, 'visit_outcome', lookup
from (
select persons.caserecnumber as caserecnumber, visits.visitoutcome as lookup,
row_number() over (partition by visits.visitoutcome order by caserecnumber) as rown
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION') as subquery
where rown = 1
union all
select caserecnumber, 'visit_report_marked_as', lookup
from (
select persons.caserecnumber as caserecnumber, visits.visitreportmarkedas as lookup,
row_number() over (partition by visits.visitreportmarkedas order by caserecnumber) as rown
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION') as subquery
where rown = 1
union all
select caserecnumber, 'visit_sub_type', lookup
from (
select persons.caserecnumber as caserecnumber, visits.visitsubtype as lookup,
row_number() over (partition by visits.visitsubtype order by caserecnumber) as rown
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION') as subquery
where rown = 1
union all
select caserecnumber, 'who_to_visit', lookup
from (
select persons.caserecnumber as caserecnumber, visits.whotovisit as lookup,
row_number() over (partition by visits.whotovisit order by caserecnumber) as rown
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION') as subquery
where rown = 1
select visits.*
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
AND persons.caserecnumber = '13217597';
union all
select caserecnumber, 'visit_cancellation_reason', lookup
from (
select persons.caserecnumber as caserecnumber, visits.visitcancellationreason as lookup,
row_number() over (partition by visits.visitcancellationreason order by caserecnumber) as rown
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION') as subquery
where rown = 1
union all
select caserecnumber, 'visit_urgency', lookup
from (
select persons.caserecnumber as caserecnumber, visits.visiturgency as lookup,
row_number() over (partition by visits.visiturgency order by caserecnumber) as rown
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION') as subquery
where rown = 1

select * from
(select persons.caserecnumber as caserecnumber, 'visit_due_date_exists', cast(visits.visitduedate as text) as lookup
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
and visits.visitduedate is not null
order by persons.caserecnumber asc
limit 1) as subquery
union all
select * from
(select persons.caserecnumber as caserecnumber, 'visit_created_date', cast(visits.visitcreateddate as text) as lookup
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
and visits.visitcreateddate is not null
order by persons.caserecnumber asc
limit 1) as subquery
union all
select * from
(select persons.caserecnumber as caserecnumber, 'visit_report_due_date', cast(visits.visitreportduedate as text) as lookup
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
and visits.visitreportduedate is not null
order by persons.caserecnumber asc
limit 1) as subquery
union all
select * from
(select persons.caserecnumber as caserecnumber, 'visit_completed_date', cast(visits.visitcompleteddate as text) as lookup
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
and visits.visitcompleteddate is not null
order by persons.caserecnumber asc
limit 1) as subquery
union all
select * from
(select persons.caserecnumber as caserecnumber, 'visit_report_received_date', cast(visits.visitreportreceiveddate as text) as lookup
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
and visits.visitreportreceiveddate is not null
order by persons.caserecnumber asc
limit 1) as subquery
union all
select * from
(select persons.caserecnumber as caserecnumber, 'visit_commision_date', cast(visits.visitcommissiondate as text) as lookup
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
and visits.visitcommissiondate is not null
order by persons.caserecnumber asc
limit 1) as subquery
union all
select * from
(select persons.caserecnumber as caserecnumber, 'first_extended', cast(visits.firstextendedvisitreportduedate as text) as lookup
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
and visits.firstextendedvisitreportduedate is not null
order by persons.caserecnumber asc
limit 1) as subquery
union all
select * from
(select persons.caserecnumber as caserecnumber, 'second_extended', cast(visits.secondextendedvisitreportduedate as text) as lookup
FROM public.visits
LEFT JOIN public.persons ON persons.id = visits.client_id
WHERE persons.type = 'actor_client'
AND persons.clientsource = 'CASRECMIGRATION'
and visits.secondextendedvisitreportduedate is not null
order by persons.caserecnumber asc
limit 1) as subquery
