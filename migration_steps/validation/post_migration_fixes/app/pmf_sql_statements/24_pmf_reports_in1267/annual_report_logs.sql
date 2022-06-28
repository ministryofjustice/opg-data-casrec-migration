--Purpose: Remove reports on P3 deputies that are prior to first order date as they were entered erroneously
--@setup_tag
CREATE SCHEMA IF NOT EXISTS {pmf_schema};

WITH earliest_order as
(select distinct on (p.caserecnumber) p.caserecnumber, c.orderdate
from persons p
inner join cases c on c.client_id = p.id
where p.clientsource = 'CASRECMIGRATION_P3' --Only run for this phase
and p.type = 'actor_client'
order by p.caserecnumber, c.orderdate asc)
select p.caserecnumber, arl.id as arl_id, arld.id as arld_id
into {pmf_schema}.annual_report_log_deletions
from annual_report_logs arl
inner join persons p on p.id = arl.client_id
inner join earliest_order eo on eo.caserecnumber = p.caserecnumber
left join annual_report_lodging_details arld ON arl.id = arld.annual_report_log_id
where arl.reportingperiodenddate::timestamp < eo.orderdate::timestamp;

--@audit_tag
select arl.*
into {pmf_schema}.annual_report_logs_audit
from annual_report_logs arl
inner join {pmf_schema}.annual_report_log_deletions del on arl.id = del.arl_id;

select arld.*
into {pmf_schema}.annual_report_lodging_details_audit
from annual_report_lodging_details arld
inner join {pmf_schema}.annual_report_log_deletions del on arld.id = del.arld_id;

--@update_tag
DELETE FROM annual_report_lodging_details
WHERE id IN (select id from {pmf_schema}.annual_report_lodging_details_audit);

DELETE FROM annual_report_logs
WHERE id IN (select id from {pmf_schema}.annual_report_logs_audit);

--@validate_tag
SELECT arl.*
FROM {pmf_schema}.annual_report_logs_audit arla
INNER JOIN annual_report_logs arl ON arl.id = arla.id;

SELECT arld.*
FROM {pmf_schema}.annual_report_lodging_details_audit arlda
INNER JOIN annual_report_lodging_details arld ON arld.id = arlda.id;