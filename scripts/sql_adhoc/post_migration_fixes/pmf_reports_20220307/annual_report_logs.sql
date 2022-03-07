CREATE SCHEMA if not exists pmf_reports_20220307_in1178;

select distinct p.caserecnumber, a.id as arl_id, a.casesupervisionlevel as original_value, s.supervisionlevel as expected_value
into pmf_reports_20220307_in1178.annual_report_log_updates
from persons p
inner join cases c on c.client_id = p.id
inner join supervision_level_log s ON c.id = s.order_id
inner join annual_report_logs a on p.id = a.client_id
where c.orderstatus = 'ACTIVE'
and a.status = 'RECEIVED'
and p.clientsource = 'CASRECMIGRATION';

select a.*
into pmf_reports_20220307_in1178.annual_report_log_audit
from pmf_reports_20220307_in1178.annual_report_log_updates f
inner join annual_report_logs a on a.id = f.arl_id;

begin;
update annual_report_logs a set casesupervisionlevel = f.expected_value
from pmf_reports_20220307_in1178.annual_report_log_updates f
where f.arl_id = a.id;
-- Run if counts incorrect
rollback;
-- Run if counts correct
commit;

-- Validation script (should be 0)
select caserecnumber, expected_value
from pmf_reports_20220307_in1178.annual_report_log_updates
except
select p.caserecnumber, a.casesupervisionlevel
from persons p
inner join cases c on c.client_id = p.id
inner join supervision_level_log s ON c.id = s.order_id
inner join annual_report_logs a on p.id = a.client_id
where c.orderstatus = 'ACTIVE'
and a.status = 'RECEIVED'
and p.clientsource = 'CASRECMIGRATION';
