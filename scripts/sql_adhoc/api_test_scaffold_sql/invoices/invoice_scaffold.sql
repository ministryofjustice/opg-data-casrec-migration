-- Table: finance_ledger_allocation

select '/api/v1/finance/{id}/ledger-entries' as url, casereference as casereference, '["ledgerEntryAllocations"][*]["dateTime"]' as datetime, col1 as col
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fla.datetime is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    inner join finance_ledger_allocation fla on fla.ledger_entry_id = fl.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["ledgerEntryAllocations"][*]["amount"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fla.amount is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    inner join finance_ledger_allocation fla on fla.ledger_entry_id = fl.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["ledgerEntryAllocations"][*]["reference"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fla.reference is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    inner join finance_ledger_allocation fla on fla.ledger_entry_id = fl.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["ledgerEntryAllocations"][*]["notes"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fla.notes is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    inner join finance_ledger_allocation fla on fla.ledger_entry_id = fl.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["ledgerEntryAllocations"][*]["allocatedDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fla.allocateddate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    inner join finance_ledger_allocation fla on fla.ledger_entry_id = fl.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3;

-- Table: finance_remission_exemption

select '/api/v1/finance/{id}/finance-discounts', casereference, '["discountType"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    discounttype as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_remission_exemption fre on fre.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/finance-discounts', casereference, '["startDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fre.startdate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_remission_exemption fre on fre.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/finance-discounts', casereference, '["endDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fre.enddate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_remission_exemption fre on fre.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/finance-discounts', casereference, '["notes"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fre.notes is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_remission_exemption fre on fre.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/finance-discounts', casereference, '["status"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fre.enddate > '2022-04-01' then 'active' when fre.enddate < now() then 'expired' else 'dontuse' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_remission_exemption fre on fre.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3;

-- Table: finance_ledger

select '/api/v1/finance/{id}/ledger-entries', casereference, '["bankDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fl.bankdate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["confirmedDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fl.confirmeddate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["dateTime"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fl.datetime is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["method"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fl.method is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["amount"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fl.amount is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["notes"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fl.notes is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/ledger-entries', casereference, '["type"]["handle"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    fl."type" as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_ledger fl on fl.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3;

-- Table: finance_ledger

select '/api/v1/finance/{id}/invoices', casereference, '["feeType"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.feetype is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["reference"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.reference is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["startDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.startdate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["endDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.enddate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["amount"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.amount is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["supervisionLevel"]["handle"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    fi.supervisionlevel as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["confirmedDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.confirmeddate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["raisedDate"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.raiseddate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["sopStatus"]["handle"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.confirmeddate is null then 'confirmed_null' else 'confirmed_not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 3
union all
select '/api/v1/finance/{id}/invoices', casereference, '["status"]["handle"]', col1
from
(select
casereference,
col1,
row_number() over (partition by col1 order by casereference) as rown
from
    (select
    p.caserecnumber as casereference,
    case when fi.confirmeddate is null then 'null' else 'not_null' end as col1
    from persons p
    inner join finance_person fp on fp.person_id = p.id
    inner join finance_invoice fi on fi.finance_person_id = fp.id
    where p.clientsource = 'CASRECMIGRATION') as a1
) as a2
where rown < 10;
