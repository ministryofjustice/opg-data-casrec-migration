CREATE SCHEMA IF NOT EXISTS deletions;

CREATE TABLE IF NOT EXISTS deletions.deletions_client_complaints (id int);
insert into deletions.deletions_client_complaints (id)
select co.id
from complaints co
inner join cases ca on co.caseitem_id = ca.id
inner join persons p on p.id = ca.client_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_document_pages (id int);
insert into deletions.deletions_client_document_pages (id)
select dpd.id
from document_pages_to_delete dpd
inner join documents doc on doc.id = dpd.document_id
inner join caseitem_document cd on doc.id = cd.document_id
inner join cases c on c.id = cd.caseitem_id
inner join persons p on p.id = c.client_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_annual_report_logs (id int);
insert into deletions.deletions_client_annual_report_logs (id)
select al.id
from annual_report_logs al
inner join persons p on p.id = al.client_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_hold_period (id int);
insert into deletions.deletions_client_hold_period (id)
select hp.id
from hold_period hp
inner join investigation inv on inv.id = hp.investigation_id
inner join persons p on p.id = inv.person_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_hold_period (id int);
insert into deletions.deletions_deputy_hold_period (id)
select hp.id
from hold_period hp
inner join investigation inv on inv.id = hp.investigation_id
inner join persons dep on dep.id = inv.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_investigation (id int);
insert into deletions.deletions_client_investigation (id)
select inv.id
from investigation inv
inner join persons p on p.id = inv.person_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_investigation (id int);
insert into deletions.deletions_deputy_investigation (id)
select inv.id
from investigation inv
inner join persons dep on dep.id = inv.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_phonenumbers (id int);
insert into deletions.deletions_client_phonenumbers (id)
select pn.id
from phonenumbers pn
inner join persons p on p.id = pn.person_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_phonenumbers (id int);
insert into deletions.deletions_deputy_phonenumbers (id)
select pn.id
from phonenumbers pn
inner join persons dep on dep.id = pn.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_addresses (id int);
insert into deletions.deletions_client_addresses (id)
select ad.id
from addresses ad
inner join persons p on p.id = ad.person_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_addresses (id int);
insert into deletions.deletions_deputy_addresses (id)
select ad.id
from addresses ad
inner join persons dep on dep.id = ad.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_validation_check (id int);
insert into deletions.deletions_validation_check (id)
select vc.id
from validation_check vc
inner join cases c  ON c.id = vc.caseitem_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

-- NOTE DO PERSON WARNING TOO
CREATE TABLE IF NOT EXISTS deletions.deletions_client_warnings (id int);
insert into deletions.deletions_client_warnings (id)
select wa.id
from warnings wa
inner join person_warning pw on wa.id = pw.warning_id
inner join persons p on p.id = pw.person_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_warnings (id int);
insert into deletions.deletions_deputy_warnings (id)
select wa.id
from warnings wa
inner join person_warning pw on wa.id = pw.warning_id
inner join persons dep on dep.id = pw.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

--NOTE DO PERSON TASK TOO
CREATE TABLE IF NOT EXISTS deletions.deletions_client_tasks (id int);
insert into deletions.deletions_client_tasks (id)
select t.id
from tasks t
inner join person_task pt on t.id = pt.task_id
inner join persons p on p.id = pt.person_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_tasks (id int);
insert into deletions.deletions_deputy_tasks (id)
select t.id
from tasks t
inner join person_task pt on t.id = pt.task_id
inner join persons dep on dep.id = pt.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_documents (id int);
insert into deletions.deletions_deputy_documents (id)
select d.id
from documents d
         inner join caseitem_document cd on d.id = cd.document_id
         inner join cases c on c.id = cd.caseitem_id
         inner join persons p on p.id = c.client_id
WHERE p.type = 'actor_client' and (caseactorgroup <> 'CLIENT-PILOT-ONE' or caseactorgroup is null)

--owning_donor_id for events
CREATE TABLE IF NOT EXISTS deletions.deletions_client_persons (id int);
insert into deletions.deletions_client_cases (id)
select c.id
from cases c
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

--owning_case_id for events
CREATE TABLE IF NOT EXISTS deletions.deletions_client_cases (id int);
insert into deletions.deletions_client_cases (id)
select c.id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

---------- OTHER NON EVENT -------

CREATE TABLE IF NOT EXISTS deletions.deletions_client_visits (id int);
insert into deletions.deletions_client_visits (id)
select v.id
from visits v
inner join persons p on p.id = v.client_id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_supervision_notes (id int);
insert into deletions.deletions_client_supervision_notes (id)
select s.id
from supervision_notes s
inner join persons p on p.id = s.person_id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_supervision_notes (id int);
insert into deletions.deletions_deputy_supervision_notes (id)
select s.id
from supervision_notes s
inner join persons dep on dep.id = s.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_powerofattorney_person (person_id int);
insert into deletions.deletions_client_powerofattorney_person (person_id)
select s.person_id
from powerofattorney_person s
inner join persons p on p.id = s.person_id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_powerofattorney_person (person_id int);
insert into deletions.deletions_deputy_powerofattorney_person (person_id)
select s.person_id
from powerofattorney_person s
inner join persons dep on dep.id = s.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_person_timeline (id int);
insert into deletions.deletions_client_person_timeline (id)
select s.id
from person_timeline s
inner join persons p on p.id = s.person_id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_person_timeline (id int);
insert into deletions.deletions_deputy_person_timeline (id)
select s.id
from person_timeline s
inner join persons dep on dep.id = s.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_person_timeline (id int);
insert into deletions.deletions_client_person_timeline (id)
select s.id
from person_timeline s
inner join persons p on p.id = s.person_id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_person_timeline (id int);
insert into deletions.deletions_deputy_person_timeline (id)
select s.id
from person_timeline s
inner join persons dep on dep.id = s.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_person_caseitem (person_id int);
insert into deletions.deletions_client_person_caseitem (person_id)
select s.person_id
from person_caseitem s
inner join persons p on p.id = s.person_id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_bonds (id int);
insert into deletions.deletions_deputy_bonds (id)
select bo.id
from bonds bo
inner join cases c  ON c.id = bo.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_death_notifications (id int);
insert into deletions.deletions_client_death_notifications (id)
select s.id
from death_notifications s
inner join persons p on p.id = s.person_id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_death_notifications (id int);
insert into deletions.deletions_deputy_death_notifications (id)
select s.id
from death_notifications s
inner join persons dep on dep.id = s.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_addresses (id int);
insert into deletions.deletions_client_addresses (id)
select s.id
from addresses s
inner join persons p on p.id = s.person_id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_addresses (id int);
insert into deletions.deletions_deputy_addresses (id)
select s.id
from addresses s
inner join persons dep on dep.id = s.person_id
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

-- order_deputy: deputy_id, persons: id
CREATE TABLE IF NOT EXISTS deletions.deletions_deputy_person (id int);
insert into deletions.deletions_deputy_person (id)
select dep.id
from persons dep
inner join order_deputy od on dep.id = od.deputy_id
inner join cases c  ON c.id = od.order_id
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);

CREATE TABLE IF NOT EXISTS deletions.deletions_client_cases (id int);
insert into deletions.deletions_client_cases (id)
select c.id
from cases c
inner join persons p on c.client_id = p.id
WHERE p.type = 'actor_client'
and (p.caseactorgroup <> 'CLIENT-PILOT-ONE' or p.caseactorgroup is null);


-- DELETE STATEMENTS
















































