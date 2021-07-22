select
p.caserecnumber,
p.id as person,
c1.id as cases,
pr.id as person_research_preferences,
dn.id as death_notifications,
v.id as visits,
pd.person_id as person_document,
arl.id as annual_report_logs,
e1.id as events,
ppr.person_id as person_personreference,
pcp.certificate_provider_id as pa_certificate_provider,
pci.person_id as person_caseitem,
pw.person_id as person_warning,
addr.id as addresses,
ct.caseitem_id as caseitem_task,
vc.caseitem_id as validation_check,
cq.case_id as caseitem_queue,
pan.pa_id as pa_notified_persons,
ocf.deputyship as order_courtfund,
arl.order_id as annual_report_logs,
ec1.source_cas as events,
ec2.owning_case as events,
pcpc.pa_id as pa_certificate_provider,
pcic.caseitem_ as person_caseitem,
cpt.caseitem_id as caseitem_paymenttype,
cpa.pa_id as pa_applicants,
ccom.caseitem_ as complaints,
cpap.powerofat as powerofattorney_person,
cw.caseitem_id as caseitem_warning,
cn.caseitem_id as caseitem_note,
sll.order_id as supervision_level_log,
ci.caseitem_id as investigation,
cb.order_id as bonds,
ctime.case_id as case_timeline,
cid.caseitem_id as caseitem_document,
cep.pa_id as epa_personnotifydonor,
cod.order_id as order_deputy
from persons p
left join cases c1 on c1.client_id = p.id
left join caseitem_task ct on ct.caseitem_id = c1.id
left join validation_check vc on vc.caseitem_id = c1.id
left join caseitem_queue cq on cq.case_id = c1.id
left join pa_notified_persons pan on pan.pa_id = c1.id
left join order_courtfund ocf on ocf.deputyship_id = c1.id
left join annual_report_logs arl on arl.order_id = c1.id
left join events ec1 on ec1.source_case_id = c1.id
left join events ec2 on ec2.owning_case_id = c1.id
left join pa_certificate_provider pcpc on pcpc.pa_id = c1.id
left join person_caseitem pcic on pcic.caseitem_id = c1.id
left join caseitem_paymenttype cpt on cpt.caseitem_id = c1.id
left join pa_applicants cpa on cpa.pa_id = c1.id
left join complaints ccom on ccom.caseitem_id = c1.id
left join powerofattorney_person cpap on cpap.powerofattorney_id = c1.id
left join caseitem_warning cw on cw.caseitem_id = c1.id
left join caseitem_note cn on cn.caseitem_id = c1.id
left join supervision_level_log sll on sll.order_id = c1.id
left join investigation ci on ci.caseitem_id = c1.id
left join bonds cb on cb.order_id = c1.id
left join case_timeline ctime on ctime.case_id = c1.id
left join caseitem_document cid on cid.caseitem_id = c1.id
left join epa_personnotifydonor cep on cep.pa_id = c1.id
left join order_deputy cod on cod.order_id = c1.id
left join persons odp on odp.id = cod.deputy_id
left join person_research_preferences pr on pr.person_id = p.id
left join death_notifications dn on dn.person_id = p.id
left join pa_notified_persons np on np.notified_person_id = p.id
left join visits v on v.client_id = p.id
left join person_note pn on pn.person_id = p.id
left join person_document pd on pd.person_id = p.id
left join annual_report_logs arl on arl.client_id = p.id
left join events e1 on e1.source_person_id = p.id
left join events e2 on e2.owning_donor_id = p.id
left join person_personreference ppr on ppr.person_id = p.id
left join pa_certificate_provider pcp on pcp.certificate_provider_id = p.id
left join person_caseitem pci on pci.person_id = p.id
left join person_warning pw on pw.person_id = p.id
left join addresses addr on addr.person_id = p.id
where p.caserecnumber = ''
